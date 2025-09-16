from django.db import models
from django.utils.text import slugify

class Place(models.Model):
    facility_id = models.CharField(max_length=50, unique=True, blank=True, null=True)  # New
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    address = models.TextField(blank=True)
    city = models.CharField(max_length=100, blank=True)  # New
    state = models.CharField(max_length=2, blank=True)   # New
    zip_code = models.CharField(max_length=10, blank=True)  # New
    phone = models.CharField(max_length=20, blank=True)  # New
    category = models.CharField(max_length=100, default="Hospital")
    tags = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)

    average_rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)
    review_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            self.slug = get_unique_slug(base_slug)  # Add this import: from .management.commands.import_places import get_unique_slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    @property
    def rating_display(self):
        return f"{self.average_rating}/5.0"  # For templates
    
    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('place_detail', kwargs={'slug': self.slug})
    
def get_unique_slug(base_slug, model_class=Place):
    """
    Generate a unique slug by appending -1, -2, etc. if it exists.
    """
    unique_slug = base_slug
    counter = 1
    while model_class.objects.filter(slug=unique_slug).exists():
        unique_slug = f"{base_slug}-{counter}"
        counter += 1
    return unique_slug
