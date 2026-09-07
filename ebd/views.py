from django.shortcuts import render
from ebd.models import Tema, Turma
import os
from django.http import FileResponse, Http404
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required


@login_required
def material_turma(request, id):
    turma = get_object_or_404(Turma, id=id)

    if not turma.material:
        raise Http404

    return FileResponse(
        turma.material.open('rb'),
        content_type='application/pdf',
        filename=os.path.basename(turma.material.name),
    )


def ebd(request):
    tema = Tema.objects.filter(ativo=True).first()
    turma = Turma.objects.filter(ativo=True)
    return render(request, 'ebd.html', {
        'tema': tema,
        'turmas': turma
    })
