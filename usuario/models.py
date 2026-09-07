from django.db import models
from django.conf import settings


class Membro(models.Model):
    nome = models.CharField(max_length=100)
    cpf = models.CharField(max_length=11, unique=True)
    usuario = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )


    def __str__(self):
        return self.nome