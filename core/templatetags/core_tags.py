from django import template
from datetime import datetime

register = template.Library()

@register.filter
def star_rating(rating):
    stars = '★' * int(rating)
    return f"{stars} ({rating})"

@register.filter
def time_ago(value):
    now = datetime.now()
    delta = now - value
    if delta.days == 0:
        return f"{delta.seconds // 3600}h ago"
    return f"{delta.days}d ago"