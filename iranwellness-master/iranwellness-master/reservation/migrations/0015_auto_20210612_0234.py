# Generated by Django 2.2.3 on 2021-06-11 22:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reservation', '0014_auto_20201215_2006'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='dayoff',
            options={'ordering': ['year', 'month', 'day'], 'verbose_name': 'روز تعطیل', 'verbose_name_plural': 'روزهای تعطیل'},
        ),
    ]
