# Generated by Django 2.2.1 on 2019-09-05 22:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0003_auto_20190906_0305'),
    ]

    operations = [
        migrations.AlterField(
            model_name='submit',
            name='response',
            field=models.CharField(default='', max_length=30),
        ),
    ]