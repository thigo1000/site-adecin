from django.db import models
from comum.imagens import redimensionar
from django.db.models.signals import post_delete
from django.dispatch import receiver


class Colecao(models.Model):
    nome = models.CharField(max_length=50)
    descricao = models.CharField(max_length=120, blank= True)
    ativo = models.BooleanField(default=False)

    def quantidade_albuns(self):
        return self.albuns.count()

    def album_recente(self):
        return self.albuns.order_by('-data').first()

    def capa(self):
        album = self.album_recente()
        return album.capa if album else None

    def data(self):
        album = self.album_recente()
        return album.data if album else None

    def __str__(self):
        return self.nome


class Album(models.Model):
    nome = models.CharField(max_length=100)
    capa = models.ImageField(upload_to='capas/', blank=False)
    criado_em = models.DateTimeField(auto_now_add=True)
    data = models.DateField(null=True, blank=True)
    colecao = models.ForeignKey(Colecao, on_delete=models.PROTECT, related_name='albuns', null=True, blank=True)

    
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


@receiver(post_delete, sender=Album)
def album_apagado(sender, instance, **kwargs):
    if instance.capa:
        instance.capa.delete(save=False)

@receiver(post_delete, sender=Foto)
def foto_apagada(sender, instance, **kwargs):
    if instance.imagem:
        instance.imagem.delete(save=False)