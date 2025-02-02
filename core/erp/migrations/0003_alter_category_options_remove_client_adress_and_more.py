# Generated by Django 4.2.8 on 2024-01-13 15:55

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('erp', '0002_alter_client_sex'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'ordering': ['id'], 'verbose_name': 'Category', 'verbose_name_plural': 'Categories'},
        ),
        migrations.RemoveField(
            model_name='client',
            name='adress',
        ),
        migrations.AddField(
            model_name='category',
            name='desc',
            field=models.CharField(blank=True, max_length=150, null=True, verbose_name='Descripción'),
        ),
        migrations.AddField(
            model_name='client',
            name='address',
            field=models.CharField(blank=True, max_length=150, null=True, verbose_name='Address'),
        ),
        migrations.AlterField(
            model_name='client',
            name='birthDate',
            field=models.DateField(default=datetime.datetime.now, verbose_name='Birth Date'),
        ),
        migrations.AlterField(
            model_name='client',
            name='identificationCard',
            field=models.CharField(max_length=10, unique=True, verbose_name='Card'),
        ),
        migrations.AlterField(
            model_name='product',
            name='name',
            field=models.CharField(max_length=150, unique=True, verbose_name='Name'),
        ),
    ]
