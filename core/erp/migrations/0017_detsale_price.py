# Generated by Django 4.2.8 on 2024-04-10 17:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('erp', '0016_alter_product_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='detsale',
            name='price',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=9),
        ),
    ]
