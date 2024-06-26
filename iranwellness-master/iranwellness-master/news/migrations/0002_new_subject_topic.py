# Generated by Django 2.2.3 on 2020-04-15 14:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='new',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Pname', models.CharField(max_length=50, null=True)),
                ('Ename', models.CharField(max_length=50, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='subject',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Pname', models.CharField(max_length=50, null=True)),
                ('Ename', models.CharField(max_length=50, null=True)),
                ('new', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='news.new')),
            ],
        ),
        migrations.CreateModel(
            name='topic',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Pname', models.CharField(max_length=50, null=True)),
                ('Ename', models.CharField(max_length=50, null=True)),
                ('subject', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='news.subject')),
            ],
        ),
    ]
