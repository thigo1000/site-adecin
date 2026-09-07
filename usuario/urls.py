from django.urls import path
from usuario.views import verificador, cadastro
from django.contrib.auth.views import LoginView
from usuario.forms import LoginForms

urlpatterns = [
    path('verificar/', verificador, name='verificador'),
    path('cadastro/', cadastro, name='cadastro'),
    path('login/', LoginView.as_view(authentication_form=LoginForms), name='login')
]