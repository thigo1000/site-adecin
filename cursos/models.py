from django.db import models
from django.core.validators import FileExtensionValidator
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from comum.imagens import redimensionar
from django.db.models.signals import post_delete
from django.dispatch import receiver


protegido = FileSystemStorage(location=settings.ARQUIVOS_PROTEGIDOS)

class Curso(models.Model):  

    class Acesso(models.TextChoices):
        PUBLICO = ('publico', 'Público')
        RESTRITO = ('restrito', 'Restrito')
        MEMBRO = ('membro', 'Membro')

    acesso = models.CharField(max_length=20,choices=Acesso.choices,default=Acesso.MEMBRO,)
    aviso = models.CharField(max_length=200, blank=True, help_text='Aparece só em curso restrito. Ex.: Este curso é para o time de audiovisual.',)
    curso = models.CharField(max_length=100)
    resumo = models.CharField(max_length=150)
    capa = models.ImageField(upload_to='capas/curso/')
    criado_em = models.DateTimeField(auto_now_add=True)
    ativo = models.BooleanField(default=False)  
    slug =models.SlugField(unique=True)
    liberados = models.ManyToManyField(settings.AUTH_USER_MODEL,blank=True,related_name='cursos_liberados',)

    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        redimensionar(self.capa.path, 800, 800)


    def pode_ver_curso(self, user):
        if self.acesso == self.Acesso.RESTRITO:
            return user.is_authenticated and self.liberados.filter(pk=user.pk).exists()
        return True

    def pode_ver_aula(self, user, aula):
        if self.acesso == self.Acesso.PUBLICO:
            return True
        
        if self.acesso == self.Acesso.MEMBRO:
            return aula.gratis or user.is_authenticated

        return user.is_authenticated and self.liberados.filter(pk=user.pk).exists()

    def quantidade_aulas(self):
            return self.aulas.count()

    def __str__(self):
        return self.curso


class Aula(models.Model):
    ordem = models.PositiveIntegerField()
    youtube_id = models.CharField(max_length=150)
    titulo = models.CharField(max_length=100)
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE, related_name='aulas')
    duracao = models.PositiveIntegerField(blank=True, null=True)
    gratis = models.BooleanField(default=False)

    class Meta:
        ordering = ['ordem']
        unique_together = ('curso', 'ordem')

    def __str__(self):
        return self.titulo


class Material(models.Model):
    pdf = models.FileField(upload_to='pdf/',storage=protegido ,validators=[FileExtensionValidator(['pdf'])],)
    nome = models.CharField(max_length=100)
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE, related_name='materiais')
    
    def __str__(self):
        return self.nome



@receiver(post_delete, sender=Curso)
def curso_apagado(sender, instance, **kwargs):
    if instance.capa:
        instance.capa.delete(save=False)

@receiver(post_delete, sender=Material)
def material_apagado(sender, instance, **kwargs):
    if instance.pdf:
        instance.pdf.delete(save=False)