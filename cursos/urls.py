from django.urls import path
from cursos.views import lista_curso, detalhe_curso, material_curso


urlpatterns = [
    path('', lista_curso, name='lista_curso'),
    path('material/<int:id>/', material_curso, name='material_curso'),
    path('<slug:slug>/', detalhe_curso, name='curso'),
    path('<slug:slug>/aula/<int:ordem>/', detalhe_curso, name='aula'),
]