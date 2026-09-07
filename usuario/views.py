from django.shortcuts import render, redirect
from usuario.forms import VerificadorForms, CadastroForms
from usuario.models import Membro
from django.contrib import messages


def verificador(request):

    form = VerificadorForms()
    

    if request.method == 'POST':
        form = VerificadorForms(request.POST)

        if form.is_valid():
            cpf = form.cleaned_data['cpf']
            membro = Membro.objects.filter(cpf=cpf).first()

            if membro is None:
                messages.error(request, 'CPF não se encontra na nossa lista de membros')
                return render(request, 'usuario/verificar.html', {'form': form})

            if membro.usuario is not None:
                messages.error(request, 'Este CPF já tem uma conta cadastrada.')
                return  redirect('login')
            

            request.session['membro_id'] = membro.id
            return redirect('cadastro')        
    
    return render(request, 'usuario/verificar.html', {'form': form})


def cadastro(request):
    membro_id = request.session.get('membro_id')

    if membro_id is None:
        return redirect('verificador')

    membro = Membro.objects.filter(id=membro_id).first()

    if membro is None or membro.usuario is not None:
        del request.session['membro_id']
        return redirect('verificador')

    form = CadastroForms()

    if request.method == 'POST':
        form = CadastroForms(request.POST)

        if form.is_valid():
            usuario = form.save()

            membro.usuario = usuario
            membro.save()

            del request.session['membro_id']

            messages.success(request, 'Acesso criado. Agora é só entrar.')
            return redirect('login')

    return render(request, 'usuario/cadastro.html', {'form': form})