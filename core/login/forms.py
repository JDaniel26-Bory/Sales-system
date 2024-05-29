from django import forms
from core.user.models import User

class ResetPasswordForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Ingrese un usuario',
        'class': 'form-control',
        'autocomplete': 'off'
    }))

    def clean(self):
        cleaned = super().clean()
        if not User.objects.filter(username=cleaned['username']).exists():
            self.add_error('username', 'El Usuario No existe')
        return cleaned
    
    def get_user(self):
        username = self.cleaned_data.get('username')
        return User.objects.get(username=username)
    
class ChangePasswordForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Ingrese una Contraseña',
        'class': 'form-control',
        'autocomplete': 'off'
    }))

    confirmpassword = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Repita la contraseña',
        'class': 'form-control',
        'autocomplete': 'off'
    }))
    
    def clean(self):
        cleaned = super().clean()
        password = cleaned['password']
        confirmpassword = cleaned['confirmpassword']

        if password != confirmpassword:
            raise forms.ValidationError('Las Contraseñas deben ser iguales')
        return cleaned