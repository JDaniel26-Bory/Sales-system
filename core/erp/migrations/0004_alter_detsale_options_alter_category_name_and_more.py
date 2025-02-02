# Generated by Django 4.2.8 on 2024-03-01 21:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('erp', '0003_alter_category_options_remove_client_adress_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='detsale',
            options={'ordering': ['id'], 'verbose_name': 'Detalle de Venta', 'verbose_name_plural': 'Detalles de Venta'},
        ),
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(max_length=150, unique=True, verbose_name='Nombre'),
        ),
        migrations.AlterField(
            model_name='detsale',
            name='price',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=12, verbose_name='Precio'),
        ),
        migrations.AlterField(
            model_name='detsale',
            name='quantity',
            field=models.IntegerField(default=0, verbose_name='Cantidad'),
        ),
        migrations.AlterField(
            model_name='detsale',
            name='subtotal',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=12, verbose_name='Subtotal'),
        ),
    ]
