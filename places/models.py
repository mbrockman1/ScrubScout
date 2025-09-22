from django.db import models
from django.utils.text import slugify
from django.urls import reverse

class Place(models.Model):
    facility_id = models.CharField(max_length=50, unique=True, blank=True, null=True)
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    address = models.TextField(blank=True)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=2, blank=True)
    zip_code = models.CharField(max_length=10, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    category = models.CharField(max_length=100, default="Hospital")
    tags = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)

    average_rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)
    review_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name or "")
            self.slug = _get_unique_slug(base_slug, self.__class__)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    @property
    def rating_display(self):
        return f"{self.average_rating}/5.0"

    def get_absolute_url(self):
        # Namespaced reverse to match scrubscout/urls.py include
        return reverse("places:place_detail", kwargs={"slug": self.slug})


def _get_unique_slug(base_slug: str, model_class):
    """
    Generate a unique slug by appending -1, -2, etc. if it exists.
    """
    if not base_slug:
        base_slug = "place"
    unique_slug = base_slug
    counter = 1
    while model_class.objects.filter(slug=unique_slug).exists():
        unique_slug = f"{base_slug}-{counter}"
        counter += 1
    return unique_slug