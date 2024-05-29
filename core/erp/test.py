from core.erp.models import *

data = ['LLantas', 'Neumáticos', 'Balineras', 'Balineras Koyo', 'Bandas de Freno economicas', 'Bandas de freno Originales'
        'Bandas de freno Osaka', 'Guayas completas', 'Pastillas Economicas', 'Pastillas Originales']

for i in data:
    cat = Category(name = i)
    cat.save()
    print('Guardando el registro N{}'.format(cat.id))