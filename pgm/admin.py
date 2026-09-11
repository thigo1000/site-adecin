from django.contrib import admin
from pgm.models import Pgm


class PgmAdmin(admin.ModelAdmin):
    list_display = ('nome', 'bairro', 'dia', 'lider', 'ativo')
    list_editable = ('ativo',)
    list_per_page = (20)
    list_filter = ('dia', 'bairro')

admin.site.register(Pgm, PgmAdmin)