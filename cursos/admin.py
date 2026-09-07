from django.contrib import admin
from cursos.models import Curso, Aula, Material

class ListaCurso(admin.ModelAdmin):
    list_display = ('curso', 'acesso', 'criado_em', 'ativo')
    list_editable = ('ativo',)
    prepopulated_fields = {'slug': ('curso',)}
    filter_horizontal = ('liberados',)

    fieldsets = [
        ('Conteúdo', {
            'fields': ['curso', 'slug', 'resumo', 'capa']
        }),
        ('Acesso', {
            'fields': ['acesso', 'aviso', 'liberados'],
            'description': 'O aviso e a lista só valem para cursos restritos.'
        }),
        ('Publicação', {
            'fields': ['ativo']
        }),
    ]

admin.site.register(Curso, ListaCurso)


class ListaAula(admin.ModelAdmin):
    list_display = ('ordem', 'titulo', 'gratis', 'youtube_id', 'curso', 'duracao')
    list_editable = ('gratis',)
    list_filter = ('curso',)
admin.site.register(Aula, ListaAula)


class ListaMaterial(admin.ModelAdmin):
    list_display = ('nome', 'pdf', 'curso')

admin.site.register(Material, ListaMaterial)