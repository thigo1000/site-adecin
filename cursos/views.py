from django.shortcuts import render, get_object_or_404
from cursos.models import Curso, Aula, Material
import os
from django.http import FileResponse, Http404
from django.contrib.auth.decorators import login_required


@login_required
def material_curso(request, id):
    material = get_object_or_404(Material, id=id)

    if not material.curso.pode_ver_curso(request.user):
        raise Http404

    if not material.pdf:
        raise Http404

    return FileResponse(
        material.pdf.open('rb'),
        content_type='application/pdf',
        filename=os.path.basename(material.pdf.name),
    )


def lista_curso(request):
    cursos = Curso.objects.filter(ativo=True)
    for curso in cursos:
        curso.liberado = curso.pode_ver_curso(request.user)

    return render(request, 'lista_curso.html', {'cursos': cursos})

def detalhe_curso(request, slug, ordem=None):
    curso = get_object_or_404(Curso, slug=slug, ativo=True)
    curso.liberado = curso.pode_ver_curso(request.user)
 
    if not curso.liberado:
        return render(request, 'curso.html', {'curso': curso})
 
    aulas = curso.aulas.all()
    materiais = curso.materiais.all()
 
    if ordem is None:
        aula_atual = aulas.first()
    else:
        aula_atual = get_object_or_404(Aula, curso=curso, ordem=ordem)
 
    if aula_atual is not None:
        aula_atual.liberada = curso.pode_ver_aula(request.user, aula_atual)
    for aula in aulas:
        aula.liberada = curso.pode_ver_aula(request.user, aula)
 
    return render(request, 'curso.html', {
        'curso': curso,
        'aulas': aulas,
        'materiais': materiais,
        'aula_atual': aula_atual,
    })
 