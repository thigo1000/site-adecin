from django.urls import path
from pgm.views import pgm

urlpatterns = [
    path('', pgm, name='pgm')
]