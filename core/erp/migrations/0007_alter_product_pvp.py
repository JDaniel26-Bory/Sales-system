# Generated by Django 4.2.8 on 2024-03-01 22:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('erp', '0006_alter_product_pvp'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='pvp',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=9),
        ),
    ]
