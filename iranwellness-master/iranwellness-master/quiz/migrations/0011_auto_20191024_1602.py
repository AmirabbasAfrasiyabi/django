# Generated by Django 2.2.5 on 2019-10-24 23:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0010_auto_20191024_1543'),
    ]

    operations = [
        migrations.RenameField(
            model_name='wellnesscircle',
            old_name='scores',
            new_name='totalquiz',
        ),
    ]
