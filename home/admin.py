from django.contrib import admin
from home.models import Anuncio

class ListaAnuncio(admin.ModelAdmin):
    list_display = ('titulo', 'ordem', 'expira_em', 'ativo')
    list_editable = ('ordem', 'expira_em', 'ativo')

admin.site.register(Anuncio, ListaAnuncio)