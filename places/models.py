from django.db import models
from django.utils.text import slugify

class Place(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    category = models.CharField(max_length=100, choices=[('hospital', 'Hospital'), ('clinic', 'Clinic'), ('therapy_center', 'Therapy Center')])  # Customize choices
    tags = models.CharField(max_length=200, blank=True)  # Comma-separated
    address = models.TextField()
    phone = models.CharField(max_length=20, blank=True)
    url = models.URLField(blank=True)
    average_rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)
    review_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    @property
    def rating_display(self):
        return f"{self.average_rating}/5.0"  # For templates
    
    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('place_detail', kwargs={'slug': self.slug})