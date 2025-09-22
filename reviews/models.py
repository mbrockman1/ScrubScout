from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator

from places.models import Place

class Review(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="reviews",
    )
    place = models.ForeignKey(
        "places.Place",   # <-- change this string if your Place app label differs
        on_delete=models.CASCADE,
        related_name="reviews",
    )
    rating = models.PositiveSmallIntegerField(
        default=5,
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="1–5",
    )
    title = models.CharField(max_length=200, blank=True)
    body = models.TextField(max_length=1000)
    pay_scale = models.CharField(max_length=100, blank=True, help_text="e.g., $40/hr")
    housing_details = models.TextField(max_length=500, blank=True, help_text="e.g., Stipend or provided")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_hidden = models.BooleanField(default=False)  # For moderator controls

    class Meta:
        ordering = ['-created_at']
        unique_together = ['author', 'place']  # One review per user per place (MVP)
        constraints = [
        models.UniqueConstraint(
            fields=["author", "place"],
            name="unique_author_place_review",
        )
        ]
        indexes = [
            models.Index(fields=["place", "-created_at"]),
        ]

    def __str__(self):
        # Be defensive in case display_name doesn't exist
        u = self.author
        name = getattr(u, "display_name", None) or getattr(u, "username", str(u))
        return f"{name} – {self.title or 'Review'}"