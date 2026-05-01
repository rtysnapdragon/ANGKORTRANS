
class Follow(models.Model):
    Id = models.IntegerField(auto_created=True,primary_key=True,db_column="ID")
    FollowedBy = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='followed_by',db_column="FOLLOWED_BY")
    Target = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='target',db_column="TARGET")
    IsFollow = models.BooleanField(default=False,db_column="IS_FOLLOW")
    IsRequest = models.BooleanField(default=False,db_column="IS_REQUEST")
    Status = models.BooleanField(default=False,db_column="STATUS")
    CreatedBy = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='follow_created_by',db_column="CREATED_BY")
    UpdatedBy = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='follow_updated_by',db_column="UPDATED_BY")
    CreatedAt = models.DateTimeField(auto_now_add=True,db_column="CREATED_AT")
    UpdatedAt = models.DateTimeField(auto_now=True,db_column="UPDATED_AT")
    def __str__(self):
        return str(self.Id)
    class Meta:
        db_table = "FOLLOWS"
        managed = True
        verbose_name = "Follow"
        verbose_name_plural = "Follows"