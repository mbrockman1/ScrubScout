from django.db.models import Q
from django.shortcuts import render
from places.models import Place

def search_results(request):
    query = request.GET.get('q', '').strip()
    sort = request.GET.get('sort', 'name')
    tags = request.GET.get('tags', '').strip()

    places = Place.objects.all()

    if query:
        places = places.filter(
            Q(name__icontains=query) |
            Q(address__icontains=query) |
            Q(tags__icontains=query)
        )

    if tags:
        for tag in tags.split(','):
            places = places.filter(tags__icontains=tag.strip())

    # Order then slice
    if sort == 'rating':
        places = places.order_by('-average_rating')
    elif sort == 'reviews':
        places = places.order_by('-review_count')
    else:
        places = places.order_by('name')

    places = places[:20]  # Limit for MVP

    context = {
        'places': places,
        'query': query,
        'sort': sort,
        'tags': tags,
        'total_results': Place.objects.count() if not query else places.count(),  # Approximate total
    }

    return render(request, 'search/results.html', context)  # Now renders Yelp-style template