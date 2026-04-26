from django.db import models
from accounts.users.models import ( Users)
from inventory.suppliers.models import ( Supplier)
from inventory.products.models import Product
from django.conf import settings

class Purchase(models.Model):
    ID = models.AutoField(primary_key=True, db_column='ID')
    CODE = models.CharField(max_length=20, unique=True, db_column='CODE')
    SUPPLIER_ID = models.ForeignKey(Supplier, on_delete=models.PROTECT, db_column='SUPPLIER_ID')
    DATE = models.DateField(db_column='DATE')
    TOTAL_AMOUNT = models.DecimalField(max_digits=15, decimal_places=2, default=0, db_column='TOTAL_AMOUNT')
    STATUS = models.CharField(max_length=20, 
                              choices=[('PENDING', 'Pending'), ('COMPLETED', 'Completed'), ('CANCELLED', 'Cancelled')], 
                              default='COMPLETED', db_column='STATUS')
    
    # Audit Fields
    CREATED_BY = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='purchase_created', db_column='CREATED_BY')
    CREATED_AT = models.DateTimeField(auto_now_add=True, db_column='CREATED_AT')
    UPDATED_BY = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='purchase_updated', db_column='UPDATED_BY')
    UPDATED_AT = models.DateTimeField(auto_now=True, db_column='UPDATED_AT')

    class Meta:
        db_table = 'PURCHASE'

    def __str__(self):
        return self.PURCHASE_CODE


class PurchaseDetail(models.Model):
    ID = models.AutoField(primary_key=True, db_column='ID')
    PURCHASE_ID = models.ForeignKey(Purchase, on_delete=models.CASCADE, db_column='PURCHASE_ID')
    PRODUCT_ID = models.ForeignKey(Product, on_delete=models.PROTECT, db_column='PRODUCT_ID')
    QUANTITY = models.IntegerField(db_column='QUANTITY')
    UNIT_PRICE = models.DecimalField(max_digits=15, decimal_places=2, db_column='UNIT_PRICE')
    
    # Audit Fields
    CREATED_BY = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='purchase_detail_created', db_column='CREATED_BY')
    CREATED_AT = models.DateTimeField(auto_now_add=True, db_column='CREATED_AT')
    UPDATED_BY = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='purchase_detail_updated', db_column='UPDATED_BY')
    UPDATED_AT = models.DateTimeField(auto_now=True, db_column='UPDATED_AT')

    class Meta:
        db_table = 'PURCHASE_DETAIL'
        unique_together = ('PURCHASE_ID', 'PRODUCT_ID')   # Prevent duplicate product in one purchase

    def save(self, *args, **kwargs):
        self.SUBTOTAL = self.QUANTITY * self.UNIT_PRICE
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Purchase {self.PURCHASE.PURCHASE_CODE} - {self.PRODUCT.CODE}"


# # ====================== PURCHASE DETAIL MODEL ======================
# class PurchaseDetail(models.Model):
#     PURCHASE_DETAIL_ID = models.AutoField(primary_key=True, db_column='PURCHASE_DETAIL_ID')
    
#     PURCHASE = models.ForeignKey(
#         'Purchase', 
#         on_delete=models.CASCADE, 
#         related_name='purchase_details',
#         db_column='PURCHASE_ID'
#     )
#     PRODUCT = models.ForeignKey(
#         'Product', 
#         on_delete=models.PROTECT, 
#         db_column='PRODUCT_ID'
#     )
    
#     QUANTITY = models.IntegerField(db_column='QUANTITY', validators=[MinValueValidator(1)])
#     UNIT_PRICE = models.DecimalField(max_digits=15, decimal_places=2, db_column='UNIT_PRICE')
    
#     # Optional: Subtotal can be calculated, but we store it for audit
#     SUBTOTAL = models.DecimalField(max_digits=15, decimal_places=2, editable=False, db_column='SUBTOTAL')

#     # Audit Fields
#     CREATED_BY = models.ForeignKey(
#         User, 
#         on_delete=models.PROTECT, 
#         related_name='purchase_detail_created', 
#         db_column='CREATED_BY'
#     )
#     CREATED_AT = models.DateTimeField(auto_now_add=True, db_column='CREATED_AT')
#     UPDATED_BY = models.ForeignKey(
#         User, 
#         on_delete=models.SET_NULL, 
#         null=True, 
#         blank=True, 
#         related_name='purchase_detail_updated', 
#         db_column='UPDATED_BY'
#     )
#     UPDATED_AT = models.DateTimeField(auto_now=True, db_column='UPDATED_AT')

#     class Meta:
#         db_table = 'PURCHASE_DETAIL'
#         unique_together = ('PURCHASE', 'PRODUCT')   # Prevent duplicate product in one purchase

#     def save(self, *args, **kwargs):
#         self.SUBTOTAL = self.QUANTITY * self.UNIT_PRICE
#         super().save(*args, **kwargs)

#     def __str__(self):
#         return f"Purchase {self.PURCHASE.PURCHASE_CODE} - {self.PRODUCT.PRODUCT_CODE}"