import pytest


@pytest.mark.django_db
class TestBookAuthorRelationship:
    def test_author_has_books(self):
        """Author.books returns related books."""
        # author = Author.objects.create(name="Max", email="max@test.com")
        # Book.objects.create(title="Book 1", author=author, ...)
        # assert author.books.count() == 1
        pass

    def test_cascade_delete(self):
        """Deleting author deletes related books (CASCADE)."""
        # author = Author.objects.create(...)
        # Book.objects.create(title="Book", author=author, ...)
        # author.delete()
        # assert Book.objects.count() == 0
        pass

    def test_m2m_categories(self):
        """Book can have multiple categories."""
        # book = Book.objects.create(...)
        # cat1 = Category.objects.create(name="Fiction", slug="fiction")
        # cat2 = Category.objects.create(name="Science", slug="science")
        # book.categories.add(cat1, cat2)
        # assert book.categories.count() == 2
        pass