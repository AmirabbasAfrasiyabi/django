# Generated by Django 2.2.3 on 2019-11-25 08:21

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Shoppingitem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Ename', models.CharField(max_length=20)),
                ('Pname', models.CharField(max_length=20)),
                ('ptype', models.CharField(max_length=20)),
                ('price', models.IntegerField()),
            ],
        ),
    ]
