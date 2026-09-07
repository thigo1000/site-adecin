from django.contrib import admin
from agenda.models import AgendaSemanal, AgendaMensal

class ListaSemanal(admin.ModelAdmin):
    list_display = ('id', 'dia','horario', 'evento')

admin.site.register(AgendaSemanal, ListaSemanal)

class ListaMensal(admin.ModelAdmin):
    list_display = ('id', 'data', 'culto')
    search_fields = ('culto',)

admin.site.register(AgendaMensal, ListaMensal)
