# Generated by Django 4.0.6 on 2022-07-31 03:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('ISBN', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('Title', models.CharField(max_length=50, null=True)),
            ],
            options={
                'db_table': 'Book',
            },
        ),
    ]
