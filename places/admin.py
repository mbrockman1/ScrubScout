from django.contrib import admin
from .models import Place
import csv
from django.http import HttpResponse
from django.urls import path

@admin.register(Place)
class PlaceAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'category', 'state', 'phone', 'facility_id', 'average_rating', 'review_count']
    list_filter = ('category', 'state')
    search_fields = ['name', 'address']

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('import-csv/', self.import_csv, name='import_csv'),
        ]
        return custom_urls + urls

    def import_csv(self, request):
        if request.method == 'POST':
            csv_file = request.FILES['file']
            decoded_file = csv_file.read().decode('utf-8').splitlines()
            reader = csv.DictReader(decoded_file)
            for row in reader:
                Place.objects.update_or_create(name=row['name'], defaults=row)
            self.message_user(request, 'Import successful')
        return render(request, 'admin/import_csv.html', {})