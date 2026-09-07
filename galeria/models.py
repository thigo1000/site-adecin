from django.db import models
from PIL import Image

class Album(models.Model):
    nome = models.CharField(max_length=100)
    capa = models.ImageField(upload_to='capas/', blank=False)
    criado_em = models.DateTimeField(auto_now_add=True)
    data = models.DateField(null=True, blank=True)

    def quantidade_fotos(self):
        return self.fotos.count()

    def __str__(self):
        return self.nome


class Foto(models.Model):
    album = models.ForeignKey(Album, on_delete=models.CASCADE, related_name='fotos')
    imagem = models.ImageField(upload_to='fotos/')

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        imagem = Image.open(self.imagem.path)
        imagem.thumbnail((1600, 1600))
        imagem.save(self.imagem.path)
        
    def __str__(self):
        return f'Foto de {self.album.nome}'
    
class Video(models.Model):
    album = models.ForeignKey(Album, on_delete=models.CASCADE, related_name='videos')
    titulo = models.CharField(max_length=100)
    youtube_id = models.CharField(max_length=100, blank= True)
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titulo