from django.contrib import admin
from ebd.models import Turma, Tema

class ListaTema(admin.ModelAdmin):
    list_display = ('livro', 'subtitulo', 'periodo', 'ativo')
    list_editable = ('ativo',)

admin.site.register(Tema, ListaTema)


class ListaTurma(admin.ModelAdmin):
    list_display = ('nome', 'material', 'ativo')
    list_editable = ('ativo',)

admin.site.register(Turma, ListaTurma)
