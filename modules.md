Great — here’s a first draft of **`docs/modules.md`** that explains the **multi-module setup** and why you’re using it:

````markdown
# Archetype Modules

This repository is organized as a **Maven multi-module project** (`packaging=pom`) that contains multiple archetypes under
a single parent build. This approach keeps related archetypes together and makes it easy to build, version, and publish
them consistently.

---

## What Is a Maven Multi-Module Project?

A multi-module Maven project is one where:

- The **root project** has `packaging=pom`.
- Each **child project (module)** has its own directory and `pom.xml`.
- Building the root project automatically builds all modules in the correct order.

Benefits:

- **Centralized build**: run `mvn clean install` once at the root to build and install all archetypes.
- **Shared versioning**: modules can use the same version and parent configuration.
- **Separation of concerns**: each archetype lives in its own module, with its own templates and metadata.
- **Extensibility**: you can add new archetypes in the future without changing the structure.

---

## Current Modules

### `basic`

The **basic archetype** generates a minimal Spring Boot REST service.  
Key features:

- Example REST controller with configurable name, path, and message
- Internal (`msvc`) and external (`coord`) service type support
- PCF configuration files for all environments
- OpenTelemetry setup and actuator endpoints
- Clean starter project structure

### `mongo`

The **mongo archetype** builds on the `basic` one by adding MongoDB multi-tenant support.  
Additional features:

- Spring Data MongoDB integration
- Multi-tenant database routing
- Configurable collection and entity class
- Optional full CRUD REST API with service layer and exception handling
- Environment-specific MongoDB configurations

---

## How the Build Works

At the root, the `pom.xml` declares both modules:

```xml
<modules>
  <module>basic</module>
  <module>mongo</module>
</modules>
````

When you run:

```bash
mvn clean install
```

Maven will:

1. Build the `basic` archetype
2. Build the `mongo` archetype
3. Install both into your local `~/.m2/repository`

You can then generate new projects with either:

* `-DarchetypeArtifactId=basic-archetype`
* `-DarchetypeArtifactId=mongo-archetype`

---

## Why This Setup?

* **One repo, multiple archetypes** – keeps everything consistent
* **Shared lifecycle** – both archetypes follow the same release process
* **Scalability** – easy to add more archetypes in the future (e.g. `kafka`, `postgres`, etc.)
* **Cleaner separation** – avoids bloated conditional logic in a single archetype

---

## Adding a New Module

To add another archetype module:

1. Create a new folder (e.g. `postgres/`)
2. Inside, create its own `pom.xml` with `<packaging>maven-archetype</packaging>`
3. Add `src/main/resources/archetype-metadata.xml` and `archetype-resources/` with template files
4. Add the module to the root `<modules>` section

Example:

```xml
<modules>
  <module>basic</module>
  <module>mongo</module>
  <module>postgres</module>
</modules>
```

Now building the parent project will also build `postgres`.

---

## Next Steps

* Decide on **which archetype to use** (`basic` vs `mongo`) when generating a project.
* Optionally, publish an `archetype-catalog.xml` so both archetypes appear in Maven’s archetype list.
* Extend with additional modules if you need new archetype flavors.

---

```

---

Would you like me to also add a **diagram** (ASCII or Mermaid) showing the parent → modules (`basic`, `mongo`) relationship, so it’s more visual for new devs?
```
