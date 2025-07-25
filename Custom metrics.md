Great — to make this **as performant as possible** and avoid **eager loading of unnecessary classes**, especially if the annotation is never used, follow these principles:

---

## ✅ Key Requirements

* `@OtelMetric` annotation and `MetricType` enum should **exist** in the API package.
* Supporting classes like `OtelMetricAspect` and any config **must not be loaded** unless annotation is used.
* Use **Spring Boot auto-configuration with conditions** to lazy-load.
* Avoid reflection or expensive logic in runtime path.

---

## 📁 Final Structure Overview

```
otel-metrics-lib/
├── api/
│   └── OtelMetric.java
│   └── MetricType.java
├── internal/
│   └── OtelMetricAspect.java
│   └── OtelMetricAutoConfiguration.java
├── META-INF/
│   └── spring/
│       └── org.springframework.boot.autoconfigure.EnableAutoConfiguration
```

---

## ✅ Step-by-Step Code

### 1. `@OtelMetric` annotation (lightweight)

```java
package com.yourorg.metrics.api;

import com.yourorg.metrics.api.MetricType;
import java.lang.annotation.*;

@Target({ElementType.METHOD})
@Retention(RetentionPolicy.RUNTIME)
@Documented
public @interface OtelMetric {
    String name();
    String description() default "";
    MetricType type() default MetricType.COUNTER;
    String[] tags() default {};
}
```

---

### 2. `MetricType` enum

```java
package com.yourorg.metrics.api;

public enum MetricType {
    COUNTER,
    TIMER,
    HISTOGRAM
}
```

---

### 3. Aspect (loaded only if annotation is on classpath)

```java
package com.yourorg.metrics.internal;

import com.yourorg.metrics.api.OtelMetric;
import com.yourorg.metrics.api.MetricType;
import io.micrometer.core.instrument.*;
import org.aspectj.lang.*;
import org.aspectj.lang.annotation.*;
import org.springframework.stereotype.Component;

import java.util.Arrays;
import java.util.stream.Stream;

@Aspect
@Component
public class OtelMetricAspect {

    private final MeterRegistry registry;

    public OtelMetricAspect(MeterRegistry registry) {
        this.registry = registry;
    }

    @Around("@annotation(metric)")
    public Object instrumentMetric(ProceedingJoinPoint pjp, OtelMetric metric) throws Throwable {
        String[] tags = parseTags(metric.tags());

        return switch (metric.type()) {
            case COUNTER -> {
                Counter.builder(metric.name())
                    .description(metric.description())
                    .tags(tags)
                    .register(registry)
                    .increment();
                yield pjp.proceed();
            }

            case TIMER -> {
                Timer timer = Timer.builder(metric.name())
                    .description(metric.description())
                    .tags(tags)
                    .register(registry);
                yield timer.recordCallable(pjp::proceed);
            }

            case HISTOGRAM -> {
                DistributionSummary summary = DistributionSummary.builder(metric.name())
                    .description(metric.description())
                    .tags(tags)
                    .register(registry);
                Object result = pjp.proceed();
                if (result instanceof Number number) {
                    summary.record(number.doubleValue());
                }
                yield result;
            }
        };
    }

    private String[] parseTags(String[] raw) {
        return Arrays.stream(raw)
            .flatMap(s -> {
                String[] kv = s.split("=", 2);
                return kv.length == 2 ? Stream.of(kv) : Stream.empty();
            })
            .toArray(String[]::new);
    }
}
```

---

### 4. Auto-Configuration (safe + lazy)

```java
package com.yourorg.metrics.internal;

import com.yourorg.metrics.api.OtelMetric;
import io.micrometer.core.instrument.MeterRegistry;
import org.springframework.boot.autoconfigure.condition.*;
import org.springframework.context.annotation.*;

@Configuration
@ConditionalOnClass(OtelMetric.class)
@ConditionalOnBean(MeterRegistry.class)
public class OtelMetricAutoConfiguration {

    @Bean
    @ConditionalOnMissingBean
    public OtelMetricAspect otelMetricAspect(MeterRegistry meterRegistry) {
        return new OtelMetricAspect(meterRegistry);
    }
}
```

---

### 5. `spring.factories` (Spring Boot 2)

```properties
# src/main/resources/META-INF/spring/org.springframework.boot.autoconfigure.EnableAutoConfiguration
com.yourorg.metrics.internal.OtelMetricAutoConfiguration
```

---

> ✅ Spring Boot 3 users should use `spring/org.springframework.boot.autoconfigure.AutoConfiguration.imports` instead.

---

## ✅ Result

* 🚀 **Zero overhead** unless someone uses `@OtelMetric` (due to `@ConditionalOnClass`).
* ⚡ Micrometer + OpenTelemetry metrics created **only on usage**.
* 🔌 Easily shareable across services via Maven dependency.

---

Would you like me to:

* Package this as a reusable JAR or starter template?
* Add unit tests for `OtelMetricAspect`?
* Add support for `@OtelMetric(tags = {"dynamic:userId"})` where values come from `MethodArgs`?

Let me know.
