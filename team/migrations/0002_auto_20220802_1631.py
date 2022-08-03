# Generated by Django 3.2.12 on 2022-08-02 08:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('team', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='team',
            name='summary',
            field=models.CharField(default='', max_length=65536),
        ),
        migrations.AlterField(
            model_name='team_user',
            name='authority',
            field=models.IntegerField(choices=[(2, 'founder'), (1, 'manager'), (0, 'member'), (-1, 'invited')], default=0),
        ),
    ]
