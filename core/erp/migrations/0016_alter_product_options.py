# Generated by Django 4.2.8 on 2024-04-10 16:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('erp', '0015_remove_client_sex_client_gender_alter_client_address_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='product',
            options={'ordering': ['id'], 'verbose_name': 'Producto', 'verbose_name_plural': 'Productos'},
        ),
    ]
