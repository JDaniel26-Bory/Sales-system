# Generated by Django 4.2.8 on 2024-04-12 22:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('erp', '0017_detsale_price'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='sale',
            options={'ordering': ['id'], 'verbose_name': 'Venta', 'verbose_name_plural': 'Ventas'},
        ),
    ]
