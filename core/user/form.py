from django import forms
from core.user.models import User

class UserForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs['placeholder'] = 'Ingrese sus Nombres'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Ingrese sus Apellidos'
        self.fields['email'].widget.attrs['placeholder'] = 'Ingrese su Correo Electrónico'
        self.fields['username'].widget.attrs['placeholder'] = 'Ingrese su Nombre de Usuario'
        self.fields['password'].widget.attrs['placeholder'] = 'Ingrese su Contraseña'

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username', 'password', 'image', 'groups']
        widgets = {
            'password': forms.PasswordInput(render_value=True),
            'groups': forms.SelectMultiple(attrs={
                'class': 'form-control select2',
                'style': 'width: 100%',
                'multiple': 'multiple'
            })
        }
        exclude = ['user_permissions', 'last_login', 'date_joined', 'is_superuser', 'is_staff', 'is_active']

    def save(self, commit=True):
        data = {}
        form = super().save(commit=False)
        try:
            if self.instance.pk is None:
                form.set_password(self.cleaned_data['password'])
            else:
                user = User.objects.get(pk=self.instance.pk)
                if user.password != self.cleaned_data['password']:
                    form.set_password(self.cleaned_data['password'])
            form.save()
            form.groups.clear()
            for group in self.cleaned_data['groups']:
                form.groups.add(group)
        except Exception as e:
            data['error'] = str(e)
        return data

class UserProfileForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs['placeholder'] = 'Ingrese sus Nombres'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Ingrese sus Apellidos'
        self.fields['email'].widget.attrs['placeholder'] = 'Ingrese su Correo Electrónico'
        self.fields['username'].widget.attrs['placeholder'] = 'Ingrese su Nombre de Usuario'
        self.fields['password'].widget.attrs['placeholder'] = 'Ingrese su Contraseña'

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username', 'password', 'image']
        widgets = {
            'password': forms.PasswordInput(render_value=True),
        }
        exclude = ['user_permissions', 'last_login', 'date_joined', 'is_superuser', 'is_staff', 'is_active', 'groups']

    def save(self, commit=True):
        data = {}
        form = super().save(commit=False)
        try:
            if self.instance.pk is None:
                form.set_password(self.cleaned_data['password'])
            else:
                user = User.objects.get(pk=self.instance.pk)
                if user.password != self.cleaned_data['password']:
                    form.set_password(self.cleaned_data['password'])
            form.save()
        except Exception as e:
            data['error'] = str(e)
        return data
