
from django.db import models
from accounts.users.models import Users
from django.conf import settings

# ====================== MAIN MODELS ======================
class Customer(models.Model):
    ID = models.AutoField(primary_key=True, db_column='ID')
    CODE = models.CharField(max_length=20, unique=True, db_column='CODE')
    NAME = models.CharField(max_length=100, db_column='NAME')
    PHONE = models.CharField(max_length=20, null=True, blank=True, db_column='PHONE')
    EMAIL = models.EmailField(max_length=100, null=True, blank=True, db_column='EMAIL')
    ADDRESS = models.TextField(null=True, blank=True, db_column='ADDRESS')
    
    # Audit Fields
    CREATED_BY = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='customer_created', db_column='CREATED_BY')
    CREATED_AT = models.DateTimeField(auto_now_add=True, db_column='CREATED_AT')
    UPDATED_BY = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='customer_updated', db_column='UPDATED_BY')
    UPDATED_AT = models.DateTimeField(auto_now=True, db_column='UPDATED_AT')

    class Meta:
        db_table = 'CUSTOMER'

    def __str__(self):
        return self.CUSTOMER_NAME