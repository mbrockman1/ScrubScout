import os
import sys
from django.core.management.base import BaseCommand
from django.utils.text import slugify
from places.models import Place
import pandas as pd

def get_unique_slug(base_slug, model_class=Place):
    """
    Generate a unique slug by appending -1, -2, etc. if it exists.
    """
    unique_slug = base_slug
    counter = 1
    while model_class.objects.filter(slug=unique_slug).exists():
        unique_slug = f"{base_slug}-{counter}"
        counter += 1
    return unique_slug

class Command(BaseCommand):
    help = 'Import hospitals from Excel sheet into Place model'

    def add_arguments(self, parser):
        parser.add_argument('excel_file', type=str, help='Path to Excel file (e.g., hospitals.xlsx)')

    def handle(self, *args, **options):
        excel_path = options['excel_file']
        if not os.path.exists(excel_path):
            self.stdout.write(self.style.ERROR(f'File not found: {excel_path}'))
            return

        try:
            # Read Excel (assumes first sheet; adjust sheet_name if needed)
            df = pd.read_excel(excel_path)
            self.stdout.write(f'Loaded {len(df)} rows from {excel_path}')

            created = 0
            updated = 0
            skipped = 0

            for index, row in df.iterrows():
                facility_id = str(row.get('Facility ID', '')).strip()
                name = str(row.get('Facility Nam', row.get('Facility Name', ''))).strip()  # Handle typo
                if not name:
                    skipped += 1
                    self.stdout.write(self.style.WARNING(f'Skipped row {index + 1}: Empty name'))
                    continue

                # Check for existing by facility_id or name
                place, created_new = Place.objects.get_or_create(
                    facility_id=facility_id if facility_id else None,
                    defaults={
                        'name': name,
                        'address': f"{row.get('Address', '')}, {row.get('City/Town', '')}, {row.get('State', '')} {row.get('ZIP Code', '')}".strip(', '),
                        'city': str(row.get('City/Town', '')).strip(),
                        'state': str(row.get('State', '')).strip(),
                        'zip_code': str(row.get('ZIP Code', '')).strip(),
                        'phone': str(row.get('Telephone Number', '')).strip(),
                        'category': str(row.get('Hospital Type', 'Hospital')).strip(),
                        'tags': f"{row.get('Hospital Ownership', '')},{row.get('Emergency Services', '')}".strip(',').replace(' ', '').replace('Yes', 'ER').replace('No', ''),
                        'description': f"Hospital in {row.get('County/Parish', 'Unknown County')} providing {row.get('Hospital Type', 'general services.')}",
                        # Slug will be set in save() override or here
                    }
                )

                if created_new:
                    # Generate unique slug
                    base_slug = slugify(name)
                    place.slug = get_unique_slug(base_slug)
                    place.save()
                    created += 1
                else:
                    # Update existing (optional; comment out if you don't want overwrites)
                    place.address = f"{row.get('Address', place.address)}, {row.get('City/Town', place.city)}, {row.get('State', place.state)} {row.get('ZIP Code', place.zip_code)}".strip(', ')
                    place.phone = str(row.get('Telephone Number', place.phone)).strip()
                    # Regenerate slug if name changed (optional)
                    base_slug = slugify(place.name)  # Use updated name
                    place.slug = get_unique_slug(base_slug)
                    place.save()
                    updated += 1

                if (index + 1) % 100 == 0:  # Progress every 100 rows
                    self.stdout.write(f'Processed {index + 1} rows...')

            self.stdout.write(
                self.style.SUCCESS(
                    f'Import complete! Created: {created}, Updated: {updated}, Skipped: {skipped}. Total places: {Place.objects.count()}'
                )
            )

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error importing: {str(e)}'))
            import traceback
            self.stdout.write(traceback.format_exc())  # Better error details
            sys.exit(1)