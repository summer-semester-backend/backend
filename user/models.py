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


class Book(models.Model):
    ISBN = models.CharField(max_length=50, primary_key=True)
    Title = models.CharField(max_length=50, null=True)

    class Meta:
        db_table = "Book"


class Order(models.Model):
    OrderID = models.UUIDField(auto_created=True, primary_key=True)

    class Meta:
        db_table = "Order"
