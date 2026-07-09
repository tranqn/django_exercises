# Advanced ORM Reference

Beyond basic .filter()/.get(): tools from the database-access docs.

## Reading & Aggregating
| Need | Tool |
|---|---|
| Stats over a queryset | aggregate(Avg, Sum, Count, Max) |
| Per-row computed field | annotate(...) |
| Group by | values(...).annotate(...) |
| Reference a column | F("price") * 1.1 |
| If/else in SQL | Case(When(...), default=...) |
| First non-null | Coalesce(a, b) |

## Writing Safely
- Wrap multi-step writes in transaction.atomic().
- Lock contended rows with select_for_update().
- Defer side effects with transaction.on_commit().

## Performance
- select_related (FK JOIN) and prefetch_related (M2M / reverse).
- bulk_create / bulk_update for batches.
- values() / values_list() / iterator() for large read-only scans.
- Add indexes (db_index, Meta.indexes) on hot filter/order fields.

## Postgres Extras
- ArrayField, JSONField, full-text search (SearchVector / SearchRank).
- GinIndex for array, JSON and search columns.

## Exercises
1. Annotate each author with their book count and average rating.
2. Tier customers gold/silver/bronze with Case/When in one query.
3. Wrap a money transfer in an atomic block with select_for_update.
4. Replace an N+1 loop with select_related; prove it with assert_max_queries.
5. Add a Postgres full-text search across title + body, ranked by relevance.