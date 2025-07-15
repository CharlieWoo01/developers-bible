Here you go — a clean, production-ready **Markdown document** describing the Kafka tracing configuration properties for your OTEL wrapper library.

---

````markdown
# Kafka Tracing Configuration

This library provides auto-configuration for OpenTelemetry Kafka interceptors to enable distributed tracing for producer and consumer flows.

Kafka tracing is **enabled by default** if Kafka is present on the classpath and OpenTelemetry is active. You can control tracing behavior using the properties described below.

---

## 📌 Global Property

| Property                | Default | Description                                                                 |
|------------------------|---------|-----------------------------------------------------------------------------|
| `otel.kafka.enabled`   | `true`  | **Master switch** to enable or disable Kafka tracing entirely.              |

If `otel.kafka.enabled` is set to `false`, no Kafka interceptors will be registered — regardless of the sub-settings.

---

## ⚙️ Producer Interceptor

| Property                         | Default | Description                                                              |
|----------------------------------|---------|--------------------------------------------------------------------------|
| `otel.kafka.producer.enabled`   | `true`  | Enables the `ProducerInterceptor` for tracing outgoing Kafka messages.   |

Only applied if:
- Kafka is present (`ProducerInterceptor.class`)
- OpenTelemetry is enabled (`OpenTelemetry` bean exists)
- A `ProducerFactory` bean is available in the application context

---

## 🎧 Consumer Interceptor

| Property                         | Default | Description                                                              |
|----------------------------------|---------|--------------------------------------------------------------------------|
| `otel.kafka.consumer.enabled`   | `true`  | Enables the `RecordInterceptor` for tracing incoming Kafka messages.     |

Only applied if:
- Kafka is present (`RecordInterceptor.class`)
- OpenTelemetry is enabled (`OpenTelemetry` bean exists)
- A `ConsumerFactory` bean is available in the application context

---

## 🧪 Example Configuration

### 🔁 Enable both producer and consumer tracing (default)

```yaml
otel:
  kafka:
    enabled: true
    producer:
      enabled: true
    consumer:
      enabled: true
````

### 🔇 Disable Kafka tracing entirely

```yaml
otel:
  kafka:
    enabled: false
```

### 🎯 Enable only producer tracing

```yaml
otel:
  kafka:
    enabled: true
    producer:
      enabled: true
    consumer:
      enabled: false
```

### 🎯 Enable only consumer tracing

```yaml
otel:
  kafka:
    enabled: true
    producer:
      enabled: false
    consumer:
      enabled: true
```

---

## 🧠 Notes

* The Kafka dependencies (`kafka-clients`) are marked as `optional` in this library. Your application must include them explicitly for tracing to activate.
* Interceptors are only registered if the relevant Kafka `*Factory` beans are present in the Spring context.
* All configurations are auto-detected via Spring Boot's `@ConditionalOn...` mechanism, with sane defaults.
* OpenTelemetry must be enabled and properly configured for spans to be emitted.

---

## 🔍 Logs

When enabled, you will see logs like:

```text
[OTEL] Kafka tracing auto-configuration is enabled
[OTEL] Kafka producer interceptor is enabled
[OTEL] Kafka record interceptor is enabled
```

These logs appear only when the relevant conditions are met.

---

## 📦 Dependency

Make sure your application includes the following (if not using a starter):

```xml
<dependency>
  <groupId>your.group</groupId>
  <artifactId>otel-kafka-tracing</artifactId>
</dependency>

<dependency>
  <groupId>org.apache.kafka</groupId>
  <artifactId>kafka-clients</artifactId>
</dependency>
```

If you're using a Spring Boot starter module you created internally, this is likely already bundled.

---

```

Let me know if you want a `.md` file download or to include a diagram of the trace flow between services.
```
