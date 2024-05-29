from django.forms import *

class ReportForm(Form):
    dateRange = CharField(widget=TextInput(attrs={
        'class': 'form-control',
        'autocomplete': 'off'
    }))