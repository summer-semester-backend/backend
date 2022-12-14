# Generated by Django 3.2.12 on 2022-08-02 03:49

from django.db import migrations, models
import utils.storage


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='EmailCode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=50)),
                ('time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
            ],
        ),
        migrations.CreateModel(
            name='Img',
            fields=[
                ('imgID', models.AutoField(primary_key=True, serialize=False)),
                ('img', models.ImageField(blank=True, storage=utils.storage.ImageStorage(), upload_to='image/%Y%m%d')),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('userID', models.IntegerField(primary_key=True, serialize=False, verbose_name='用户ID')),
                ('email', models.EmailField(max_length=254, verbose_name='邮箱')),
                ('username', models.CharField(max_length=25, null=True, verbose_name='真实姓名')),
                ('nickname', models.CharField(max_length=25, null=True, verbose_name='昵称')),
                ('password', models.CharField(max_length=50, verbose_name='密码')),
                ('sex', models.IntegerField(blank=True, null=True, verbose_name='性别')),
                ('age', models.IntegerField(blank=True, null=True, verbose_name='年龄')),
                ('avatar', models.CharField(blank=True, max_length=50, null=True, verbose_name='头像地址')),
                ('phone', models.CharField(max_length=25, null=True, verbose_name='电话')),
                ('summary', models.CharField(max_length=100, null=True, verbose_name='个人资料')),
            ],
        ),
    ]
