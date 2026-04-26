
from django.db import models

from django.conf import settings
from inventory.products.models import Product

class StockMovement(models.Model):
    ID = models.AutoField(primary_key=True, db_column='ID')
    PRODUCT_ID = models.ForeignKey(Product, on_delete=models.PROTECT, db_column='PRODUCT_ID')
    TYPE = models.CharField(max_length=20, 
                                     choices=[('PURCHASE','Purchase'),('SALE','Sale'),('ADJUSTMENT','Adjustment')], 
                                     db_column='TYPE')
    QUANTITY = models.IntegerField(db_column='QUANTITY')   # Positive = In, Negative = Out
    REFERENCE_ID = models.IntegerField(null=True, blank=True, db_column='REFERENCE_ID')
    REFERENCE_TYPE = models.CharField(max_length=20, null=True, blank=True, db_column='REFERENCE_TYPE')
    NOTES = models.TextField(null=True, blank=True, db_column='NOTES')
    
    # Audit Fields
    CREATED_BY = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='stock_movement_created', db_column='CREATED_BY')
    CREATED_AT = models.DateTimeField(auto_now_add=True, db_column='CREATED_AT')
    UPDATED_BY = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='stock_movement_updated', db_column='UPDATED_BY')
    UPDATED_AT = models.DateTimeField(auto_now=True, db_column='UPDATED_AT')

    class Meta:
        db_table = 'STOCK_MOVEMENT'