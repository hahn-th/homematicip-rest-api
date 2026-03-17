# Code Review Findings

This file tracks the current review findings so we can work them down one by one without losing context.

## Open

### 1. Sensitive data can leak into logs

- Severity: High
- Area: Security
- Files:
  - `src/homematicip/auth.py`
  - `src/homematicip/connection/rest_connection.py`
- Summary:
  - Auth flows log raw `RestResult` objects and request/response details.
  - Error logging includes full response bodies and request payloads.
  - Current redaction only handles a top-level `id`, so tokens, PINs, client IDs, and access point identifiers can leak into logs.
- Status:
  - Addressed in the current PR by adding recursive redaction and replacing raw auth-result logging with status-only logs.

### 2. Websocket connection state checks use method objects instead of booleans

- Severity: High
- Area: Correctness / Maintainability
- Files:
  - `src/homematicip/async_home.py`
- Summary:
  - `enable_events()` checks `self._websocket_client.is_connected` instead of `is_connected()`.
  - `websocket_is_connected()` returns the bound method object instead of a boolean.
  - This can suppress reconnect attempts and mislead callers about actual websocket state.
- Status:
  - Not started.

### 3. Rate limiter is not concurrency-safe and adds unnecessary latency

- Severity: Medium
- Area: Efficiency / Correctness
- Files:
  - `src/homematicip/connection/buckets.py`
- Summary:
  - `wait_and_take()` mutates token state without holding the lock used by `take()`.
  - Concurrent callers can oversubscribe the bucket.
  - The fixed 1-second polling interval is coarse and increases avoidable wait time.
- Status:
  - Not started.

### 4. One bad device payload can abort the entire device refresh

- Severity: Medium
- Area: Reliability / Maintainability
- Files:
  - `src/homematicip/async_home.py`
- Summary:
  - `_get_devices()` stops processing all remaining devices after the first parse/update exception.
  - That can leave the in-memory state partially updated without surfacing a failure to the caller.
- Status:
  - Not started.

### 5. Broad exception fallbacks hide programming bugs as “unknown type” cases

- Severity: Medium
- Area: Maintainability
- Files:
  - `src/homematicip/async_home.py`
- Summary:
  - Device, rule, and group parsing use broad `except` fallbacks.
  - This masks genuine implementation errors like `KeyError`, `TypeError`, and mapping bugs.
- Status:
  - Not started.

### 6. HTTP client reuse and SSL behavior are inconsistent with the public API

- Severity: Low
- Area: Efficiency / Security / Maintainability
- Files:
  - `src/homematicip/connection/rest_connection.py`
  - `src/homematicip/connection/connection_url_resolver.py`
  - `src/homematicip/connection/websocket_handler.py`
- Summary:
  - A new `httpx.AsyncClient` is created per request when no session is injected, which loses pooling benefits.
  - The documented `enforce_ssl=False` behavior does not match implementation.
  - Websocket SSL setup uses `ssl_ctx` directly and does not follow the same verification semantics as the REST path.
- Status:
  - Not started.
