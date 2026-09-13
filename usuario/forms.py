from django import forms
import re
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User


class VerificadorForms(forms.Form):
    cpf = forms.CharField(
        label= 'CPF',
        max_length= 11
    )

    def clean_cpf(self):
        cpf = self.cleaned_data['cpf']
        so_numeros = re.sub(r'\D', '', cpf)
        if len(so_numeros) != 11:
            raise ValidationError('CPF Inválido')
        return so_numeros


class CadastroForms(UserCreationForm):
    first_name = forms.CharField(required=True, label='Nome')
    last_name = forms.CharField(required=False, label='Sobrenome')
    email = forms.EmailField(required=True, label='E-mail')

    def clean_username(self):
        username = self.cleaned_data['username']
        username = username.strip().lower()
        if User.objects.filter(username=username).exists():
            raise ValidationError('Este nome de usuário já está em uso.')
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        email = email.lower()
        if User.objects.filter(email=email).exists():
            raise ValidationError('Email ja cadastrado')
        return email

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')


class LoginForms(AuthenticationForm):

    error_messages = {
        'invalid_login': 'Usuário ou senha incorretos.',
        'inactive': 'Esta conta está desativada.',
    }
    
    def clean_username(self):
        username = self.cleaned_data['username']
        return username.strip().lower()