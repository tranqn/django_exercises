from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator


class Review(models.Model):
    book = models.ForeignKey("Book", on_delete=models.CASCADE, related_name="reviews")
    reviewer_name = models.CharField(max_length=100)
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField()
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        unique_together = [["book", "reviewer_name"]]

    def __str__(self):
        return f"{self.reviewer_name}: {self.rating}/5 for {self.book.title}"

    def clean(self):
        if self.rating and self.rating <= 2 and len(self.comment.strip()) < 20:
            raise ValidationError(
                {"comment": "Please provide at least 20 characters for low ratings."}
            )