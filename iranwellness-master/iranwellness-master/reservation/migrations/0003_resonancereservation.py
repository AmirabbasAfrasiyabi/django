# Generated by Django 2.2.1 on 2019-08-13 11:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('reservation', '0002_auto_20190813_1459'),
    ]

    operations = [
        migrations.CreateModel(
            name='resonancereservation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year', models.IntegerField(default=0)),
                ('month', models.IntegerField(default=0)),
                ('day', models.IntegerField(default=0)),
                ('order', models.IntegerField(default=0)),
                ('string', models.CharField(default='', max_length=50)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]