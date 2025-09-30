Perfect 👍 — here’s the **full updated README** with all of your existing content preserved, but with the **modules explanation added**. I also added a link out to `docs/modules.md` in case you want a deeper dive later.

````markdown
# Spring Boot REST Archetypes

A reusable set of **Maven archetypes** that generate Spring Boot REST applications with **PCF deployment configuration**.  
This repository contains **two archetypes**, managed via Maven POM modules:

- **`basic`** – Generates a minimal Spring Boot REST service (internal or external).
- **`mongo`** – Extends the `basic` archetype with MongoDB multi-tenant support and optional REST API CRUD generation.

---

## Features

### Common (Both Archetypes)

- Ready-to-run **Spring Boot** app
- Example **REST controller** with configurable name, path, and message
- **Service type configuration** for both internal (`msvc`) and external (`coord`) services
- **Comprehensive PCF deployment configuration** for all environments (dev, sit, uat, nft, prd)
- Clean project structure with proper separation of concerns
- OpenTelemetry integration
- Actuator endpoints for monitoring
- Brand header support for multi-tenant operations

### Mongo Archetype (Extra)

- Spring Data MongoDB integration
- Multi-tenant MongoDB configuration
- Optional full **REST API** with CRUD, service layer, and exception handling
- Custom repositories with `MongoTemplate`
- Tenant-specific database routing
- Environment-specific MongoDB configs

---

## Build & Install Locally

Clone this repo and run:

```bash
mvn clean install
````

This installs **both archetypes** into your local Maven repository (`~/.m2/repository`).

---

## Deploy to Artifactory

TBC

---

## Using the Archetypes

You can generate a service using either the **interactive script** or **direct Maven commands**.

---

### Option 1: Interactive Script (Recommended)

Save this [`create-service.sh`](create-service.sh) in your `dev/work` folder and make it executable:

```bash
chmod +x create-service.sh
./create-service.sh
```

The script will guide you through:

* Basic project config (name, description, sub group)
* Service type (coord vs msvc)
* Archetype selection (`basic` or `mongo`)
* MongoDB/REST API settings (if `mongo` chosen)

It also validates package names to ensure OpenTelemetry tracing works properly.

---

### Option 2: Direct Maven Command

#### Basic Archetype

```bash
mvn archetype:generate \
  -DarchetypeGroupId=some.app.archetype \
  -DarchetypeArtifactId=basic-archetype \
  -DarchetypeVersion=0.0.1-SNAPSHOT \
  -DgroupId=some.app \
  -DartifactId=my-basic-service \
  -Dversion=1.0.0-SNAPSHOT \
  -Dpackage=some.app \
  -DprojectDescription="A sample basic service" \
  -DsubGroup=DigitalHomeBuying \
  -DserviceType=msvc \
  -DendpointName=Welcome \
  -DendpointMapping=welcome \
  -Dmessage="Hello from basic service!" \
  -DinteractiveMode=false
```

#### Mongo Archetype

```bash
mvn archetype:generate \
  -DarchetypeGroupId=some.app.archetype \
  -DarchetypeArtifactId=mongo-archetype \
  -DarchetypeVersion=0.0.1-SNAPSHOT \
  -DgroupId=some.app \
  -DartifactId=consent-service \
  -Dversion=1.0.0-SNAPSHOT \
  -Dpackage=some.app \
  -DprojectDescription="A sample Mongo-enabled service" \
  -DsubGroup=DigitalHomeBuying \
  -DserviceType=msvc \
  -DendpointName=Welcome \
  -DendpointMapping=welcome \
  -Dmessage="Hello from consent service!" \
  -DmongoCollectionName=consents \
  -DmongoClassName=Consent \
  -DincludeRestApi=true \
  -DinteractiveMode=false
```

---

### Option 3: Interactive Mode (Plain Maven)

Without arguments, Maven will prompt for all inputs:

```bash
mvn archetype:generate \
  -DarchetypeGroupId=some.app.archetype \
  -DarchetypeArtifactId=basic-archetype \
  -DarchetypeVersion=0.0.1-SNAPSHOT
```

---

## Generated Project Structure

### Basic Project

```
my-new-service/
├─ pom.xml
├─ README.md
├─ .gitignore
├─ pcf-config/
│  ├─ env-common.ini
│  ├─ env-dev.ini
│  ├─ env-nft.ini
│  ├─ env-prd.ini
│  ├─ env-sit.ini
│  ├─ env-uat.ini
│  ├─ pcf-dev.config
│  ├─ pcf-nft.config
│  ├─ pcf-prd.config
│  ├─ pcf-sit.config
│  ├─ pcf-uat.config
│  ├─ spring-application-dev.json
│  ├─ spring-application-nft.json
│  ├─ spring-application-prd.json
│  ├─ spring-application-sit.json
│  └─ spring-application-uat.json
├─ src/main/java/some/app/
│  ├─ Application.java
│  └─ controllers/WelcomeController.java
└─ src/main/resources/
    ├─ application.properties
    └─ application-local.properties
```

### With MongoDB + REST API

```
consent-service/
├─ pom.xml
├─ README.md
├─ .gitignore
├─ pcf-config/
│  ├─ env-common.ini
│  ├─ env-dev.ini
│  ├─ env-nft.ini
│  ├─ env-prd.ini
│  ├─ env-sit.ini
│  ├─ env-uat.ini
│  ├─ pcf-dev.config
│  ├─ pcf-nft.config
│  ├─ pcf-prd.config
│  ├─ pcf-sit.config
│  ├─ pcf-uat.config
│  ├─ spring-application-dev.json
│  ├─ spring-application-nft.json
│  ├─ spring-application-prd.json
│  ├─ spring-application-sit.json
│  └─ spring-application-uat.json
├─ src/main/java/some/app/
│  ├─ Application.java
│  ├─ controllers/
│  │  ├─ WelcomeController.java
│  │  └─ ConsentController.java
│  ├─ models/
│  │  └─ Consent.java
│  ├─ repositories/
│  │  └─ ConsentRepository.java
│  ├─ services/
│  │  ├─ ConsentService.java
│  │  └─ impl/ConsentServiceImpl.java
│  ├─ configs/
│  │  └─ MultiTenantMongoConfig.java
│  └─ exceptions/
│     └─ ConsentNotFoundException.java
└─ src/main/resources/
    ├─ application.properties
    └─ application-local.properties
```

---

## Run the Generated Project

```bash
cd my-new-service
mvn spring-boot:run
```

### Test Basic Endpoint

Visit `http://localhost:8080/welcome` → `Hello from my service!`

### Test MongoDB API (if enabled)

```bash
# Create a new entity (requires brand header)
curl -X POST http://localhost:8080/api/consents \
  -H "Content-Type: application/json" \
  -H "X-Brand: nwb" \
  -d '{"name":"John Doe","email":"john@example.com"}'

# Get entity by ID
curl -H "X-Brand: nwb" http://localhost:8080/api/consents/{id}
```

---

## Configuration Parameters

### Basic Parameters

| Property             | Default value               | Description                                           |
| -------------------- | --------------------------- | ----------------------------------------------------- |
| `groupId`            | —                           | Maven groupId for your new project                    |
| `artifactId`         | —                           | Maven artifactId for your new project                 |
| `version`            | `1.0.0-SNAPSHOT`            | Initial project version                               |
| `package`            | `some.app`                  | Base package name                                     |
| `projectDescription` | —                           | Description of the project purpose                    |
| `subGroup`           | —                           | Sub group or team name (e.g., DigitalHomeBuying)      |
| `serviceType`        | `msvc`                      | Service type: `coord` (external) or `msvc` (internal) |
| `endpointName`       | `Hello`                     | Controller class name (PascalCase)                    |
| `endpointMapping`    | `hello`                     | REST endpoint path (without leading slash)            |
| `message`            | `Hello from ${artifactId}!` | Response message from the example endpoint            |

### MongoDB Parameters

| Property              | Default value | Description                                           |
| --------------------- | ------------- | ----------------------------------------------------- |
| `mongoCollectionName` | —             | MongoDB collection name (required if MongoDB enabled) |
| `mongoClassName`      | `User`        | Entity class name (PascalCase)                        |
| `includeRestApi`      | `false`       | Include complete REST API (requires MongoDB)          |

---

## Service Types

### Coord Services (External Facing)

* **Domain**: `openapi.some.app.com` (production) / `dev-openapi.some.app.com` (dev)
* **Use case**: Services exposed to external consumers or UI applications
* **Hostname pattern**: `{service-name}-v1-mortgages`
* **Health check**: Full path `/mortgages/v1/{service-name}/actuator/health`

### MSVC Services (Internal Microservices)

* **Domain**: `internal-paas-ms.api.banksvcs.net`
* **Use case**: Internal microservices for backend communication
* **Hostname pattern**: `{service-name}-v1-hboapiplatform`
* **Health check**: `/actuator/health`

---

## PCF Configuration

The generated project includes comprehensive PCF deployment configuration files for all environments:

### Environment Configuration Files

#### `pcf-config/env-*.ini` Files

* **env-common.ini**: Shared configuration across all environments
* **env-dev.ini**: Development environment specific settings
* **env-sit.ini**: System Integration Test environment settings
* **env-uat.ini**: User Acceptance Test environment settings
* **env-nft.ini**: Non-Functional Test environment settings
* **env-prd.ini**: Production environment settings

#### `pcf-config/pcf-*.config` Files

* **pcf-dev.config**: PCF deployment configuration for development
* **pcf-sit.config**: PCF deployment configuration for SIT
* **pcf-uat.config**: PCF deployment configuration for UAT
* **pcf-nft.config**: PCF deployment configuration for NFT
* **pcf-prd.config**: PCF deployment configuration for production

Each config file is automatically configured based on your service type (coord vs msvc) and includes:

* Memory allocation and instance counts
* Domain and hostname configuration
* Health check endpoints
* Service binding configurations

#### `pcf-config/spring-application-*.json` Files

* **spring-application-dev.json**: Spring Boot configuration for development
* **spring-application-sit.json**: Spring Boot configuration for SIT
* **spring-application-uat.json**: Spring Boot configuration for UAT
* **spring-application-nft.json**: Spring Boot configuration for NFT
* **spring-application-prd.json**: Spring Boot configuration for production

These Velocity template files include:

* JWT and security configuration
* MongoDB connection settings (if enabled)
* Certificate and encryption configuration
* Environment-specific service bindings

---

## Repo Structure

```
java-archetypes-poc/
├─ pom.xml                     # parent pom, packaging=pom
├─ create-service.sh           # interactive generation script
├─ basic/                      # module for basic archetype
└─ mongo/                      # module for mongo archetype
```

### About the Modules

This repository is a **multi-module Maven project** (`packaging=pom`) that bundles multiple archetypes:

* **`basic/`** – Generates a minimal Spring Boot REST service.
* **`mongo/`** – Extends the basic archetype with MongoDB multi-tenancy and optional CRUD REST API.
* **Root `pom.xml`** – Parent POM that builds and installs both archetypes together.

When you run `mvn clean install` at the root, Maven installs **both archetypes** into your local repository.
You can then pick which archetype to use (`basic-archetype` or `mongo-archetype`) when generating a new service.

See [**docs/modules.md**](docs/modules.md) for more details on Maven multi-module projects and why this setup is used.

---

## Examples

### Generate a Basic Internal REST Service

```bash
./create-service.sh
# Choose: archetype = basic
# Choose: serviceType = msvc
```

### Generate an External Mongo-Backed Service

```bash
./create-service.sh
# Choose: archetype = mongo
# Choose: serviceType = coord
# Collection: users
# Class: User
# REST API: Y
```

### Generate an Internal Product Catalog Service

```bash
./create-service.sh
# Choose: archetype = mongo
# Choose: serviceType = msvc
# Collection: products
# Class: Product
# REST API: Y
```

---

> TODO: Add `archetype-catalog.xml` to publish both archetypes in one catalog.

```

---

Do you want me to also go ahead and **draft the `docs/modules.md`** with a short tutorial-style explanation of what Maven multi-modules are and how they apply here, so the link works straight away?
```
