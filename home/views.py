from django.shortcuts import render
from django.utils import timezone
from django.db.models import Q
from home.models import Anuncio

def index(request):
    hoje = timezone.now().date()
    anuncios = Anuncio.objects.filter(Q(expira_em__gte=hoje) | Q(expira_em__isnull=True), ativo=True)

    return render(request, 'index.html', {'anuncios': anuncios})