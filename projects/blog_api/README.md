# Blog API — DRF Project

A small but complete REST API for a blog: posts, categories, tags and
comments, with token auth, author-only edit permissions, filtering,
pagination and tests.

## Stack
- Django + Django REST Framework
- django-filter (filtering / search)
- drf-spectacular (OpenAPI schema)

## Layout
    models.py        Post, Category, Tag, Comment
    serializers.py   read / write serializers
    views.py         ModelViewSets
    permissions.py   IsAuthorOrReadOnly
    filters.py       PostFilter
    urls.py          DRF router wiring
    tests.py         API tests