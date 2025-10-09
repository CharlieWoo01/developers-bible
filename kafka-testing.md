Perfect — let’s keep it lean and maintainable 👍
Here’s a **short, lightweight doc** you can safely keep in your repo (e.g. `docs/kafka-testing.md` or add as a section in your main README).
No config dumps or big code blocks — just enough to explain how the system works and how to use it.

---

# 🧩 Kafka Integration Testing (Overview)

We use **Embedded Kafka** with **Mock Schema Registry** to test our Avro-based Kafka consumers and producers without hitting real infrastructure.

---

## 🔍 How it works

### Embedded Kafka

Spring Kafka’s `@EmbeddedKafka` spins up an **in-memory broker** for the duration of the test.

* It runs inside the JUnit process — no Docker or external Kafka required.
* The property `spring.embedded.kafka.brokers` automatically points to this temporary broker.
* Topics declared in `@EmbeddedKafka(topics = …)` are created automatically before the test runs.
* Each test class can safely run in isolation (we reset context before each test).

### Mock Schema Registry

Instead of connecting to Confluent Cloud or a real Schema Registry, tests use `mock://capie-it`.

* The Confluent Avro serializers/deserializers are fully compatible with this in-memory mock.
* No authentication or network calls are made.
* The schema registry scope (`capie-it`) is dropped automatically at the end of each test run.

Together, these simulate a **real Kafka + SR environment** completely in memory.

---

## ⚙️ How we write Kafka integration tests

We use a small helper config class (`KafkaIntegrationTestConfig`) that:

* registers the mock Schema Registry
* provides a `KafkaTemplate` using the Avro serializer
* can be imported via `@Import` in any Kafka test

Each test then:

1. Starts Embedded Kafka (`@EmbeddedKafka`)
2. Loads the test Spring context (`@SpringBootTest`, profile = `test`)
3. Injects the `KafkaTemplate`
4. Uses a real listener (with manual ack mode)
5. Verifies the message was consumed and acknowledged

---

## 🧪 Example pattern

Every Kafka IT follows this structure:

* **Annotation setup**

  * `@SpringBootTest`
  * `@ActiveProfiles("test")`
  * `@EmbeddedKafka(partitions = 1, topics = "...")`
  * `@Import(KafkaIntegrationTestConfig.class)`
* **Send event:** use the `KafkaTemplate` to publish an Avro message.
* **Assert:** use `@SpyBean` on the listener and `verify(listener, timeout(...)).listen(...)` to check consumption.

We rely on **manual immediate ack mode**, so our listener commits offsets explicitly (`ack.acknowledge()`), ensuring deterministic and testable behavior.

---

## 📁 Folder convention

```
src/test/java/com/yourco/app/kafka/
├─ config/     → test-only config beans (e.g. KafkaIntegrationTestConfig)
├─ listener/   → integration tests for Kafka listeners
└─ util/       → optional helpers for Avro/test data
```

This mirrors the production `kafka` package structure for consistency and discoverability.

---

## 🧠 Why this setup

* No external dependencies (runs anywhere)
* Fast and reliable
* Avro schemas validated automatically
* Manual ack ensures we test exactly what production does
* Safe for CI pipelines

---

> 🏁 **Summary:**
> Embedded Kafka + Mock SR = fully functional Kafka environment in memory.
> Integration tests run end-to-end without touching real brokers.
> Extendable, isolated, and simple to maintain.

---

Would you like me to format this as a short section (for your main `README.md`) instead of a separate `docs/kafka-testing.md`?
