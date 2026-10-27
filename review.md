# Code Review Findings

This file tracks the current review findings so we can work them down one by one without losing context.

## Open

### 1. Broad exception fallbacks hide programming bugs as “unknown type” cases

- Severity: Medium
- Area: Maintainability
- Files:
  - `src/homematicip/async_home.py`
- Summary:
  - Device, rule, and group parsing use broad `except` fallbacks.
  - This masks genuine implementation errors like `KeyError`, `TypeError`, and mapping bugs.
- Status:
  - Not started.

## Done

- Sensitive data in logs: recursive redaction, status-only auth logging (#644).
- Websocket state checks call `is_connected()`.
- Rate limiter holds the lock in `wait_and_take()`.
- One bad device payload no longer aborts the device refresh (#733).
- SSL: a CA path in `ssl_ctx` becomes an `SSLContext`, and REST, URL lookup and websocket resolve it the same way (#734). A new `httpx.AsyncClient` per request only happens without an injected session; Home Assistant injects one.
