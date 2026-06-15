"""
Django Shell Quick Reference
Run: python manage.py shell

Tip: pip install django-extensions → python manage.py shell_plus
     (auto-imports all models)
"""

# ============================================================
# CRUD Operations
# ============================================================
# CREATE
# obj = Model(field=value)
# obj.save()
# obj = Model.objects.create(field=value)  # create + save

# READ
# Model.objects.all()
# Model.objects.get(pk=1)          # raises DoesNotExist / MultipleObjectsReturned
# Model.objects.filter(field=val)  # returns QuerySet
# Model.objects.first()
# Model.objects.last()
# Model.objects.count()
# Model.objects.exists()

# UPDATE
# obj.field = new_value
# obj.save()
# Model.objects.filter(...).update(field=value)  # bulk update

# DELETE
# obj.delete()
# Model.objects.filter(...).delete()  # bulk delete

# ============================================================
# QuerySet Methods (chainable)
# ============================================================
# .filter()     — include matching
# .exclude()    — exclude matching
# .order_by()   — sort results
# .values()     — return dicts instead of objects
# .values_list() — return tuples
# .distinct()   — remove duplicates
# .only()       — load specific fields
# .defer()      — exclude specific fields
# [:5]          — LIMIT 5

# ============================================================
# Lookups (double underscore)
# ============================================================
# field__exact      field__iexact     (case-insensitive)
# field__contains   field__icontains
# field__startswith field__endswith
# field__gt  field__gte  field__lt  field__lte
# field__in=[1,2,3]
# field__range=(start, end)
# field__isnull=True
# field__year  field__month  field__day
# related__field   (across relationships)