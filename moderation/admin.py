from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.conf import settings
from reviews.models import Review
from .models import ContentReport, ModerationAction
from accounts.models import CustomUser  # Import CustomUser explicitly

@admin.action(description='Hide selected reviews')
def hide_reviews(modeladmin, request, queryset):
    queryset.update(is_hidden=True)
    for review in queryset:
        ModerationAction.objects.create(
            staff=request.user,
            review=review,
            action='hidden',
            notes='Hidden via admin action'
        )

@admin.action(description='Unhide selected reviews')
def unhide_reviews(modeladmin, request, queryset):
    queryset.update(is_hidden=False)
    for review in queryset:
        ModerationAction.objects.create(
            staff=request.user,
            review=review,
            action='restored',
            notes='Restored via admin action'
        )

@admin.action(description='Delete selected reviews')
def delete_reviews(modeladmin, request, queryset):
    for review in queryset:
        ModerationAction.objects.create(
            staff=request.user,
            review=review,
            action='deleted',
            notes='Deleted via admin action'
        )
        review.delete()

class ReviewAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'place', 'is_hidden', 'created_at')
    list_filter = ('is_hidden', 'created_at')
    actions = [hide_reviews, unhide_reviews, delete_reviews]
    search_fields = ('title', 'author__display_name', 'place__name')

class ContentReportAdmin(admin.ModelAdmin):
    list_display = ('review', 'reporter', 'reason', 'is_resolved', 'created_at')
    list_filter = ('reason', 'is_resolved')
    actions = ['mark_resolved']

    @admin.action(description='Mark reports as resolved')
    def mark_resolved(self, request, queryset):
        queryset.update(is_resolved=True)

class ModerationActionAdmin(admin.ModelAdmin):
    list_display = ('action', 'staff', 'review', 'created_at')
    list_filter = ('action',)

admin.site.register(Review, ReviewAdmin)
admin.site.register(ContentReport, ContentReportAdmin)
admin.site.register(ModerationAction, ModerationActionAdmin)

# Customize User admin for deactivation
class CustomUserAdmin(UserAdmin):
    actions = ['deactivate_users', 'reactivate_users']

    @admin.action(description='Deactivate selected users')
    def deactivate_users(self, request, queryset):
        queryset.update(is_active=False)

    @admin.action(description='Reactivate selected users')
    def reactivate_users(self, request, queryset):
        queryset.update(is_active=True)

# Unregister and re-register CustomUser
admin.site.unregister(CustomUser)  # Use CustomUser model class
admin.site.register(CustomUser, CustomUserAdmin)