# Generated by Django 2.2.3 on 2019-12-15 11:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0020_auto_20191209_1618'),
    ]

    operations = [
        migrations.AddField(
            model_name='wellnesscircle',
            name='result',
            field=models.CharField(default='', max_length=5000),
        ),
    ]
