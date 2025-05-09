## **Spring Boot Environment Dashboard – Summary of Ideas (No Code Required)**

### **1. Build & Git Metadata**

**Goal**: Show what version is running and where it came from

| Source                                           | Config / Env                                    | Purpose                                         |
| ------------------------------------------------ | ----------------------------------------------- | ----------------------------------------------- |
| `/actuator/info`                                 | `management.info.git.mode=full`                 | Shows `commit.id`, `branch`, `build.time`, etc. |
| `/actuator/env`                                  | `spring.profiles.active`                        | Show active profile                             |
| **Deployment metadata (deployedBy, deployedAt)** | **Handled via deployment pipeline**             | **Not exposed via `/info`; tracked externally** |

---

### **2. Runtime Diagnostics & Dev Debugging**

**Goal**: Help developers quickly identify config and runtime issues

| Source                 | What to Look For                                                                           |
| ---------------------- | ------------------------------------------------------------------------------------------ |
| `/actuator/mappings`   | List of all application and actuator endpoints                                             |
| `/actuator/env`        | See resolved values like `spring.datasource.url`, `spring.data.mongodb.uri`, `app.*`, etc. |
| `/actuator/metrics`    | Uptime, memory usage, CPU load, request volume, thread usage                               |
| `/actuator/health`     | Component status (DB, disk, Redis, etc.)                                                   |
| `/actuator/loggers`    | Current log levels (adjustable in dev only)                                                |
| `/actuator/threaddump` | View active threads (for deadlock/scheduler issues)                                        |

---

### **3. Platform/Integration Visibility via `/actuator/info`**

**Goal**: Surface key backend features — useful across dev, ops, and business

| Key                     | Example                 | Description                           |
| ----------------------- | ----------------------- | ------------------------------------- |
| `info.dbType`           | `MongoDB`, `PostgreSQL` | Determined from data source URI       |
| `info.otel.enabled`     | `true` / `false`        | Indicates if OpenTelemetry is enabled |
| `info.features.cache`   | `redis`, `none`         | Cache backend used                    |
| `info.features.email`   | `true`, `false`         | Whether email integration is active   |
| `info.features.storage` | `s3`, `filesystem`      | File storage method                   |
| `info.featureFlags.*`   | `true`, `false`         | Expose current feature toggles        |
| `info.tenants`          | `[brandA, brandB]`      | Optional list of loaded tenants       |

---

### **4. Environment-Specific Configuration & Masking**

Expose full info only in **non-production environments**. In production, either mask or fully suppress non-essential info.

#### `application-dev.yml`

```yaml
management:
  info.git.mode: full
  endpoint:
    env:
      enabled: true
      show-values: always
    loggers:
      enabled: true
    mappings:
      enabled: true
    threaddump:
      enabled: true
  endpoints:
    web:
      exposure:
        include: "*"

info:
  dbType: ${DB_TYPE:MongoDB}
  otel:
    enabled: ${OTEL_ENABLED:true}
  features:
    cache: redis
    storage: s3
    email: true
  featureFlags:
    newDashboard: true
    referralBonus: false
  tenants: [brandA, brandB]
```

#### `application-prod.yml`

```yaml
management:
  info.git.mode: full
  endpoint:
    env:
      enabled: false
    loggers:
      enabled: false
    mappings:
      enabled: false
    threaddump:
      enabled: false
  endpoints:
    web:
      exposure:
        include: health, info

# Mask all custom info fields in production
info: {}
```
