from django.shortcuts import render
from .forms import *
from .models import *
from digitalSus.settings import DEFAULT_FROM_EMAIL
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from usuarios.decorators import *

@login_required(login_url='/login')
@paciente_user
def cadastrarVacinaPaciente(request):
    context = {}
    context['valido'] = False
    if request.method == 'POST':
        form = vacina_paciente(request.POST)
        
        if form.is_valid():
            formulario = form.save(commit=False)
            paciente = request.user.perfil_paciente
            formulario.paciente = paciente
            formulario.sus = False
            formulario.save()
            context['valido'] = True
            form = vacina_paciente()

            subject = "Vacina Adicionada Ao Seu Cartão de Vacinas"
            message = "Olá "+ request.user.perfil_paciente.nome+"! \n A vacina que você cadastrou já está disponivel no seu cartão de vacinas!!" 
            email = request.user.perfil_paciente.email

            send_mail(subject, message,DEFAULT_FROM_EMAIL, [email], fail_silently= False )

        
    else:
        paciente = request.user.perfil_paciente
        form = vacina_paciente()

    context['form'] = form
    return render(request, 'paciente_cadastrarVacina.html', context)

@login_required(login_url='/login')
@paciente_user
def cartaovacina(request):
    context = {}

    context['vacinas'] = VacinaPaciente.objects.filter(paciente=request.user.perfil_paciente)


    return render(request, 'paciente_cartaovacina.html', context)