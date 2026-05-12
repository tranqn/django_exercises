from django.db import models


class Author(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=300)
    authors = models.ManyToManyField(Author, through="BookAuthor", related_name="books")
    tags = models.ManyToManyField(Tag, blank=True, related_name="books")

    def __str__(self):
        return self.title


class BookAuthor(models.Model):
    ROLE_CHOICES = [
        ("primary", "Primary Author"),
        ("co-author", "Co-Author"),
        ("editor", "Editor"),
        ("translator", "Translator"),
    ]
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="primary")

    class Meta:
        unique_together = [["book", "author", "role"]]

    def __str__(self):
        return f"{self.author.name} — {self.book.title} ({self.get_role_display()})"