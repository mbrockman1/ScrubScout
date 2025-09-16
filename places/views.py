from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Place

def place_detail(request, slug):
    place = get_object_or_404(Place, slug=slug)
    
    # FIXED: Use 'reviews' (from related_name) instead of 'review_set'
    reviews = place.reviews.all()[:10]  # Limit for MVP
    
    # Calculate stats (signals update these, but verify here)
    review_count = place.review_count
    average_rating = place.average_rating
    
    # Check if user can add a review (no duplicates)
    can_review = False
    if request.user.is_authenticated:
        can_review = not place.reviews.filter(user=request.user).exists()

    context = {
        'place': place,
        'reviews': reviews,
        'review_count': review_count,
        'average_rating': average_rating,
        'can_review': can_review,
    }
    return render(request, 'places/place_detail.html', context)

# Optional: If you want a separate view for listing all places (not needed for MVP, but add if wanted)
# def place_list(request):
#     places = Place.objects.all().order_by('name')
#     return render(request, 'places/place_list.html', {'places': places})