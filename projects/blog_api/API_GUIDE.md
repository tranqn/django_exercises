# Blog API — Usage Guide

## Auth
Obtain a token, then send it on each request:
    POST /api-token-auth/   {"username": "...", "password": "..."}
    Authorization: Token <key>

## Posts
    GET    /api/posts/                 list published posts (paginated)
    POST   /api/posts/                 create (auth required)
    GET    /api/posts/{slug}/          retrieve
    PUT    /api/posts/{slug}/          update (author only)
    DELETE /api/posts/{slug}/          delete (author only)

## Filtering & search
    /api/posts/?status=published
    /api/posts/?category=django&tag=orm
    /api/posts/?search=migrations
    /api/posts/?ordering=-created

## Comments
    GET  /api/posts/{slug}/comments/   list
    POST /api/posts/{slug}/comments/   add (auth required)

## Exercises
1. Add a "like" action to PostViewSet using @action(detail=True).
2. Annotate each post with a reading time computed from word count.
3. Restrict comment deletion to the comment author.
4. Switch the comments endpoint to cursor pagination.