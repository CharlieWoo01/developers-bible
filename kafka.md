awesome — here’s a compact doc you can drop into your repo (either `docs/kafka.md` or a README section). it explains **where things live**, **what each class does**, **how the listener container is built (manual ack)**, and **how we use Avro + SR**, without big config or code blocks.

---

# Kafka (Avro) Architecture & Conventions

## 1) Package structure

```
src/main/java/com/yourco/app
├─ kafka/
│  ├─ config/
│  │  ├─ KafkaProducerFactoryBuilder.java
│  │  ├─ KafkaConsumerFactoryBuilder.java
│  │  ├─ KafkaErrorHandlerConfig.java
│  │  ├─ AvroKafkaConsumerConfig.java      # builds the listener container (manual ack)
│  │  └─ AvroKafkaProducerConfig.java      # (present if we produce)
│  ├─ listener/
│  │  └─ CapieHydrateConfirmationListener.java
│  └─ producer/                            # (optional) producers live here
│     └─ ...
└─ (other non-Kafka app packages)
```

> Avro schemas live in `src/main/avro/*.avsc` (generated classes end up in `target/generated-sources/avro`, not in `main/java`).

---

## 2) Responsibilities (at a glance)

| Component                          | What it does                                                                           | Key notes                                                                                                                                   |
| ---------------------------------- | -------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------- |
| `KafkaProducerFactoryBuilder`      | Creates a `ProducerFactory<K,V>` from Spring’s `KafkaProperties` plus a few overrides. | Keeps producer wiring DRY; serializers are supplied by the caller.                                                                          |
| `KafkaConsumerFactoryBuilder`      | Creates a `ConsumerFactory<K,V>` from `KafkaProperties` plus overrides.                | We pass the deserializer(s) here; supports extra props per consumer type.                                                                   |
| `KafkaErrorHandlerConfig`          | Central `CommonErrorHandler` (currently `DefaultErrorHandler`).                        | Handles listener errors **and** deserialization errors (when using `ErrorHandlingDeserializer`), with fixed backoff + max attempts; no DLT. |
| `AvroKafkaConsumerConfig`          | Wires the **Avro** consumer factory + `ConcurrentKafkaListenerContainerFactory`.       | Sets **AckMode = MANUAL_IMMEDIATE**; plugs in the shared `CommonErrorHandler`.                                                              |
| `AvroKafkaProducerConfig`          | (If used) Wires a `KafkaTemplate<K,V>` for Avro.                                       | Enables idempotence/acks etc.                                                                                                               |
| `CapieHydrateConfirmationListener` | The business listener.                                                                 | Uses `@KafkaListener(..., containerFactory="avroKafkaListenerContainerFactory")` and calls `ack.acknowledge()` after successful processing. |

---

## 3) How the pieces fit (consumer path)

1. **Spring Boot config** (`spring.kafka.*`) supplies the base Kafka properties (bootstrap servers, SR URL, serializers, etc.).
2. **`KafkaConsumerFactoryBuilder`** reads those and applies **Avro-specific overrides** (e.g., `specific.avro.reader`, and **ErrorHandlingDeserializer** delegates to `KafkaAvroDeserializer` when enabled).
3. **`AvroKafkaConsumerConfig`** creates a `ConcurrentKafkaListenerContainerFactory` and sets:

   * `AckMode = MANUAL_IMMEDIATE` (we commit offsets exactly when we call `ack.acknowledge()`).
   * the shared `CommonErrorHandler` (retries/backoff; no DLT).
   * concurrency (usually `1` for strict ordering).
4. **Listeners** are annotated with `@KafkaListener` pointing to topic/group properties (no hard-coded strings). The method signature accepts `ConsumerRecord<K,V>` and an `Acknowledgment` to perform the manual commit.

**Why manual immediate?**

* We only commit after we’ve finished processing, not at poll nor in batches.
* Deterministic in tests and production; easy to reason about retries.

---

## 4) Avro & Schema Registry

* We use **Confluent Avro Serializer/Deserializer**.
* In **tests**, the SR URL is a **mock scope** (`mock://<scope>`), so there’s no real network or auth.
* Decide per environment whether producers **auto-register** schemas:

  * **Dev/Test**: usually **on** (or pre-register with the mock client).
  * **Higher envs**: often **off** + manage schemas via CI/CD.

**Important flags (wherever you set them):**

* `specific.avro.reader` → `true`
* `auto.register.schemas` → on/off depending on env
* `use.latest.version` → generally **false** (use the schema ID embedded in the record; safer and faster)

---

## 5) Topics, groups, naming

* Topics and groups are configured in YAML and bound into the listener via placeholders, e.g.:

  * `spring.kafka.topics.capieHydrateConfirmation`
  * `spring.kafka.groups.capieHydrateConfirmationGroup`
* **Do not** hard-code topic names or groups in code.
* Prefer `kebab.case.vN` for topic names, and meaningful groups (one per consumer app/concern).

---

## 6) Error-handling model

* We **do not** use a DLT.
* Transient failures: retried by `DefaultErrorHandler` with `FixedBackOff`.
* Deserialization failures:

  * **If** we wrap with `ErrorHandlingDeserializer`, the failure is surfaced to the error handler (as a `DeserializationException` with headers), not as a hard poll failure.
  * This avoids the container stopping on bad payloads.
* Permanent failures:

  * After `maxAttempts`, the record is logged (and will not be re-attempted unless re-polled).

Keep the retry policy conservative to avoid message “thrashing”.

---

## 7) Testing (one-liner overview)

* **Embedded Kafka** (`@EmbeddedKafka`) spins an in-memory broker for the test run.
* **Mock Schema Registry** uses an in-JVM scope (e.g. `mock://capie-it`), cleaned up after tests.
* Tests send **real Avro** messages using a `KafkaTemplate` and verify the **real listener** was invoked (e.g. `@SpyBean + verify(timeout(...))`).
* Manual ack is exercised exactly as in production.

(See `docs/kafka-testing.md` for the test pattern; no big config included here.)

---

## 8) Conventions & Do/Don’t

**Do**

* Keep **all Kafka beans** under `kafka/config` and **listeners** under `kafka/listener`.
* Keep topic/group **in YAML**, referenced via placeholders in `@KafkaListener`.
* Use **manual immediate ack** for idempotent, deterministic processing.
* Wrap deserializers with `ErrorHandlingDeserializer` where you want graceful handling.
* Use `src/main/avro` for schema sources + Avro Maven plugin for codegen.

**Don’t**

* Don’t hard-code topic names/groups in Java.
* Don’t mix real SR URLs into test profile.
* Don’t enable `use.latest.version` in tests unless you’re pre-registering schemas.

---

## 9) Quick FAQ

**Q: Where do I add a new Kafka consumer?**
Create a new `@KafkaListener` in `kafka/listener`, wire it to the **same** `avroKafkaListenerContainerFactory`, and add its topic/group to YAML.

**Q: Where do I tweak retries/backoff?**
In `KafkaErrorHandlerConfig` (the shared `CommonErrorHandler`), so all listeners inherit it.

**Q: Where do I change serializers/deserializers?**
Prefer environment config (YAML) for base serializers; the builder applies only minimal, consumer-specific overrides.

**Q: How do I add a producer?**
Add a `KafkaTemplate` in `AvroKafkaProducerConfig` (or reuse an existing one) and a thin producer in `kafka/producer`.

---

If you want, I can add a **tiny “How to add a new listener” checklist** (4–5 bullets) you can paste at the end of this doc.
