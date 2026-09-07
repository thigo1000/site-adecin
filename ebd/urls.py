from django.urls import path
from ebd.views import ebd, material_turma


urlpatterns = [
    path('', ebd, name='ebd'),
    path('material/<int:id>/', material_turma, name='material_turma'),
]