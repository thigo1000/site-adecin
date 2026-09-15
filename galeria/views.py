from datetime import date
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, render
from galeria.models import Album, Colecao


def _por_data(item):
    return item['data'] or date.min


def galeria(request):
    itens = []

    for atual in Colecao.objects.filter(ativo=True):
        itens.append({
            'tipo': 'colecao',
            'obj': atual,
            'data': atual.data(),
            'capa': atual.capa(),
            'quantidade': atual.quantidade_albuns(),
        })

    for atual in Album.objects.filter(colecao__isnull=True):
        itens.append({
            'tipo': 'album',
            'obj': atual,
            'data': atual.data,
            'capa': atual.capa,
            'quantidade': atual.quantidade_fotos(),
        })

    itens.sort(key=_por_data, reverse=True)

    paginator = Paginator(itens, 9)
    pagina = paginator.get_page(request.GET.get('page'))

    return render(request, 'midia_lista.html', {'itens': pagina})


def colecao(request, id):
    atual = get_object_or_404(Colecao, id=id, ativo=True)

    paginator = Paginator(atual.albuns.order_by('-data'), 9)
    pagina = paginator.get_page(request.GET.get('page'))

    return render(request, 'midia_colecao.html', {
        'colecao': atual,
        'albuns': pagina,
    })


def album(request, id):
    atual = get_object_or_404(Album, pk=id)

    return render(request, 'midia_album.html', {
        'album': atual,
        'fotos': atual.fotos.all(),
        'videos': atual.videos.all(),
    })