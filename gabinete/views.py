from django.shortcuts import render, redirect, get_object_or_404
from gabinete.models import Agendamento, Gabinete, Janela
from datetime import datetime
from urllib.parse import quote
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.views.decorators.http import require_POST


def _membro_de(request):
    return getattr(request.user, 'membro', None)


def _link_whatsapp(agendamento, membro):
    gabinete = Gabinete.objects.first()

    if gabinete is None:
        return None

    data = agendamento.data.strftime('%d/%m')
    hora = agendamento.horario.strftime('%Hh')

    texto = (
        f'Olá, Pastor. Sou {membro.nome} e agendei um horário '
        f'no gabinete para o dia {data}, às {hora}.'
    )

    return f'https://wa.me/{gabinete.telefone}?text={quote(texto)}'


def _monta_dias(hoje):
    janelas = Janela.objects.filter(data__gte=hoje)

    ocupados = set(
        Agendamento.objects
        .filter(
            data__gte=hoje,
            status__in=[Agendamento.Status.ATIVO, Agendamento.Status.CANCELADO_PASTOR],
        )
        .values_list('data', 'horario')
    )

    dias = []

    for janela in janelas:
        vagas = [
            {'hora': hora, 'livre': (janela.data, hora) not in ocupados}
            for hora in janela.horarios()
        ]

        if not vagas:
            continue

        bloco = {'inicio': janela.inicio, 'fim': janela.fim, 'vagas': vagas}

        if dias and dias[-1]['data'] == janela.data:
            dias[-1]['blocos'].append(bloco)
        else:
            dias.append({'data': janela.data, 'blocos': [bloco]})

    return [dia for dia in dias if any(
        vaga['livre'] for bloco in dia['blocos'] for vaga in bloco['vagas']
    )]


@login_required
def gabinete(request):
    membro = _membro_de(request)

    if membro is None:
        messages.error(request, 'Sua conta ainda não está ligada a um cadastro de membro.')
        return redirect('index')

    hoje = timezone.now().date()

    agendamento = Agendamento.objects.filter(
        membro=membro,
        data__gte=hoje,
        status=Agendamento.Status.ATIVO,
    ).first()

    cancelado = Agendamento.objects.filter(
        membro=membro,
        data__gte=hoje,
        status=Agendamento.Status.CANCELADO_PASTOR,
    ).first()

    if request.method == 'POST' and agendamento is None:
        quando = request.POST.get('quando', '')

        try:
            marcado = datetime.strptime(quando, '%Y-%m-%dT%H:%M')
        except ValueError:
            messages.error(request, 'Escolha um horário para continuar.')
            return redirect('gabinete')

        novo = Agendamento(
            membro=membro,
            data=marcado.date(),
            horario=marcado.time(),
            motivo=request.POST.get('motivo', '').strip(),
        )

        try:
            novo.full_clean()
        except ValidationError as erro:
            for mensagem in erro.messages:
                messages.error(request, mensagem)
            return redirect('gabinete')

        novo.save()
        messages.success(request, 'Horário confirmado.')
        return redirect('gabinete')

    if agendamento is not None:
        return render(request, 'gabinete.html', {
            'agendamento': agendamento,
            'whatsapp': _link_whatsapp(agendamento, membro),
            'cancelado': cancelado,
        })

    return render(request, 'gabinete.html', {
        'dias': _monta_dias(hoje),
        'cancelado': cancelado,
    })


@login_required
@require_POST
def cancelar_gabinete(request, id):
    membro = _membro_de(request)
    agendamento = get_object_or_404(Agendamento, id=id, membro=membro)

    if not agendamento.pode_cancelar():
        messages.error(request, 'Faltam menos de 24 horas. Fale com a secretaria.')
        return redirect('gabinete')

    agendamento.status = Agendamento.Status.CANCELADO_MEMBRO
    agendamento.save()

    messages.success(request, 'Horário cancelado.')
    return redirect('gabinete')