from typing import Iterable
from django.db import models, transaction
from datetime import datetime

from django.forms import model_to_dict
from .choices import gender_choices
from config.settings import MEDIA_URL, STATIC_URL
from core.models import BaseModel
from crum import get_current_user

class Category(BaseModel):
    name = models.CharField(max_length=150, verbose_name='Nombre', unique=True)
    desc = models.CharField(max_length=150, null=True, blank=True, verbose_name='Descripción')

    def __str__(self):
        return self.name
    
    def toJSON(self):
        item = model_to_dict(self, exclude=['user_creation', 'user_updated'])
        return item
    
    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        ordering = ['id']

class Product(models.Model):
    name = models.CharField(max_length=150, verbose_name='Nombre', unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Categoría')
    image = models.ImageField(upload_to='product/%Y/%m/%d', null=True, blank=True, verbose_name='Imagen')
    pvp = models.DecimalField(default=0.00, max_digits=9, decimal_places=3, verbose_name='Precio de Venta')
    stock = models.IntegerField(default=0, verbose_name='Stock')
    

    def __str__(self):
        return self.name
    
    def toJSON(self):
        item = model_to_dict(self)
        item['full_name'] = '{} / {}'.format(self.name, self.category.name)
        item['category'] = self.category.toJSON()
        item['image'] = self.get_image()
        item['pvp'] = format(self.pvp, '.3f')
        return item

    def get_image(self):
        if self.image:
            return '{}{}'.format(MEDIA_URL, self.image)
        return '{}{}'.format(STATIC_URL, 'img/favicon.jpeg')
    
    def formatear_numero_decimal(self):
        numero_str = str(self.pvp)
        numero_formateado = numero_str.replace(',', '.')
        return numero_formateado
    
    class Meta:
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'
        ordering = ['id']

class Client(models.Model):
    name = models.CharField(max_length=150, verbose_name='Nombre')
    lastName = models.CharField(max_length=150, verbose_name='Apellido')
    identificationCard = models.CharField(max_length=10, unique=True, verbose_name='Cédula')
    birthDate = models.DateField(default=datetime.now, verbose_name='Fecha de Naciemiento')
    address = models.CharField(max_length=150, null=True, blank=True, verbose_name='Dirección')
    gender = models.CharField(max_length=10, choices=gender_choices, default='male', verbose_name='Sexo')

    def __str__(self):
        return self.get_full_name()
    
    def get_full_name(self):
        return '{} {} / {}'.format(self.name, self.lastName, self.identificationCard)
    
    def toJSON(self):
        item = model_to_dict(self)
        item['gender'] = {'id': self.gender, 'name': self.get_gender_display()}
        item['birthDate'] = self.birthDate.strftime('%Y-%m-%d')
        item['full_name'] = self.get_full_name()
        return item
    
    class Meta:
        verbose_name = 'Client'
        verbose_name_plural = 'Clients'
        ordering = ['id']

class Sale(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    registrationDate = models.DateField(default=datetime.now)
    subtotal = models.DecimalField(default=0.00, max_digits=9, decimal_places=3)
    iva = models.DecimalField(default=0.00, max_digits=9, decimal_places=3)
    total = models.DecimalField(default=0.00, max_digits=9, decimal_places=3)

    def __str__(self):
        return self.client.name
    
    def toJSON(self):
        item = model_to_dict(self)
        item['client'] = self.client.toJSON()
        item['subtotal'] = format(self.subtotal, '.3f')
        item['iva'] = format(self.iva, '.3f')
        item['total'] = format(self.total, '.3f')
        item['registrationDate'] = self.registrationDate.strftime('%Y-%m-%d')
        item['det'] = [i.toJSON() for i in self.detsale_set.all()]
        return item
    
    def delete(self):
        for det in self.detsale_set.all():
            det.product.stock += det.quantity
            det.product.save()
        super(Sale, self).delete()

    class Meta:
        verbose_name = 'Venta'
        verbose_name_plural = 'Ventas'
        ordering = ['id']

class DetSale(models.Model):
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    quantity = models.IntegerField(default=0, verbose_name='Cantidad')
    subtotal = models.DecimalField(default=0.00, max_digits=9, decimal_places=3, verbose_name='Subtotal')


    def __str__(self):
        return self.product.name
    
    def toJSON(self):
        item = model_to_dict(self, exclude=['sale'])
        item['product'] = self.product.toJSON()
        item['price'] = format(self.price, '.3f')
        item['subtotal'] = format(self.subtotal, '.3f')
        return item


    class Meta:
        verbose_name = 'Detalle de Venta'
        verbose_name_plural = 'Detalles de Venta'
        ordering = ['id']
