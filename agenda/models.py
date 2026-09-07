from django.db import models

class AgendaSemanal(models.Model):

    class DiaDaSemana(models.IntegerChoices):
        DOMINGO = (0, 'Domingo')
        SEGUNDA = (1, 'Segunda') 
        TERCA = (2, 'Terça')
        QUARTA = (3, 'Quarta')
        QUINTA = (4, 'Quinta')
        SEXTA = (5, 'Sexta')
        SABADO = (6, 'Sábado')

    dia = models.IntegerField(choices=DiaDaSemana.choices)
    horario =models.TimeField()
    evento = models.CharField(max_length=50)

    class Meta:
        ordering = ['dia', 'horario']
        verbose_name = 'Agenda Semanal'
        verbose_name_plural = 'Agenda Semanal'

    def __str__(self):
        return self.evento
    
class AgendaMensal(models.Model):
    data = models.DateTimeField()
    culto = models.CharField(max_length=50)
   
    class Meta:
        ordering = ['data']
        verbose_name = 'Agenda Mensal'
        verbose_name_plural = 'Agenda Mensal'

    def __str__(self):
        return self.culto
    
    