# Generated by Django 4.0.4 on 2022-08-05 13:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='userID',
            field=models.AutoField(editable=False, primary_key=True, serialize=False),
        ),
    ]
