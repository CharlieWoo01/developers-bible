# Avro codegen: quick generate & troubleshoot guide (Maven + IntelliJ)

## 1) Minimal `pom.xml` setup

Put this under `<build><plugins>`:

```xml
<!-- Generate Java from Avro .avsc files -->
<plugin>
  <groupId>org.apache.avro</groupId>
  <artifactId>avro-maven-plugin</artifactId>
  <version>1.12.0</version>
  <executions>
    <execution>
      <id>schemas</id>
      <phase>generate-sources</phase>
      <goals><goal>schema</goal></goals>
      <configuration>
        <stringType>String</stringType>
        <sourceDirectory>${project.basedir}/src/main/resources/kafka/avro/schema</sourceDirectory>
        <outputDirectory>${project.build.directory}/generated-sources/avro</outputDirectory>
      </configuration>
    </execution>
  </executions>
</plugin>
```

> Your `.avsc` files live in `src/main/resources/kafka/avro/schema`.

## 2) Generate the classes

From project root:

```bash
mvn clean generate-sources
# or
mvn avro:schema
# full compile path
mvn clean compile
```

Generated Java ends up in:

```
target/generated-sources/avro
```

## 3) Make IntelliJ see them

* Maven tool window → **Reload All Maven Projects** (this fixes most cases).
* If needed: Right-click `target/generated-sources/avro` → **Mark Directory As → Generated Sources Root**.
* Settings → **Build Tools ▸ Maven ▸ Importing** → *Generated sources folders:* **Detect automatically** → Reload Maven.
* **Build ▸ Rebuild Project**.

## 4) Quick sanity checks (common pitfalls)

* **Namespace matches imports:** In your `.avsc`, `namespace` must match the package you import (e.g. `com.mg.events` → import `com.mg.events.PlayerCreated`).
* **Plugin actually runs:** `mvn -X generate-sources` should show `avro-maven-plugin` execution.
* **Clean stale output:** `rm -rf target && mvn clean generate-sources`.
* **Version alignment:** Use Avro plugin **1.11+** with Avro schemas created for 1.9+; avoid mixing very old runtime libs.
* **Multi-module builds:** Put the plugin in the module that holds the schemas (not only in the parent).
* **Schema errors:** Invalid defaults or unions (e.g., `["null","string"]` with default `""`) will skip generation—check the console.

## 5) “Still not importing?” belt-and-braces

Add Build Helper so Maven explicitly registers the generated folder:

```xml
<plugin>
  <groupId>org.codehaus.mojo</groupId>
  <artifactId>build-helper-maven-plugin</artifactId>
  <version>3.5.0</version>
  <executions>
    <execution>
      <id>add-avro-sources</id>
      <phase>generate-sources</phase>
      <goals><goal>add-source</goal></goals>
      <configuration>
        <sources>
          <source>${project.build.directory}/generated-sources/avro</source>
        </sources>
      </configuration>
    </execution>
  </executions>
</plugin>
```

Then:

```bash
mvn clean generate-sources
```

and **Reload Maven** in IntelliJ.

## 6) Nuclear option

**File ▸ Invalidate Caches / Restart…** → *Invalidate and Restart*.

---

That’s it—run `mvn generate-sources`, reload Maven, and you’re good. Want me to add a tiny sample `.avsc` and show the generated class shape?
