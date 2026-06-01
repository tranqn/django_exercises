"""
Django Async Views (Django 4.1+)

Async views run in an async context, useful for I/O-bound operations.
"""

import asyncio
import httpx
from django.http import JsonResponse


async def async_home(request):
    """Simple async view."""
    return JsonResponse({"message": "Hello from async view!"})


async def fetch_external_data(request):
    """Fetch data from external APIs concurrently."""
    async with httpx.AsyncClient() as client:
        # Run multiple API calls concurrently
        results = await asyncio.gather(
            client.get("https://api.example.com/data1"),
            client.get("https://api.example.com/data2"),
        )

    return JsonResponse({
        "data1": results[0].json() if results[0].status_code == 200 else None,
        "data2": results[1].json() if results[1].status_code == 200 else None,
    })


# Async ORM operations (Django 4.1+)
# async def async_book_list(request):
#     books = [book async for book in Book.objects.all()]
#     data = [{"title": b.title, "pages": b.pages} for b in books]
#     return JsonResponse(data, safe=False)
#
# book = await Book.objects.aget(pk=1)
# exists = await Book.objects.filter(status="published").aexists()
# count = await Book.objects.acount()