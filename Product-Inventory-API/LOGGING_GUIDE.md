# 🎯 Logging Guide - Product Inventory API

## Overview
This document explains how logging is implemented in this application and how to use it for debugging and monitoring.

---

## Logging Architecture

### Logger Setup (`app/core/logger.py`)
- **Modular design** - Can be copied to other projects
- **Dual output** - Console + File
- **Color-coded** - Easy visual parsing in terminal
- **Rotating files** - Prevents disk space issues
- **Separate error logs** - Critical issues in dedicated file

### Log Files Location
```
logs/
├── app.log          # All log levels (INFO, WARNING, ERROR, etc.)
└── app_error.log    # Only ERROR and CRITICAL
```

---

## Log Levels Used

### DEBUG
**When:** Detailed diagnostic information  
**Example:**
```python
logger.debug(f"Applied sorting: {sort_field}")
logger.debug(f"Found {total} matching products")
```

### INFO
**When:** Normal operation milestones  
**Example:**
```python
logger.info(
    f"Product created successfully: {product.name} (ID: {product.id})",
    extra={
        "product_id": str(product.id),
        "product_name": product.name,
    }
)
```

### WARNING
**When:** Unexpected but recoverable issues  
**Example:**
```python
logger.warning(
    f"Invalid product ID format: {product_id}",
    extra={"product_id": product_id, "error": str(e)}
)
```

### ERROR
**When:** Errors that prevent operation completion  
**Example:**
```python
logger.error(
    f"Failed to create product: {str(e)}",
    exc_info=True,  # Includes full stack trace
    extra={"product_data": product_data.model_dump()}
)
```

### CRITICAL
**When:** Application-level failures  
**Example:**
```python
logger.critical(
    f"Failed to start application: {str(e)}",
    exc_info=True
)
```

---

## Structured Logging with Context

### Why Use `extra` Parameter?
Makes logs machine-parsable and searchable.

**Example:**
```python
logger.info(
    "Creating new product: iPhone 14",
    extra={
        "product_name": "iPhone 14",
        "category": "Electronics",
        "price": 999.99,
        "quantity": 50,
        "operation": "create_product"
    }
)
```

**Output:**
```
2024-01-15 10:30:45 | INFO     | app.routes.product | product:create_product:42 | Creating new product: iPhone 14
```

**Benefits:**
- Can filter logs by product_name
- Can aggregate by category
- Can track specific operations
- Easy to parse with log aggregators (ELK, Splunk)

---

## Logging in Each Layer

### 1. Application Startup (`main.py`)
```python
logger.info(
    f"Starting {settings.APP_NAME} v{settings.APP_VERSION}",
    extra={
        "environment": settings.ENVIRONMENT,
        "debug": settings.DEBUG,
    }
)
```

### 2. Database Operations (`database.py`)
```python
logger.info(
    "Successfully connected to MongoDB",
    extra={
        "database": settings.DATABASE_NAME,
        "attempt": attempt,
    }
)
```

### 3. Request Middleware (`middleware.py`)
```python
logger.info(
    f"Incoming request: {method} {path}",
    extra={
        "request_id": request_id,
        "method": method,
        "path": path,
        "client_host": client_host,
    }
)
```

### 4. API Routes (`routes/product.py`)
```python
# Start of operation
logger.info(
    f"Creating new product: {product_data.name}",
    extra={
        "product_name": product_data.name,
        "category": product_data.category,
    }
)

# Success
logger.info(
    f"Product created successfully: {product.name}",
    extra={"product_id": str(product.id)}
)

# Error
logger.error(
    f"Failed to create product: {str(e)}",
    exc_info=True,
    extra={"product_data": product_data.model_dump()}
)
```

---

## Request Tracing

Every request gets a unique ID for tracking across logs.

**Example flow:**
```
# Request arrives
INFO | Incoming request: POST /products | request_id=abc123

# Route handler
INFO | Creating new product: iPhone 14 | request_id=abc123

# Database operation
INFO | Product created successfully | request_id=abc123

# Request completes
INFO | Request completed: POST /products - Status: 201 - Time: 0.145s | request_id=abc123
```

**Finding all logs for a request:**
```bash
grep "request_id=abc123" logs/app.log
```

---

## Common Logging Patterns

### Pattern 1: CRUD Operations
```python
logger.info(f"Starting operation: {operation_name}", extra={...})
try:
    # Do work
    logger.info(f"Operation successful", extra={...})
except SpecificError as e:
    logger.warning(f"Validation failed", extra={...})
except Exception as e:
    logger.error(f"Operation failed", exc_info=True, extra={...})
```

### Pattern 2: Database Queries
```python
logger.debug(f"Executing query with filters: {filters}")
results = await query.to_list()
logger.debug(f"Query returned {len(results)} results")
```

### Pattern 3: Validation Errors
```python
logger.warning(
    f"Invalid input: {error_message}",
    extra={
        "input_data": data,
        "validation_errors": errors
    }
)
```

---

## Searching & Filtering Logs

### By Level
```bash
# Only errors
grep "ERROR" logs/app.log

# Errors and critical
grep -E "ERROR|CRITICAL" logs/app.log
```

### By Operation
```bash
# All product creations
grep "Creating new product" logs/app.log

# All database operations
grep "MongoDB" logs/app.log
```

### By Request ID
```bash
# Trace a specific request
grep "request_id=abc-123" logs/app.log
```

### By Time Range
```bash
# Logs from specific date
grep "2024-01-15" logs/app.log

# Logs from specific hour
grep "2024-01-15 14:" logs/app.log
```

---

## Monitoring in Production

### Key Metrics to Track

1. **Error Rate**
```bash
# Count errors per hour
grep "ERROR" logs/app.log | grep "$(date +%Y-%m-%d\ %H:)" | wc -l
```

2. **Request Volume**
```bash
# Requests per minute
grep "Incoming request" logs/app.log | grep "$(date +%Y-%m-%d\ %H:%M)" | wc -l
```

3. **Slow Requests**
```bash
# Requests taking > 1 second
grep "Request completed" logs/app.log | awk -F'Time: ' '{print $2}' | awk -F's' '$1 > 1.0'
```

4. **Database Health**
```bash
# Database connection issues
grep -E "MongoDB.*fail|MongoDB.*error" logs/app.log
```

---

## Log Rotation

**Current Settings:**
- Max file size: 10 MB
- Backup count: 5 files
- Encoding: UTF-8

**Files created:**
```
app.log          # Current
app.log.1        # Previous
app.log.2        # Older
...
app.log.5        # Oldest (deleted when new rotation occurs)
```

**Change rotation settings** in `main.py`:
```python
logger_config = LoggerConfig(
    max_file_size=20 * 1024 * 1024,  # 20 MB
    backup_count=10,  # Keep 10 backups
)
```

---

## Integration with Log Aggregators

### ELK Stack (Elasticsearch, Logstash, Kibana)
```python
# Add JSON formatter for structured logs
import json_log_formatter

formatter = json_log_formatter.JSONFormatter()
handler.setFormatter(formatter)
```

### Grafana Loki
```yaml
# promtail config
scrape_configs:
  - job_name: product-api
    static_configs:
      - targets:
          - localhost
        labels:
          app: product-inventory
          __path__: /app/logs/*.log
```

### Datadog / New Relic
Use their Python integrations to ship logs directly.

---

## Environment-Specific Settings

### Development
```env
LOG_LEVEL=DEBUG
LOG_TO_CONSOLE=True
LOG_TO_FILE=True
LOG_USE_COLORS=True
```

### Production
```env
LOG_LEVEL=INFO
LOG_TO_CONSOLE=True
LOG_TO_FILE=True
LOG_USE_COLORS=False  # Colors can break some log parsers
```

---

## Troubleshooting with Logs

### Problem: API returning 500 error

**Step 1:** Find the error
```bash
grep "ERROR" logs/app.log | tail -20
```

**Step 2:** Get the request ID
```
ERROR | Failed to create product | request_id=abc123
```

**Step 3:** Trace the full request
```bash
grep "abc123" logs/app.log
```

**Step 4:** Check stack trace in error log
```bash
tail -50 logs/app_error.log
```

---

## Best Practices

### ✅ DO
- Use structured logging with `extra` parameter
- Include relevant context (IDs, names, counts)
- Use appropriate log levels
- Log both success and failure cases
- Include stack traces for errors (`exc_info=True`)

### ❌ DON'T
- Log sensitive data (passwords, tokens, PII)
- Log inside tight loops (use counters instead)
- Use print() statements (use logger)
- Log at DEBUG level in production
- Forget to log request/response for debugging

---

## Quick Reference

| What to Log | Level | Include |
|-------------|-------|---------|
| Request received | INFO | method, path, request_id, client IP |
| Operation started | INFO | operation name, input params |
| Operation succeeded | INFO | result summary, IDs |
| Validation error | WARNING | input data, error details |
| Not found | INFO | searched ID/criteria |
| Application error | ERROR | error message, stack trace, context |
| DB connection issue | ERROR | connection details, retry attempt |
| Startup/shutdown | INFO | app name, version, environment |
| Slow operation | WARNING | duration, operation details |
| Critical failure | CRITICAL | full context, stack trace |

---

## Example: Full Request Lifecycle Logs

```
2024-01-15 10:30:45 | INFO | RequestLoggingMiddleware | Incoming request: POST /products | request_id=abc123, client=192.168.1.100
2024-01-15 10:30:45 | INFO | product | Creating new product: iPhone 14 | request_id=abc123, category=Electronics
2024-01-15 10:30:45 | DEBUG | database | Inserting document into products collection
2024-01-15 10:30:45 | INFO | product | Product created successfully: iPhone 14 | product_id=507f1f77bcf86cd799439011
2024-01-15 10:30:45 | INFO | RequestLoggingMiddleware | Request completed: POST /products - Status: 201 - Time: 0.145s | request_id=abc123
```

---