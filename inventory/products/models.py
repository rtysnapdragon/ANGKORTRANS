
from django.db import models
from django.core.validators import MinValueValidator
from accounts.users.models import ( User)

class Product(models.Model):
    ID = models.AutoField(primary_key=True, db_column='ID')
    CODE = models.CharField(max_length=30, unique=True, db_column='CODE')
    NAME = models.CharField(max_length=150, db_column='NAME')
    CATEGORY = models.CharField(max_length=50, null=True, blank=True, db_column='CATEGORY')
    UNIT = models.CharField(max_length=20, default='PCS', db_column='UNIT')
    PURCHASE_PRICE = models.DecimalField(max_digits=15, decimal_places=2, db_column='PURCHASE_PRICE')
    SALE_PRICE = models.DecimalField(max_digits=15, decimal_places=2, db_column='SALE_PRICE')
    CURRENT_STOCK = models.IntegerField(default=0, validators=[MinValueValidator(0)], db_column='CURRENT_STOCK')
    MIN_STOCK = models.IntegerField(default=10, db_column='MIN_STOCK')
    
    # Audit Fields
    CREATED_BY = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='product_created', db_column='CREATED_BY')
    CREATED_AT = models.DateTimeField(auto_now_add=True, db_column='CREATED_AT')
    UPDATED_BY = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='product_updated', db_column='UPDATED_BY')
    UPDATED_AT = models.DateTimeField(auto_now=True, db_column='UPDATED_AT')

    class Meta:
        db_table = 'PRODUCT'

    def __str__(self):
        return f"{self.CODE} - {self.NAME}"


# ====================== PRODUCT DETAIL MODEL (New) ======================
class ProductDetail(models.Model):
    ID = models.AutoField(primary_key=True, db_column='ID')
    PRODUCT_ID = models.OneToOneField(
        'Product', 
        on_delete=models.CASCADE, 
        related_name='product_detail',
        db_column='PRODUCT_ID'
    )
    
    # Extended product information
    DESCRIPTION = models.TextField(null=True, blank=True, db_column='DESCRIPTION')
    SPECIFICATIONS = models.JSONField(null=True, blank=True, db_column='SPECIFICATIONS')  # e.g., {"color": "red", "weight": "5kg"}
    IMAGE_URL = models.URLField(max_length=500, null=True, blank=True, db_column='IMAGE_URL')
    BARCODE = models.CharField(max_length=100, null=True, blank=True, unique=True, db_column='BARCODE')
    LOCATION = models.CharField(max_length=50, null=True, blank=True, db_column='LOCATION')  # Warehouse location
    EXPIRY_DATE = models.DateField(null=True, blank=True, db_column='EXPIRY_DATE')
    NOTES = models.TextField(null=True, blank=True, db_column='NOTES')
    
    # Audit Fields
    CREATED_BY = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='product_detail_created', db_column='CREATED_BY')
    CREATED_AT = models.DateTimeField(auto_now_add=True, db_column='CREATED_AT')
    UPDATED_BY = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='product_detail_updated', db_column='UPDATED_BY')
    UPDATED_AT = models.DateTimeField(auto_now=True, db_column='UPDATED_AT')

    class Meta:
        db_table = 'PRODUCT_DETAIL'

    def __str__(self):
        return f"Details for {self.PRODUCT.CODE}"