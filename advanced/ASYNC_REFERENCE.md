# Async & Real-time Architecture

## When to Use What
| Need | Solution |
|---|---|
| Background email/report | Celery task |
| Scheduled cleanup | Celery Beat |
| Real-time chat | Django Channels + WebSocket |
| Live notifications | Django Channels |
| Concurrent API calls | async view + httpx |
| Long-running API request | Celery + status polling |

## Celery Commands