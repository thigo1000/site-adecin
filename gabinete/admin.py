from django.contrib import admin
from gabinete.models import Gabinete, Janela, Agendamento


class GabineteList(admin.ModelAdmin):
    list_display = ('nome', 'telefone')

admin.site.register(Gabinete, GabineteList)


class JanelaList(admin.ModelAdmin):
    list_display = ('data', 'inicio', 'fim')
    list_filter = ('data',)

admin.site.register(Janela, JanelaList)


class AgendamentoList(admin.ModelAdmin):
    list_display = ('data', 'horario', 'membro', 'status')
    list_editable = ('status',)
    list_filter = ('data', 'status')
    list_per_page = 10

admin.site.register(Agendamento, AgendamentoList)