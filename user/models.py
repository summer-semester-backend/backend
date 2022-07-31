from django.db import models


# Create your models here.

class UserInfo(models.Model):
    """
    用户表
    """
    email = models.EmailField(primary_key=True)
    username = models.CharField(max_length=25, null=True)

    class Meta:
        db_table = "UserInfo"


