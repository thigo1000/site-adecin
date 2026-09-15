from django.db import models
from comum.imagens import redimensionar
from django.db.models.signals import post_delete
from django.dispatch import receiver


class Anuncio(models.Model):
    titulo = models.CharField(max_length=50)
    imagem = models.ImageField(upload_to='anuncios/')
    ordem = models.IntegerField(default=0)
    ativo = models.BooleanField(default=True)
    expira_em = models.DateField(null=True, blank=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['ordem', '-criado_em']

    def __str__(self):
        return self.titulo

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        redimensionar(self.imagem.path, 1600, 900)


@receiver(post_delete, sender=Anuncio)
def anuncio_apagado(sender, instance, **kwargs):
    if instance.imagem:
        instance.imagem.delete(save=False)