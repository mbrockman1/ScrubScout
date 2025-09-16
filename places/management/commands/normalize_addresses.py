from django.core.management.base import BaseCommand
from places.models import Place
from django.utils.text import slugify


class Command(BaseCommand):
    help = 'Normalize addresses and other text fields to title case'

    def handle(self, *args, **options):
        updated = 0
        for place in Place.objects.all():
            old_address = place.address
            old_name = place.name

            # Normalize name
            place.name = place.name.title()

            # Normalize address components (split, title, rejoin)
            if place.address:
                # Simple split by comma, title each part, rejoin
                parts = [part.strip().title() for part in place.address.split(',')]
                # Ensure state (last non-empty part before ZIP) is uppercase if it's 2 letters
                if len(parts) > 2 and len(parts[-3].strip()) == 2:  # e.g., "CA" before ZIP
                    parts[-3] = parts[-3].upper()
                place.address = ', '.join(parts)

            # Other fields
            place.city = place.city.title() if place.city else ''
            place.category = place.category.title() if place.category else 'Hospital'
            place.description = place.description.title() if place.description else ''

            # Tags: Lowercase for consistency
            if place.tags:
                place.tags = ','.join([tag.strip().lower() for tag in place.tags.split(',') if tag.strip()])

            # Regenerate unique slug if name changed
            if place.name != old_name:
                from .import_places import get_unique_slug  # Import the helper
                base_slug = slugify(place.name)
                place.slug = get_unique_slug(base_slug)

            place.save(update_fields=['name', 'address', 'city', 'category', 'description', 'tags', 'slug'])
            updated += 1

            if updated % 500 == 0:
                self.stdout.write(f'Normalized {updated} places...')

        self.stdout.write(self.style.SUCCESS(f'Normalization complete! Updated {updated} places.'))