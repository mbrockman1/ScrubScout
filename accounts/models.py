from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import Group, Permission  # Import for explicit field defs
from django.utils.translation import gettext_lazy as _

class CustomUser(AbstractUser):
    display_name = models.CharField(max_length=100, blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    bio = models.TextField(blank=True, max_length=500)
    location = models.CharField(max_length=200, blank=True)
    review_count = models.PositiveIntegerField(default=0)
    join_date = models.DateTimeField(default=timezone.now)

    # FIXED: Override M2M fields with custom related_name to avoid clashes
    groups = models.ManyToManyField(
        Group,
        verbose_name=_('groups'),
        blank=True,
        help_text=_('The groups this user belongs to. A user will get all permissions granted to each of their groups.'),
        related_name='custom_user_set',  # Unique reverse name (avoids 'user_set' clash)
        related_query_name='custom_user',
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=_('user permissions'),
        blank=True,
        help_text=_('Specific permissions for this user.'),
        related_name='custom_user_set',  # Same unique name for consistency
        related_query_name='custom_user',
    )

    def __str__(self):
        return self.username or self.display_name

    class Meta:
        # Optional: Add swappable for advanced use, but not needed for MVP
        swappable = 'AUTH_USER_MODEL'

# Signal to update review_count (connect in apps.py)
from django.db.models.signals import post_save
from django.dispatch import receiver
from reviews.models import Review  # Forward reference; import carefully

@receiver(post_save, sender=Review)
def update_user_review_count(sender, instance, created, **kwargs):
    if created:
        instance.user.review_count += 1
        instance.user.save(update_fields=['review_count'])