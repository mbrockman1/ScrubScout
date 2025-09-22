# reviews/signals.py
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.db.models import Avg, Count

from .models import Review

def _recalc_place_stats(place):
    agg = place.reviews.aggregate(
        avg=Avg("rating"),
        cnt=Count("id"),
    )
    place.average_rating = float(agg["avg"] or 0.0)
    place.review_count = int(agg["cnt"] or 0)
    place.save(update_fields=["average_rating", "review_count"])

def _recalc_user_count(user):
    # Optional: keep a running counter on the user profile if you have one.
    # If you store it on the User model or on a Profile (e.g., accounts.Profile),
    # adjust this function accordingly or remove it entirely.
    if hasattr(user, "review_count"):
        user.review_count = user.reviews.count()
        user.save(update_fields=["review_count"])

@receiver(post_save, sender=Review)
def on_review_saved(sender, instance, **kwargs):
    _recalc_place_stats(instance.place)
    _recalc_user_count(instance.author)

@receiver(post_delete, sender=Review)
def on_review_deleted(sender, instance, **kwargs):
    _recalc_place_stats(instance.place)
    _recalc_user_count(instance.author)