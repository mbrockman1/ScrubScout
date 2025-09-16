from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Review
from places.models import Place

@receiver([post_save, post_delete], sender=Review)
def update_place_stats(sender, instance, **kwargs):
    place = instance.place
    reviews = place.reviews.all()
    place.review_count = reviews.count()
    if reviews:
        place.average_rating = sum(r.rating for r in reviews) / place.review_count
    else:
        place.average_rating = 0.00
    place.save(update_fields=['average_rating', 'review_count'])