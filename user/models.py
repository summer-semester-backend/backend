from django.db import models
from django.contrib.auth.models import User
from django.db.models.base import Model
from django.db.models.deletion import PROTECT
from utils.storage import *


# Create your models here.


class User(models.Model):
    userID = models.IntegerField(primary_key=True, verbose_name='用户ID')
    email = models.EmailField(verbose_name='邮箱', blank=False)
    username = models.CharField(max_length=25, null=True, verbose_name='真实姓名')
    nickname = models.CharField(max_length=25, null=True, verbose_name='昵称')
    password = models.CharField(max_length=50, verbose_name='密码')
    sex = models.IntegerField(blank=True, null=True, verbose_name='性别')
    age = models.IntegerField(blank=True, null=True, verbose_name='年龄')
    avatar = models.CharField(max_length=50, blank=True, null=True, verbose_name='头像地址')
    phone = models.CharField(max_length=25, null=True, verbose_name='电话')
    summary = models.CharField(max_length=100, null=True, verbose_name='个人资料')


class EmailCode(models.Model):
    code = models.CharField(max_length=50)
    time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)


class Img(models.Model):
    imgID = models.AutoField(primary_key=True)
    img = models.ImageField(blank=True, upload_to='image/%Y%m%d', storage=ImageStorage())
