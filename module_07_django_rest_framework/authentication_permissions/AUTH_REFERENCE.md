# Authentication & Security Reference

## Auth Flow Comparison
| Method | Header | Stateless | Best For |
|---|---|---|---|
| Session | Cookie | No | Web apps with templates |
| Token | `Token <key>` | Yes | Simple APIs |
| JWT | `Bearer <token>` | Yes | SPAs, mobile apps |

## JWT Flow