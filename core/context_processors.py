from .templatetags import core_tags  # For global tags

def site_globals(request):
    return {
        'site_name': 'ScrubScout',
        'nav_items': [('Home', '/'), ('Search', '/'), ('Profile', '/accounts/profile/')],
    }