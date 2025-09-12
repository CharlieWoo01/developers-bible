# 1) Repo structure

```
spring-boot-rest-poc-archetype/
├─ pom.xml                          # packaging = maven-archetype
└─ src/
   └─ main/
      └─ resources/
         ├─ META-INF/maven/archetype-metadata.xml
         └─ archetype-resources/
            ├─ pom.xml
            ├─ src/main/java/${package}/Application.java
            ├─ src/main/java/${package}/web/__endpointName__Controller.java
            └─ src/main/resources/application.properties
```

> `archetype-resources/**` is the template that will be copied into generated projects.
> Filenames can contain tokens like `__endpointName__` and contents use `${...}` tokens.

---

# 2) `pom.xml` (archetype project)

```xml
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 https://maven.apache.org/xsd/maven-4.0.0.xsd">
  <modelVersion>4.0.0</modelVersion>

  <groupId>com.mission.archetypes</groupId>
  <artifactId>spring-boot-rest-poc-archetype</artifactId>
  <version>1.0.0-SNAPSHOT</version>
  <name>Spring Boot REST POC Archetype</name>
  <packaging>maven-archetype</packaging>

  <properties>
    <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
    <maven.archetype.plugin.version>3.2.1</maven.archetype.plugin.version>
  </properties>

  <build>
    <plugins>
      <plugin>
        <groupId>org.apache.maven.plugins</groupId>
        <artifactId>maven-archetype-plugin</artifactId>
        <version>${maven.archetype.plugin.version}</version>
      </plugin>
    </plugins>
  </build>
</project>
```

---

# 3) `META-INF/maven/archetype-metadata.xml`

```xml
<archetype-descriptor
    xmlns="http://maven.apache.org/plugins/maven-archetype-plugin/archetype-descriptor/1.0.0"
    name="spring-boot-rest-poc">
  <requiredProperties>
    <requiredProperty key="groupId"/>
    <requiredProperty key="artifactId"/>
    <requiredProperty key="version" defaultValue="1.0.0-SNAPSHOT"/>
    <requiredProperty key="package" defaultValue="com.example.demo"/>

    <requiredProperty key="endpointName">
      <defaultValue>Hello</defaultValue>
      <description>PascalCase name for the controller class</description>
    </requiredProperty>
    <requiredProperty key="endpointPath">
      <defaultValue>/hello</defaultValue>
      <description>HTTP path to expose</description>
    </requiredProperty>
    <requiredProperty key="message">
      <defaultValue>Hello from ${artifactId}!</defaultValue>
      <description>Response body for the example endpoint</description>
    </requiredProperty>
  </requiredProperties>

  <fileSets>
    <!-- Java sources -->
    <fileSet filtered="true" packaged="true">
      <directory>src/main/java</directory>
      <includes>
        <include>**/*.java</include>
      </includes>
    </fileSet>

    <!-- Resources -->
    <fileSet filtered="true">
      <directory>src/main/resources</directory>
      <includes>
        <include>**/*</include>
      </includes>
    </fileSet>

    <!-- Root files -->
    <fileSet filtered="true">
      <directory>.</directory>
      <includes>
        <include>pom.xml</include>
      </includes>
    </fileSet>
  </fileSets>
</archetype-descriptor>
```

---

# 4) Template payload (`archetype-resources/**`)

## `archetype-resources/pom.xml`

```xml
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 https://maven.apache.org/xsd/maven-4.0.0.xsd">
  <modelVersion>4.0.0</modelVersion>
  <groupId>${groupId}</groupId>
  <artifactId>${artifactId}</artifactId>
  <version>${version}</version>
  <name>${artifactId}</name>

  <properties>
    <java.version>17</java.version>
    <spring.boot.version>3.3.4</spring.boot.version>
    <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
  </properties>

  <dependencyManagement>
    <dependencies>
      <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-dependencies</artifactId>
        <version>${spring.boot.version}</version>
        <type>pom</type>
        <scope>import</scope>
      </dependency>
    </dependencies>
  </dependencyManagement>

  <dependencies>
    <dependency>
      <groupId>org.springframework.boot</groupId>
      <artifactId>spring-boot-starter-web</artifactId>
    </dependency>
    <dependency>
      <groupId>org.springframework.boot</groupId>
      <artifactId>spring-boot-starter-test</artifactId>
      <scope>test</scope>
    </dependency>
  </dependencies>

  <build>
    <plugins>
      <plugin>
        <groupId>org.apache.maven.plugins</groupId>
        <artifactId>maven-compiler-plugin</artifactId>
        <version>3.13.0</version>
        <configuration>
          <source>${java.version}</source>
          <target>${java.version}</target>
        </configuration>
      </plugin>
      <plugin>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-maven-plugin</artifactId>
      </plugin>
    </plugins>
  </build>
</project>
```

## `archetype-resources/src/main/java/${package}/Application.java`

```java
package ${package};

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication
public class Application {
  public static void main(String[] args) {
    SpringApplication.run(Application.class, args);
  }
}
```

## `archetype-resources/src/main/java/${package}/web/__endpointName__Controller.java`

```java
package ${package}.web;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class __endpointName__Controller {

  @GetMapping("${endpointPath}")
  public String hello() {
    return "${message}";
  }
}
```

## `archetype-resources/src/main/resources/application.properties`

```properties
server.port=8080
```

---

# 5) Build, install, deploy

```bash
# from the archetype repo root
mvn clean install
# -> installs com.mission.archetypes:spring-boot-rest-poc-archetype:1.0.0-SNAPSHOT into ~/.m2

# deploy to your private repo (Nexus/Artifactory), no distributionManagement needed:
mvn deploy -DaltDeploymentRepository=private-repo::default::https://nexus.example.com/repository/maven-snapshots \
           -DskipTests
```

(Use releases URL for non-SNAPSHOTs.)

---

# 6) Consume the archetype

From any empty dir:

```bash
mvn archetype:generate \
  -DarchetypeGroupId=com.mission.archetypes \
  -DarchetypeArtifactId=spring-boot-rest-poc-archetype \
  -DarchetypeVersion=1.0.0-SNAPSHOT \
  -DgroupId=com.mission \
  -DartifactId=demo-rest \
  -Dversion=0.1.0-SNAPSHOT \
  -Dpackage=com.mission.demo \
  -DendpointName=Status \
  -DendpointPath=/status \
  -Dmessage="OK from demo-rest" \
  -DinteractiveMode=false
```

Run it:

```bash
cd demo-rest
mvn spring-boot:run
# http://localhost:8080/status -> "OK from demo-rest"
```

---

# 7) Optional: Catalog + GitLab pipeline

* **Catalog:** Some orgs host an `archetype-catalog.xml` in Nexus/Artifactory so `-DarchetypeCatalog=internal` lists your archetypes. Nice-to-have, not required.
