# Generated by Django 2.2.1 on 2019-09-05 22:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0002_auto_20190905_1957'),
    ]

    operations = [
        migrations.DeleteModel(
            name='details',
        ),
        migrations.DeleteModel(
            name='title',
        ),
    ]
