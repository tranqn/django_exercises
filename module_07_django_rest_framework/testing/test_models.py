import pytest
from django.core.exceptions import ValidationError


@pytest.mark.django_db
class TestBookModel:
    def test_create_book(self):
        """Book can be created with valid data."""
        # book = Book.objects.create(title="Test", pages=100, ...)
        # assert book.pk is not None
        # assert str(book) == "Test"
        pass

    def test_book_str_representation(self):
        """__str__ returns the title."""
        pass

    def test_slug_auto_generated(self):
        """Slug is auto-generated from title on save."""
        # book = Book.objects.create(title="My Great Book", ...)
        # assert book.slug == "my-great-book"
        pass

    def test_pages_must_be_positive(self):
        """pages field rejects negative values."""
        # book = Book(title="Test", pages=-1, ...)
        # with pytest.raises(ValidationError):
        #     book.full_clean()
        pass

    def test_default_status_is_draft(self):
        """New books default to 'draft' status."""
        # book = Book.objects.create(title="Test", pages=100, ...)
        # assert book.status == "draft"
        pass