from django.contrib import admin
from pgm.models import Pgm


class PgmAdmin(admin.ModelAdmin):
    list_display = ('nome', 'categoria', 'bairro', 'dia', 'lider', 'ativo')
    list_editable = ('categoria', 'ativo')
    list_per_page = (20)
    list_filter = ('categoria', 'dia', 'bairro')

admin.site.register(Pgm, PgmAdmin)