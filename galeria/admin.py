from django.contrib import admin
from galeria.forms import FotoEmLoteForm
from galeria.models import Album, Foto, Video, Colecao


@admin.register(Colecao)
class ColecaoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'ativo')
    list_editable = ('ativo',)


@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):
    list_display = ('nome', 'colecao', 'data', 'quantidade_fotos', 'criado_em')
    list_filter = ('colecao', 'data')
    search_fields = ('nome',)
    list_filter = ('data',)
    list_per_page = 15


@admin.register(Foto)
class FotoAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'album')
    list_filter = ('album',)
    list_per_page = 10

    def get_form(self, request, obj=None, **kwargs):
        if obj is None:
            kwargs['form'] = FotoEmLoteForm
        return super().get_form(request, obj, **kwargs)

    def save_model(self, request, obj, form, change):
        if change:
            return super().save_model(request, obj, form, change)

        arquivos = request.FILES.getlist('imagens')

        obj.imagem = arquivos[0]
        obj.save()

        for arquivo in arquivos[1:]:
            Foto(album=obj.album, imagem=arquivo).save()

@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'album', 'criado_em')
    list_filter = ('album',)
    search_fields = ('titulo',)
    list_per_page = 10
