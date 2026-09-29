from django.shortcuts import render
from pgm.models import Pgm


def pgm(request):
    pgms = list(Pgm.objects.filter(ativo=True))
    for g in pgms:
        g.bairro = g.bairro.strip()


    secoes = []
    for valor, rotulo in Pgm.Categoria.choices:
        grupos = [g for g in pgms if g.categoria == valor]
        if grupos:
            secoes.append({
                'valor': valor,
                'rotulo': rotulo,
                'faixa': Pgm.FAIXAS_ETARIAS.get(valor, ''),
                'grupos': grupos,
            })


    sem_categoria = [g for g in pgms if g.categoria not in Pgm.Categoria.values]
    if sem_categoria:
        secoes.append({'valor': 'outros', 'rotulo': 'Outros grupos', 'faixa': '', 'grupos': sem_categoria})

    bairros = sorted({g.bairro for g in pgms}, key=str.casefold)

    return render(request, 'pgm.html', {'secoes': secoes, 'bairros': bairros})