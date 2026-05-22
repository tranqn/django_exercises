# DRF Advanced Features

## Pagination Types
| Type | Best For | Query Param |
|---|---|---|
| PageNumber | Traditional pages | `?page=2` |
| LimitOffset | Flexible ranges | `?limit=10&offset=20` |
| Cursor | Infinite scroll, real-time | `?cursor=abc123` |

## Filter Backends
| Backend | Purpose | Query |
|---|---|---|
| DjangoFilterBackend | Field-based filtering | `?seller=1&city=Berlin` |
| SearchFilter | Full-text search | `?search=django` |
| OrderingFilter | Dynamic sorting | `?ordering=-name` |

## Throttle Rates
| Scope | Format | Example |
|---|---|---|
| anon | `N/period` | `100/day` |
| user | `N/period` | `1000/day` |

## ViewSet Actions
| Action | HTTP | URL |
|---|---|---|
| list | GET | `/items/` |
| create | POST | `/items/` |
| retrieve | GET | `/items/{id}/` |
| update | PUT | `/items/{id}/` |
| partial_update | PATCH | `/items/{id}/` |
| destroy | DELETE | `/items/{id}/` |
| @action | custom | `/items/{id}/action/` |