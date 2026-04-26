import csv
import os
from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone
from accounts.users.models import Users

SYSTEM_USER = Users.objects.get(ID=1)

from admin_address.models import (
    Country, Province, District, Commune, Village
)

class Command(BaseCommand):
    help = 'Import official Cambodia administrative data (2025) from MEF CSV files'

    def add_arguments(self, parser):
        parser.add_argument('--country', type=str, help='Path to Country CSV file')
        parser.add_argument('--province', type=str, help='Path to Province CSV file')
        parser.add_argument('--district', type=str, help='Path to District CSV file')
        parser.add_argument('--commune', type=str, help='Path to Commune CSV file')
        parser.add_argument('--village', type=str, help='Path to Village CSV file')
        parser.add_argument('--delete-existing', action='store_true', 
                            help='Delete existing data before import (use with caution)')

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting import of Cambodia administrative data...'))

        try:
            print(" User sysrtem ---------> ", SYSTEM_USER)
            with transaction.atomic():
                if options['delete_existing']:
                    self.stdout.write(self.style.WARNING('Deleting existing administrative data...'))
                    Village.objects.all().delete()
                    Commune.objects.all().delete()
                    District.objects.all().delete()
                    Province.objects.all().delete()
                    Country.objects.all().delete()

                # Import in correct order: Country → Province → District → Commune → Village
                if options['country']:
                    self.import_country(options['country'])

                if options['province']:
                    self.import_province(options['province'])

                if options['district']:
                    self.import_district(options['district'])

                if options['commune']:
                    self.import_commune(options['commune'])

                if options['village']:
                    self.import_village(options['village'])

            self.stdout.write(self.style.SUCCESS('✅ Successfully imported all Cambodia administrative data!'))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'❌ Error during import: {str(e)}'))

    def import_country(self, filepath):
        self.stdout.write(f'Importing Country from {filepath}...')
        with open(filepath, 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            for row in reader:
                Country.objects.update_or_create(
                    COUNTRY_CODE=row.get('country_code') or row.get('code') or row.get('CountryCode'),
                    defaults={
                        'NAME_EN': row.get('country_en') or row.get('name_en') or row.get('CountryNameEn'),
                        'NAME_KH': row.get('country_kh') or row.get('name_kh'),
                        'NATIONALITY_EN': row.get('nationality_en') or row.get('nationality_en'),
                        'NATIONALITY_KH': row.get('nationality_kh') or row.get('nationality_kh'),
                        'PHONE_CODE': row.get('phone_code'),
                        'CURRENCY_CODE': row.get('currency_code'),
                        'CURRENCY_NAME': row.get('currency_name'),
                        'CURRENCY_SYMBOL': row.get('currency_symbol'),
                        'IS_ACTIVE': True,
                        'CREATED_BY': SYSTEM_USER,
                    }
                )
        self.stdout.write(self.style.SUCCESS(f'→ Imported Country data'))

    def import_province(self, filepath):
        self.stdout.write(f'Importing Province from {filepath}...')
        with open(filepath, 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            for row in reader:
                country = Country.objects.get(CODE='KH')
                print(" Country ------------------> ", country)
                print(" Country ID ------------------> ", country.ID)
                Province.objects.update_or_create(
                    COUNTRY_ID=country,
                    CODE=row.get('province_code') or row.get('code'),
                    defaults={
                        'NAME_KH': row.get('province_kh') or row.get('name_kh'),
                        'NAME_EN': row.get('province_en') or row.get('name_en'),
                        'REGION': row.get('region'),
                        'CREATED_BY': SYSTEM_USER,
                    }
                )
        self.stdout.write(self.style.SUCCESS(f'→ Imported Province data'))

    def import_district(self, filepath):
        self.stdout.write(f'Importing District from {filepath}...')
        with open(filepath, 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            for row in reader:
                province_code = row.get('province_code') or row.get('pcode')
                try:
                    province = Province.objects.get(CODE=province_code)
                    District.objects.update_or_create(
                        PROVINCE_ID=province,
                        CODE=row.get('district_code') or row.get('code'),
                        defaults={
                            'NAME_KH': row.get('district_kh') or row.get('name_kh'),
                            'NAME_EN': row.get('district_en') or row.get('name_en'),
                            'CREATED_BY': SYSTEM_USER,
                        }
                    )
                except Province.DoesNotExist:
                    self.stdout.write(self.style.WARNING(f"Province {province_code} not found for district"))
        self.stdout.write(self.style.SUCCESS(f'→ Imported District data'))

    def import_commune(self, filepath):
        self.stdout.write(f'Importing Commune from {filepath}...')
        with open(filepath, 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            for row in reader:
                district_code = row.get('district_code') or row.get('dcode')
                try:
                    district = District.objects.get(CODE=district_code)
                    Commune.objects.update_or_create(
                        DISTRICT_ID=district,
                        CODE=row.get('commune_code') or row.get('code'),
                        defaults={
                            'NAME_KH': row.get('commune_kh') or row.get('name_kh'),
                            'NAME_EN': row.get('commune_en') or row.get('name_en'),
                            'CREATED_BY': SYSTEM_USER,
                        }
                    )
                except District.DoesNotExist:
                    self.stdout.write(self.style.WARNING(f"District {district_code} not found for commune"))
        self.stdout.write(self.style.SUCCESS(f'→ Imported Commune data'))

    def import_village(self, filepath):
        self.stdout.write(f'Importing Village from {filepath}... (this may take a while)')
        count = 0
        with open(filepath, 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            for row in reader:
                commune_code = row.get('commune_code') or row.get('ccode')
                try:
                    commune = Commune.objects.get(CODE=commune_code)
                    Village.objects.update_or_create(
                        COMMUNE_ID=commune,
                        CODE=row.get('village_code') or row.get('code'),
                        defaults={
                            'NAME_KH': row.get('village_kh') or row.get('name_kh'),
                            'NAME_EN': row.get('village_en') or row.get('name_en'),
                            'CREATED_BY': SYSTEM_USER,
                        }
                    )
                    count += 1
                    if count % 5000 == 0:
                        self.stdout.write(f'   Imported {count} villages...')
                except Commune.DoesNotExist:
                    pass  # Skip if commune not found
        self.stdout.write(self.style.SUCCESS(f'→ Imported {count} Village records'))


"""Run commands
python manage.py import_cambodia_admin `
  --province admin_address/management/data/CambodiaProvinceList2025.csv `
  --district admin_address/management/data/CambodiaDistrictList2025.csv `
  --commune admin_address/management/data/CambodiaCommuneList2025.csv `
  --village admin_address/management/data/CambodiaVillagesList2025.csv

python manage.py import_cambodia_admin \
  --province /path/to/CambodiaProvinceList2025.csv \
  --district /path/to/CambodiaDistrictList2025.csv \
  --commune /path/to/CambodiaCommuneList2025.csv \
  --village /path/to/CambodiaVillagesList2025.csv

python manage.py import_cambodia_admin \
  --province ... --district ... --commune ... --village ... \
  --delete-existing
"""