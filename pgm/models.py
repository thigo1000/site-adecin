from django.db import models
from comum.imagens import redimensionar


class Pgm(models.Model):

    class DiaDaSemana(models.IntegerChoices):
        DOMINGO = (0 ,'Domingo')
        SEGUNDA = (1, 'Segunda')
        TERCA = (2, 'Terça')
        QUARTA = (3, 'Quarta')
        QUINTA = (4, 'Quinta')
        SEXTA = (5, 'Sexta')
        SABADO = (6, 'Sábado')

    nome = models.CharField(max_length= 50)
    bairro = models.CharField(max_length=50)
    dia = models.IntegerField(choices=DiaDaSemana.choices)
    horario = models.TimeField(help_text='modelo (20:00)')
    foto = models.ImageField(upload_to='pgm/')
    lider = models.CharField(max_length=100)
    contato = models.CharField(max_length=20, help_text='Número com país e DDD, só dígitos. Ex.: 5521987654321')
    ativo = models.BooleanField(default=True)

    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        redimensionar(self.foto.path, 800, 800)


    def __str__(self):
        return self.nome

    class Meta:
        ordering = ['nome', 'bairro']