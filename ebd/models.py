from django.db import models
from django.core.validators import FileExtensionValidator
from django.core.exceptions import ValidationError
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.db.models.signals import post_delete
from django.dispatch import receiver


protegido = FileSystemStorage(location=settings.ARQUIVOS_PROTEGIDOS)

class Tema(models.Model):
    livro = models.CharField(max_length=50)
    subtitulo = models.CharField(max_length=100)
    introducao = models.TextField()
    periodo = models.CharField(max_length=150)
    ativo = models.BooleanField(default=False)

    def clean(self):
        if self.ativo:                                    
            existe_outro = Tema.objects.filter(ativo=True).exclude(pk=self.pk).exists()
            if existe_outro:                              
                raise ValidationError({'ativo':'Já existe um trimestre ativo. Desative-o antes de ativar este.'})                

    def __str__(self):
        return self.livro


class Turma(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField()
    ativo = models.BooleanField(default=True)
    material = models.FileField(upload_to='materiais/', blank=True, null=True, storage=protegido ,validators=[FileExtensionValidator(['pdf'])])

    def __str__(self):
        return self.nome


@receiver(post_delete, sender=Turma)
def material_apagado(sender, instance, **kwargs):
    if instance.material:
        instance.material.delete(save=False)
