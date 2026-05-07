
from django.db import models

from inventory.customers.models import Customer
from inventory.products.models import Product



class Sale(models.Model):
    ID = models.AutoField(primary_key=True, db_column='ID')
    CODE = models.CharField(max_length=20, unique=True, db_column='CODE')
    CUSTOMER_ID = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True, db_column='CUSTOMER_ID')
    DATE = models.DateField(db_column='SDATE')
    TOTAL_AMT = models.DecimalField(max_digits=15, decimal_places=2, default=0, db_column='TOTAL_AMOUNT')
    DISCOUNT = models.DecimalField(max_digits=15, decimal_places=2, default=0, db_column='DISCOUNT')
    NET_AMOUNT = models.DecimalField(max_digits=15, decimal_places=2, default=0, editable=False, db_column='NET_AMOUNT')
    PAYMENT_METHOD = models.CharField(max_length=20, 
                                      choices=[('CASH','Cash'),('BANK_TRANSFER','Bank Transfer'),('CARD','Card'),('OTHER','Other')], 
                                      default='CASH', db_column='PAYMENT_METHOD')
    STATUS = models.CharField(max_length=20, 
                              choices=[('PENDING', 'Pending'), ('COMPLETED', 'Completed'), ('CANCELLED', 'Cancelled')], 
                              default='COMPLETED', db_column='STATUS')
    
    # Audit Fields
    CREATED_BY = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='sale_created', db_column='CREATED_BY')
    CREATED_AT = models.DateTimeField(auto_now_add=True, db_column='CREATED_AT')
    UPDATED_BY = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='sale_updated', db_column='UPDATED_BY')
    UPDATED_AT = models.DateTimeField(auto_now=True, db_column='UPDATED_AT')

    class Meta:
        db_table = 'SALE'

    def save(self, *args, **kwargs):
        self.NET_AMOUNT = self.TOTAL_AMOUNT - self.DISCOUNT
        super().save(*args, **kwargs)

class SaleDetail(models.Model):
    ID = models.AutoField(primary_key=True, db_column='ID')
    SALE_ID = models.ForeignKey(Sale, on_delete=models.CASCADE, db_column='SALE_ID')
    PRODUCT_ID = models.ForeignKey(Product, on_delete=models.PROTECT, db_column='PRODUCT_ID')
    QUANTITY = models.IntegerField(db_column='QUANTITY')
    UNIT_PRICE = models.DecimalField(max_digits=15, decimal_places=2, db_column='UNIT_PRICE')
    
    # Audit Fields
    CREATED_BY = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='sale_detail_created', db_column='CREATED_BY')
    CREATED_AT = models.DateTimeField(auto_now_add=True, db_column='CREATED_AT')
    UPDATED_BY = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='sale_detail_updated', db_column='UPDATED_BY')
    UPDATED_AT = models.DateTimeField(auto_now=True, db_column='UPDATED_AT')

    class Meta:
        db_table = 'SALE_DETAIL'