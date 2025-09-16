from django.db.models.signals import post_save
from django.dispatch import receiver
from reviews.models import Review
from .models import CustomUser

@receiver(post_save, sender=Review)
def update_user_review_count(sender, instance, created, **kwargs):
    if created:
        instance.user.review_count += 1
        instance.user.save(update_fields=['review_count'])
    # Note: For deletions, you'd need a post_delete signal, but MVP skips for simplicity