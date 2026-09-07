from django.urls import path
from galeria.views import album, galeria

urlpatterns = [
    path('<int:id>/', album, name= 'album'),
    path('', galeria, name='galeria')
]