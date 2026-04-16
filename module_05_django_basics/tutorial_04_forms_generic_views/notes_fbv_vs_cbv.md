# Function-Based Views vs Class-Based Views

## When to use FBV (Function-Based Views)
- Simple, one-off views
- Complex logic that doesn't fit standard patterns
- When you need full control over the request/response cycle

## When to use CBV (Class-Based Views)
- Standard CRUD operations (List, Detail, Create, Update, Delete)
- When you want to reuse logic via mixins
- When following DRY principles

## Generic Views Used
| Generic View | Replaces | Purpose |
|---|---|---|
| ListView | Manual queryset + render | Display list of objects |
| DetailView | get_object_or_404 + render | Display single object |
| CreateView | Form handling + save | Create new object |
| UpdateView | Form + existing object | Edit existing object |
| DeleteView | Confirm + delete | Delete object |

## Key Differences
- FBV uses `question_id` parameter → CBV uses `pk`
- FBV: explicit render() call → CBV: automatic template rendering
- CBV methods: get_queryset(), get_context_data(), get_object()