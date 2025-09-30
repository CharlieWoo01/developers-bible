Here’s an updated **README** for your repo that reflects the fact you now have **two archetypes (`basic` and `mongo`)** and that you’re managing them via **pom modules**. I’ve restructured the doc so it’s clear which archetype does what, and how to use them:

---

# Spring Boot REST Archetypes

A reusable set of **Maven archetypes** that generate minimal Spring Boot REST applications with **PCF deployment
configuration**. This repository contains **two archetypes**, managed via Maven modules:

* **`basic`** – Generates a minimal Spring Boot REST service (internal or external).
* **`mongo`** – Extends the `basic` archetype with MongoDB multi-tenant support and optional REST API CRUD generation.

---

## Features

### Common (Both Archetypes)

* Ready-to-run **Spring Boot** app
* Example **REST controller** with configurable name, path, and message
* **Service type configuration** for both internal (`msvc`) and external (`coord`) services
* **Comprehensive PCF deployment configuration** for all environments (dev, sit, uat, nft, prd)
* Clean project structure with proper separation of concerns
* OpenTelemetry integration
* Actuator endpoints for monitoring
* Brand header support for multi-tenant operations

### Mongo Archetype (Extra)

* Spring Data MongoDB integration
* Multi-tenant MongoDB configuration
* Optional full **REST API** with CRUD, service layer, and exception handling
* Custom repositories with `MongoTemplate`
* Tenant-specific database routing
* Environment-specific MongoDB configs

---

## Build & Install Locally

Clone this repo and run:

```bash
mvn clean install
```

This installs both archetypes into your local Maven repository (`~/.m2/repository`).

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

## Repo Structure

```
java-archetypes-poc/
├─ pom.xml                     # parent pom, packaging=pom
├─ create-service.sh           # interactive generation script
├─ basic/                      # module for basic archetype
│  └─ src/main/resources/
│     └─ META-INF/maven/archetype-metadata.xml
└─ mongo/                      # module for mongo archetype
   └─ src/main/resources/
      └─ META-INF/maven/archetype-metadata.xml
```

Each archetype module (`basic`, `mongo`) has its own template under
`src/main/resources/archetype-resources/`.

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

---

> TODO: Add `archetype-catalog.xml` to publish both archetypes in one catalog.

---

Do you want me to also **split the README into two mini-sections** (one for each archetype), or keep them unified under one doc like this?
