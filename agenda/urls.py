from django.urls import path
from agenda.views import agenda

urlpatterns = [
    path('', agenda, name= 'agenda'),
]