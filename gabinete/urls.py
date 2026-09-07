from django.urls import path

from gabinete.views import gabinete, cancelar_gabinete

urlpatterns = [
    path('', gabinete, name='gabinete'),
    path('cancelar/<int:id>/', cancelar_gabinete, name='cancelar_gabinete'),
]

