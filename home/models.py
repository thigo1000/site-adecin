from django.db import models
from PIL import Image

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
        imagem = Image.open(self.imagem.path)
        imagem.thumbnail((1600, 900))
        imagem.save(self.imagem.path)