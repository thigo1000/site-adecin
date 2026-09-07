from django import forms

from galeria.models import Foto


class MultiplasImagens(forms.ClearableFileInput):
    allow_multiple_selected = True


class MultiploFileField(forms.FileField):

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('widget', MultiplasImagens())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        valida_um = super().clean
        if isinstance(data, (list, tuple)):
            return [valida_um(arquivo, initial) for arquivo in data]
        return valida_um(data, initial)


class FotoEmLoteForm(forms.ModelForm):

    imagens = MultiploFileField(
        label='Fotos',
        help_text='Segure Shift ou Ctrl para selecionar várias de uma vez.',
    )

    class Meta:
        model = Foto
        fields = ('album',)