from django.db import models
from django.conf import settings

# ====================== COUNTRY ======================
class Country(models.Model):
    ID = models.AutoField(primary_key=True, db_column='ID')
    CODE = models.CharField(max_length=2, unique=True, db_column='CODE')
    CODE3 = models.CharField(max_length=3, null=True, blank=True, db_column='CODE3')
    NAME_EN = models.CharField(max_length=100, db_column='NAME_EN')
    NAME_KH = models.CharField(max_length=100, null=True, blank=True, db_column='NAME_KH')
    NATIONALITY_EN = models.CharField(max_length=100, null=True, blank=True, db_column='NATIONALITY_EN')
    NATIONALITY_KH = models.CharField(max_length=100, null=True, blank=True, db_column='NATIONALITY_KH')
    PHONE_CODE = models.CharField(max_length=10, null=True, blank=True, db_column='PHONE_CODE')
    CURRENCY_CODE = models.CharField(max_length=3, null=True, blank=True, db_column='CURRENCY_CODE')
    ISO_NAME = models.CharField(max_length=100, null=True, blank=True)
    ISO_NUMERIC = models.CharField(max_length=3, null=True, blank=True)
    
    CAPITAL_CITY = models.CharField(max_length=100, null=True, blank=True)

    TIMEZONE = models.CharField(max_length=50, null=True, blank=True)
    
    CURRENCY_NAME = models.CharField(max_length=50, null=True, blank=True)
    CURRENCY_SYMBOL = models.CharField(max_length=10, null=True, blank=True)

    LATITUDE = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    LONGITUDE = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)

    FLAG_URL = models.URLField(null=True, blank=True)

    SORT_ORDER = models.IntegerField(default=0)

    IS_ACTIVE = models.BooleanField(default=True, db_column='IS_ACTIVE')

    CREATED_BY = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, db_column='CREATED_BY', related_name="%(class)s_created")
    CREATED_AT = models.DateTimeField(auto_now_add=True, db_column='CREATED_AT')
    UPDATED_BY = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, db_column='UPDATED_BY', related_name="%(class)s_updated")
    UPDATED_AT = models.DateTimeField(auto_now=True, db_column='UPDATED_AT')

    class Meta:
        db_table = 'COUNTRY'

    def __str__(self):
        return self.NAME_EN


# ====================== PROVINCE ======================
class Province(models.Model):
    ID = models.AutoField(primary_key=True, db_column='ID')
    CODE = models.CharField(max_length=10, unique=True, db_column='CODE')
    CODE2 = models.CharField(max_length=10, null=True, blank=True)
    NAME_KH = models.CharField(max_length=100, db_column='NAME_KH')
    NAME_EN = models.CharField(max_length=100, db_column='NAME_EN')
    REGION = models.CharField(max_length=50, null=True, blank=True, db_column='REGION')
    
    POSTAL_CODE_PREFIX = models.CharField(max_length=10, null=True, blank=True)

    LATITUDE = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    LONGITUDE = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)

    IS_CAPITAL = models.BooleanField(default=False)

    IS_ACTIVE = models.BooleanField(default=True)
    SORT_ORDER = models.IntegerField(default=0)

    CREATED_BY = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, db_column='CREATED_BY', related_name="%(class)s_created")
    CREATED_AT = models.DateTimeField(auto_now_add=True, db_column='CREATED_AT')
    UPDATED_BY = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, db_column='UPDATED_BY', related_name="%(class)s_updated")
    UPDATED_AT = models.DateTimeField(auto_now=True, db_column='UPDATED_AT')

    class Meta:
        db_table = 'PROVINCE'


# ====================== DISTRICT ======================
class District(models.Model):
    ID = models.AutoField(primary_key=True, db_column='ID')
    PROVINCE = models.ForeignKey(Province, on_delete=models.CASCADE, db_column='PROVINCE_ID')
    CODE = models.CharField(max_length=20, db_column='CODE')
    NAME_KH = models.CharField(max_length=100, db_column='NAME_KH')
    NAME_EN = models.CharField(max_length=100, db_column='NAME_EN')

    POSTAL_CODE = models.CharField(max_length=20, null=True, blank=True)

    LATITUDE = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    LONGITUDE = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)

    IS_ACTIVE = models.BooleanField(default=True)
    SORT_ORDER = models.IntegerField(default=0)

    CREATED_BY = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, db_column='CREATED_BY', related_name="%(class)s_created")
    CREATED_AT = models.DateTimeField(auto_now_add=True, db_column='CREATED_AT')
    UPDATED_BY = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, db_column='UPDATED_BY', related_name="%(class)s_updated")
    UPDATED_AT = models.DateTimeField(auto_now=True, db_column='UPDATED_AT')

    class Meta:
        db_table = 'DISTRICT'


# ====================== COMMUNE ======================
class Commune(models.Model):
    ID = models.AutoField(primary_key=True, db_column='ID')
    DISTRICT = models.ForeignKey(District, on_delete=models.CASCADE, db_column='DISTRICT_ID')
    CODE = models.CharField(max_length=30, db_column='CODE')
    NAME_KH = models.CharField(max_length=100, db_column='NAME_KH')
    NAME_EN = models.CharField(max_length=100, db_column='NAME_EN')

    POSTAL_CODE = models.CharField(max_length=20, null=True, blank=True)

    LATITUDE = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    LONGITUDE = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)

    IS_ACTIVE = models.BooleanField(default=True)
    SORT_ORDER = models.IntegerField(default=0)

    CREATED_BY = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, db_column='CREATED_BY', related_name="%(class)s_created")
    CREATED_AT = models.DateTimeField(auto_now_add=True, db_column='CREATED_AT')
    UPDATED_BY = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, db_column='UPDATED_BY', related_name="%(class)s_updated")
    UPDATED_AT = models.DateTimeField(auto_now=True, db_column='UPDATED_AT')

    class Meta:
        db_table = 'COMMUNE'


# ====================== VILLAGE ======================
class Village(models.Model):
    ID = models.AutoField(primary_key=True, db_column='ID')
    COMMUNE = models.ForeignKey(Commune, on_delete=models.CASCADE, db_column='COMMUNE_ID')
    CODE = models.CharField(max_length=50, null=True, blank=True, db_column='CODE')
    NAME_KH = models.CharField(max_length=150, db_column='NAME_KH')
    NAME_EN = models.CharField(max_length=150, null=True, blank=True, db_column='NAME_EN')

    POSTAL_CODE = models.CharField(max_length=20, null=True, blank=True)

    LATITUDE = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    LONGITUDE = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)

    POPULATION = models.IntegerField(null=True, blank=True)

    IS_ACTIVE = models.BooleanField(default=True)
    SORT_ORDER = models.IntegerField(default=0)

    CREATED_BY = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, db_column='CREATED_BY', related_name="%(class)s_created")
    CREATED_AT = models.DateTimeField(auto_now_add=True, db_column='CREATED_AT')
    UPDATED_BY = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, db_column='UPDATED_BY', related_name="%(class)s_updated")
    UPDATED_AT = models.DateTimeField(auto_now=True, db_column='UPDATED_AT')

    class Meta:
        db_table = 'VILLAGE'


# ====================== ADMIN ADDRESS (Main Table) ======================
class AdminAddress(models.Model):
    ID = models.AutoField(primary_key=True, db_column='ID')

    COUNTRY_ID = models.ForeignKey(Country, on_delete=models.PROTECT, default=1, db_column='COUNTRY_ID')
    PROVINCE_ID = models.ForeignKey(Province, on_delete=models.PROTECT, db_column='PROVINCE_ID')
    DISTRICT_ID = models.ForeignKey(District, on_delete=models.PROTECT, db_column='DISTRICT_ID')
    COMMUNE_ID = models.ForeignKey(Commune, on_delete=models.PROTECT, db_column='COMMUNE_ID')
    VILLAGE_ID = models.ForeignKey(Village, on_delete=models.SET_NULL, null=True, blank=True, db_column='VILLAGE_ID')

    ADDRESS_LINE1 = models.CharField(max_length=255, db_column='ADDRESS_LINE1')
    ADDRESS_LINE2 = models.CharField(max_length=255, null=True, blank=True, db_column='ADDRESS_LINE2')
    ZIP_CODE = models.CharField(max_length=20, null=True, blank=True, db_column='ZIP_CODE')

    ADDRESS_TYPE = models.CharField(
        max_length=20,
        choices=[('BILLING','Billing'), ('SHIPPING','Shipping'), ('WAREHOUSE','Warehouse'),
                 ('HEAD_OFFICE','Head Office'), ('BRANCH','Branch'), ('OTHER','Other')],
        default='SHIPPING',
        db_column='ADDRESS_TYPE'
    )

    ENTITY_TYPE = models.CharField(
        max_length=20,
        choices=[('CUSTOMER','Customer'), ('SUPPLIER','Supplier'), ('WAREHOUSE','Warehouse'), ('COMPANY','Company')],
        db_column='ENTITY_TYPE'
    )
    ENTITY_ID = models.BigIntegerField(db_column='ENTITY_ID')

    IS_DEFAULT = models.BooleanField(default=False, db_column='IS_DEFAULT')
    IS_ACTIVE = models.BooleanField(default=True, db_column='IS_ACTIVE')

    FULL_ADDRESS = models.TextField(null=True, blank=True)
    ADDRESS_NOTE = models.TextField(null=True, blank=True)

    LATITUDE = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    LONGITUDE = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)

    VERIFIED = models.BooleanField(default=False)
    VERIFIED_AT = models.DateTimeField(null=True, blank=True)
    VERIFIED_BY = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="verified_addresses"
    )

    IS_DELETED = models.BooleanField(default=False)
    DELETED_AT = models.DateTimeField(null=True, blank=True)

    CREATED_BY = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, db_column='CREATED_BY', related_name="%(class)s_created")
    CREATED_AT = models.DateTimeField(auto_now_add=True, db_column='CREATED_AT')
    UPDATED_BY = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, db_column='UPDATED_BY', related_name="%(class)s_updated")
    UPDATED_AT = models.DateTimeField(auto_now=True, db_column='UPDATED_AT')

    class Meta:
        db_table = 'ADMIN_ADDRESS'
        indexes = [
            models.Index(fields=['ENTITY_TYPE', 'ENTITY_ID']),
        ]