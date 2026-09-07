from django.shortcuts import render
from agenda.models import AgendaMensal, AgendaSemanal


def agenda(request):
    dados = AgendaSemanal.objects.all()
    datas = AgendaMensal.objects.all()

    return render(request, 'agenda.html',
            {
                'dados': dados,
                'datas': datas
            })