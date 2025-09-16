from django.core.management.base import BaseCommand
from places.models import Place

class Command(BaseCommand):
    def handle(self, *args, **options):
        places = [
            {'name': 'City Hospital', 'address': '123 Main St, Anytown', 'category': 'hospital', 'tags': 'ER, ICU'},
            # Add more sample data
        ]
        for data in places:
            Place.objects.get_or_create(name=data['name'], defaults=data)
        self.stdout.write('Seeded places')