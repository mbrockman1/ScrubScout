from django.contrib import admin
# from reviews.models import Review

# @admin.action(description='Hide selected reviews')
# def hide_reviews(modeladmin, request, queryset):
#     queryset.update(is_hidden=True)

# @admin.action(description='Unhide selected reviews')
# def unhide_reviews(modeladmin, request, queryset):
#     queryset.update(is_hidden=False)

# class ReviewAdmin(admin.ModelAdmin):
#     actions = [hide_reviews, unhide_reviews]
#     list_display = ('title', 'author', 'is_hidden')

# admin.site.register(Review, ReviewAdmin)