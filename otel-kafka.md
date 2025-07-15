Perfect — in that case, you don’t need a full standalone Markdown doc. Instead, you can add a **Kafka-specific section** to your existing library documentation.

Here’s a concise, drop-in **section** you can paste into your existing `README.md` or internal handbook:

---

### 📦 Kafka Tracing Properties

If your service uses Kafka, the library provides auto-configuration to enable OpenTelemetry tracing for both **producer** and **consumer** sides. These settings are **optional** and default to enabled when Kafka is present.

| Property                      | Default | Description                                                             |
| ----------------------------- | ------- | ----------------------------------------------------------------------- |
| `otel.kafka.enabled`          | `true`  | Master switch to enable/disable all Kafka tracing logic.                |
| `otel.kafka.producer.enabled` | `true`  | Enables the Kafka **producer** interceptor. Requires `ProducerFactory`. |
| `otel.kafka.consumer.enabled` | `true`  | Enables the Kafka **consumer** interceptor. Requires `ConsumerFactory`. |

#### 🧪 Example YAML

```yaml
otel:
  kafka:
    enabled: true
    producer:
      enabled: true
    consumer:
      enabled: false
```

#### 💡 Notes

* Interceptors are only registered if Kafka is present **and** the appropriate factory beans (`ProducerFactory`, `ConsumerFactory`) exist.
* This library marks Kafka as an **optional dependency**, so apps must explicitly include `kafka-clients`.
* Tracing spans will only emit if OpenTelemetry is enabled and correctly configured.
* Logs will indicate when Kafka tracing is active:

  ```text
  [OTEL] Kafka producer interceptor is enabled
  [OTEL] Kafka record interceptor is enabled
  ```

---

You can place this under a heading like:

```
## Kafka Integration (Optional)
```

Let me know if you'd like this formatted as a collapsible section, or tailored to a specific documentation site or style (e.g. Docusaurus, AsciiDoc).
