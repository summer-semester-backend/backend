# Generated by Django 4.0.6 on 2022-07-31 03:29

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UserInfo',
            fields=[
                ('email', models.EmailField(max_length=254, primary_key=True, serialize=False)),
                ('username', models.CharField(max_length=25, null=True)),
            ],
            options={
                'db_table': 'UserInfo',
            },
        ),
    ]
