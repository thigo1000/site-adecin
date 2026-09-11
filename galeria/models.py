from django.db import models
from comum.imagens import redimensionar


class Album(models.Model):
    nome = models.CharField(max_length=100)
    capa = models.ImageField(upload_to='capas/', blank=False)
    criado_em = models.DateTimeField(auto_now_add=True)
    data = models.DateField(null=True, blank=True)

    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        redimensionar(self.capa.path, 800, 800)

    def quantidade_fotos(self):
        return self.fotos.count()

    def __str__(self):
        return self.nome


class Foto(models.Model):
    album = models.ForeignKey(Album, on_delete=models.CASCADE, related_name='fotos')
    imagem = models.ImageField(upload_to='fotos/')

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        redimensionar(self.imagem.path, 1600, 1600)
        
    def __str__(self):
        return f'Foto de {self.album.nome}'
    
class Video(models.Model):
    album = models.ForeignKey(Album, on_delete=models.CASCADE, related_name='videos')
    titulo = models.CharField(max_length=100)
    youtube_id = models.CharField(max_length=100, blank= True)
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titulo