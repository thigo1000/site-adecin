from django.urls import path
from galeria.views import album, galeria, colecao

urlpatterns = [
    path('<int:id>/', album, name= 'album'),
    path('', galeria, name='lista'),
    path('colecao/<int:id>/', colecao, name='colecao')
]