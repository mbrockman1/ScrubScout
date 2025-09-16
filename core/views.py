from django.shortcuts import render
from places.models import Place  # For top samples

def home(request):
    # Top 3 places for samples (like before)
    top_places = Place.objects.order_by('-review_count')[:3]
    context = {
        'top_places': top_places,
    }
    return render(request, 'core/home.html', context)