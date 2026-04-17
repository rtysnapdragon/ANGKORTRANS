import csv
from django.core.management.base import BaseCommand
from django.db import transaction
from inventory.address.models import (
    Country, Province, District, Commune, Village
)

class Command(BaseCommand):
    help = 'Import official Cambodia administrative data from MEF CSV files'

    def add_arguments(self, parser):
        parser.add_argument('--country', type=str, help='Path to Country CSV')
        parser.add_argument('--province', type=str, help='Path to Province CSV')
        parser.add_argument('--district', type=str, help='Path to District CSV')
        parser.add_argument('--commune', type=str, help='Path to Commune CSV')
        parser.add_argument('--village', type=str, help='Path to Village CSV')

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting import of Cambodia administrative data...'))

        try:
            with transaction.atomic():
                # 1. Country (usually just Cambodia)
                if options['country']:
                    self.import_country(options['country'])

                # 2. Province
                if options['province']:
                    self.import_province(options['province'])

                # 3. District
                if options['district']:
                    self.import_district(options['district'])

                # 4. Commune
                if options['commune']:
                    self.import_commune(options['commune'])

                # 5. Village (largest file)
                if options['village']:
                    self.import_village(options['village'])

            self.stdout.write(self.style.SUCCESS('Successfully imported all administrative data!'))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error during import: {str(e)}'))

    def import_country(self, filepath):
        with open(filepath, 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            for row in reader:
                Country.objects.update_or_create(
                    COUNTRY_CODE=row.get('country_code') or row.get('code'),
                    defaults={
                        'COUNTRY_NAME_EN': row.get('country_name_en') or row.get('name_en'),
                        'COUNTRY_NAME_KH': row.get('country_name_kh') or row.get('name_kh'),
                        'PHONE_CODE': row.get('phone_code'),
                        'CURRENCY_CODE': row.get('currency_code'),
                        'CREATED_BY': 1,   # Change to your admin user ID
                    }
                )

    # Similar methods for Province, District, Commune, Village...
    # (I can expand them if you want full code)

    def import_province(self, filepath):
        # Similar logic using update_or_create with PROVINCE_CODE as key
        pass   # I'll provide full version if needed

    # ... (add the other methods similarly)



"""
    Step 4: Run the Command
Example usage:
Bashpython manage.py import_cambodia_admin \
  --province path/to/CambodiaProvinceList2025.csv \
  --district path/to/CambodiaDistrictList2025.csv \
  --commune path/to/CambodiaCommuneList2025.csv \
  --village path/to/CambodiaVillagesList2025.csv

"""