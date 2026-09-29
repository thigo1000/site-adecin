from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
from usuario.models import Membro
from django.db.models import Q
from datetime import datetime, timedelta

class Gabinete(models.Model):
    nome = models.CharField(max_length=70)
    telefone = models.CharField(max_length=13, help_text='número com país e DD Ex:5521987654321')

    def __str__(self):
        return self.nome


class Janela(models.Model):

    data = models.DateField() 
    inicio = models.TimeField()
    fim = models.TimeField()

    class Meta:
        ordering = ['data', 'inicio']

    def clean(self):
        if not (self.data and self.inicio and self.fim):
            return  

        if self.fim <= self.inicio:
            raise ValidationError({'fim': 'O fim precisa ser depois do início.'})

        duracao = datetime.combine(self.data, self.fim) - datetime.combine(self.data, self.inicio)
        if duracao < timedelta(hours=1):
            raise ValidationError({'fim': 'A janela precisa ter pelo menos 1 hora.'})

        vizinhas = Janela.objects.filter(data=self.data, inicio__lt=self.fim, fim__gt=self.inicio).exclude(pk=self.pk)

        if vizinhas.exists():
            raise ValidationError('Já existe uma janela nesse intervalo.')

    def horarios(self):
        vagas = []
        atual = datetime.combine(self.data, self.inicio)
        fim = datetime.combine(self.data, self.fim)

        while atual + timedelta(hours=1) <= fim:
            vagas.append(atual.time())
            atual += timedelta(hours=1)

        return vagas

    def __str__(self):
        return f'{self.data} · {self.inicio} às {self.fim}'
 
 
class Agendamento(models.Model):

    class Status(models.TextChoices):
        ATIVO = ('ativo', 'Ativo')
        CANCELADO_PASTOR = ('cancelado_pastor', 'Cancelado pelo Pastor')
        CANCELADO_MEMBRO = ('cancelado_membro', 'Cancelado pelo Membro')

    membro = models.ForeignKey(Membro,on_delete=models.CASCADE,related_name='agendamentos',)
    data = models.DateField()
    horario = models.TimeField()
    motivo = models.TextField(blank=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.ATIVO)
    motivo_cancelamento = models.CharField(max_length=200, blank=True)


    class Meta:
        ordering = ['data', 'horario']
        constraints = [models.UniqueConstraint(fields=['data', 'horario'], condition=Q(status__in=['ativo','cancelado_pastor']), name='um_agendamento_por_horario')]
 
    def clean(self):
        dentro = Janela.objects.filter(data=self.data, inicio__lte=self.horario,fim__gt=self.horario).exists()
 
        if not dentro:
            raise ValidationError({'horario': 'Esse horário não está aberto para atendimento.'})
 
        ocupado = Agendamento.objects.filter(data=self.data, horario=self.horario, status__in=[self.Status.ATIVO, self.Status.CANCELADO_PASTOR]).exclude(pk=self.pk).exists()
 
        if ocupado:
            raise ValidationError({'horario': 'Esse horário já foi agendado.'})

        if self._state.adding and self.data and self.horario:
            if self.inicio() <= timezone.now():
                raise ValidationError({'horario': 'Esse horário já passou. Escolha outro.'})

        if self.membro_id and self.status == self.Status.ATIVO:
            outro = Agendamento.objects.filter(membro=self.membro, data__gte=timezone.localdate(), status=self.Status.ATIVO).exclude(pk=self.pk).exists()

            if outro:
                raise ValidationError('Você já tem um horário marcado. Cancele antes de agendar outro.')
 
    def inicio(self):
        return timezone.make_aware(datetime.combine(self.data, self.horario))

    def pode_cancelar(self):
        return self.inicio() - timezone.now() > timedelta(hours=24)
     
    def __str__(self):
        return f'{self.membro.nome} · {self.data} às {self.horario}'