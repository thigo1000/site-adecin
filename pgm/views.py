from django.shortcuts import render
from pgm.models import Pgm


def pgm(request):
    pgms = Pgm.objects.filter(ativo=True)
    bairros = pgms.values_list('bairro', flat=True).distinct()

    return render(request, 'pgm.html', {'pgms': pgms, 'bairros': bairros})