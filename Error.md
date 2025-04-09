Perfect — here's a full **POC implementation** of a reusable **Spring Boot error handling library** with environment-based masking, structured error responses, and the ability to extend in your services.

---

## **1. Library Module: `error-handler-lib`**

### `pom.xml` (library module)
```xml
<project>
  <modelVersion>4.0.0</modelVersion>
  <groupId>com.example</groupId>
  <artifactId>error-handler-lib</artifactId>
  <version>1.0.0</version>
  <packaging>jar</packaging>

  <dependencies>
    <dependency>
      <groupId>org.springframework.boot</groupId>
      <artifactId>spring-boot-starter-web</artifactId>
    </dependency>
  </dependencies>
</project>
```

---

### `ErrorResponse.java`
```java
package com.example.errorhandling.model;

import java.util.Map;

public class ErrorResponse {
    private final String title;
    private final String detail;
    private final Map<String, Object> errors;
    private final String code;
    private final int status;

    public ErrorResponse(String title, String detail, Map<String, Object> errors, String code, int status) {
        this.title = title;
        this.detail = detail;
        this.errors = errors;
        this.code = code;
        this.status = status;
    }

    public String getTitle() { return title; }
    public String getDetail() { return detail; }
    public Map<String, Object> getErrors() { return errors; }
    public String getCode() { return code; }
    public int getStatus() { return status; }
}
```

---

### `ApiExceptionMetadata.java`
```java
package com.example.errorhandling.annotation;

import org.springframework.http.HttpStatus;

import java.lang.annotation.*;

@Retention(RetentionPolicy.RUNTIME)
@Target(ElementType.TYPE)
public @interface ApiExceptionMetadata {
    String code();
    HttpStatus status();
}
```

---

### `BaseApiExceptionHandler.java`
```java
package com.example.errorhandling.handler;

import com.example.errorhandling.annotation.ApiExceptionMetadata;
import com.example.errorhandling.model.ErrorResponse;
import org.springframework.core.env.Environment;
import org.springframework.http.*;
import org.springframework.validation.FieldError;
import org.springframework.web.bind.MethodArgumentNotValidException;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.context.request.WebRequest;
import org.springframework.web.servlet.mvc.method.annotation.ResponseEntityExceptionHandler;

import java.util.*;
import java.util.stream.Collectors;

public class BaseApiExceptionHandler extends ResponseEntityExceptionHandler {

    protected final Environment environment;

    public BaseApiExceptionHandler(Environment environment) {
        this.environment = environment;
    }

    @ExceptionHandler(Exception.class)
    public ResponseEntity<Object> handleAll(Exception ex, WebRequest request) {
        return buildGenericErrorResponse(ex, HttpStatus.INTERNAL_SERVER_ERROR);
    }

    @Override
    protected ResponseEntity<Object> handleMethodArgumentNotValid(
        MethodArgumentNotValidException ex,
        HttpHeaders headers,
        HttpStatus status,
        WebRequest request
    ) {
        Map<String, Object> fieldErrors = ex.getBindingResult().getFieldErrors().stream()
            .collect(Collectors.toMap(FieldError::getField, FieldError::getDefaultMessage));

        return buildGenericErrorResponse(ex, status, fieldErrors);
    }

    protected ResponseEntity<Object> buildGenericErrorResponse(Exception ex, HttpStatus status) {
        return buildGenericErrorResponse(ex, status, null);
    }

    protected ResponseEntity<Object> buildGenericErrorResponse(Exception ex, HttpStatus status, Map<String, Object> errors) {
        String code = "CODE_" + status.value();
        String title = status.getReasonPhrase();
        String detail = shouldMaskDetails() ? "An unexpected error occurred." : ex.getMessage();

        ApiExceptionMetadata meta = ex.getClass().getAnnotation(ApiExceptionMetadata.class);
        if (meta != null) {
            code = meta.code();
            status = meta.status();
            title = status.getReasonPhrase();
        }

        ErrorResponse response = new ErrorResponse(title, detail, errors, code, status.value());
        return new ResponseEntity<>(response, status);
    }

    protected boolean shouldMaskDetails() {
        return Arrays.asList(environment.getActiveProfiles()).contains("prod");
    }
}
```

---

### Optional: `BadRequestException.java`
```java
package com.example.errorhandling.exception;

import com.example.errorhandling.annotation.ApiExceptionMetadata;
import org.springframework.http.HttpStatus;

@ApiExceptionMetadata(code = "CODE_BAD_REQUEST", status = HttpStatus.BAD_REQUEST)
public class BadRequestException extends RuntimeException {
    public BadRequestException(String message) {
        super(message);
    }
}
```

---

## **2. Consumer App POC (`demo-service`)**

### Add to your app's `pom.xml`
```xml
<dependency>
  <groupId>com.example</groupId>
  <artifactId>error-handler-lib</artifactId>
  <version>1.0.0</version>
</dependency>
```

---

### `GlobalExceptionHandler.java` in your app
```java
package com.example.demo.handler;

import com.example.errorhandling.handler.BaseApiExceptionHandler;
import org.springframework.core.env.Environment;
import org.springframework.web.bind.annotation.RestControllerAdvice;

@RestControllerAdvice
public class GlobalExceptionHandler extends BaseApiExceptionHandler {

    public GlobalExceptionHandler(Environment environment) {
        super(environment);
    }

    // Add project-specific handlers here if needed
}
```

---

### Example Controller
```java
@RestController
@RequestMapping("/api")
public class DemoController {

    @GetMapping("/fail")
    public ResponseEntity<Void> fail() {
        throw new BadRequestException("This is a bad request.");
    }
}
```

---

### Profile Config (to see masking behavior)
```yaml
spring:
  profiles:
    active: prod
```

---

## ✅ Summary

| Feature                  | Provided In Lib? | Extensible in App? |
|--------------------------|------------------|---------------------|
| Error response format    | Yes              | Yes                 |
| Exception metadata       | Yes              | Yes                 |
| Validation handler       | Yes              | Yes                 |
| Base handler class       | Yes              | Yes                 |
| Profile-based masking    | Yes              | Yes                 |
| ControllerAdvice binding | Optional         | Yes (recommended)   |

---

Would you like a working GitHub template or zip of this whole structure?
