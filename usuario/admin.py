from django.contrib import admin
from usuario.models import Membro

class ListaMembro(admin.ModelAdmin):
    list_display = ('nome', 'cpf', 'usuario')

admin.site.register(Membro, ListaMembro)