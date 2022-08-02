# Generated by Django 4.0.4 on 2022-08-01 12:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_order'),
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
        migrations.DeleteModel(
            name='Book',
        ),
        migrations.DeleteModel(
            name='Order',
        ),
        migrations.DeleteModel(
            name='UserInfo',
        ),
    ]
