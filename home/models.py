from django.db import models
from comum.imagens import redimensionar 


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
        