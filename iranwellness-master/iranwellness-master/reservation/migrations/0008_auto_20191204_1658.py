# Generated by Django 2.2.3 on 2019-12-04 13:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservation', '0007_auto_20191202_1350'),
    ]

    operations = [
        migrations.AddField(
            model_name='healthreservation',
            name='duration',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='resonancereservation',
            name='duration',
            field=models.IntegerField(default=0),
        ),
    ]
