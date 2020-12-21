from django.http import HttpResponse
from django.shortcuts import redirect
from .models import *

## Essas funções vão ser responsaveis por verifica se o usuario certo está acessando sua views
def paciente_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.perfil_paciente:
            return view_func(request, *args, **kwargs)
        elif request.user.perfil_profissional:
            return redirect('home_profissional')
        elif request.user.perfil_coordenador:
            return redirect('home_coordenador')
        
    return wrapper_func

def profissional_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.perfil_profissional:
            return view_func(request, *args, **kwargs)
        elif request.user.perfil_paciente:
            return redirect('home_paciente')
        elif request.user.perfil_coordenador:
            return redirect('home_coordenador')
        
    return wrapper_func

def coordenador_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.perfil_coordenador:
            return view_func(request, *args, **kwargs)
        elif request.user.perfil_profissional:
            return redirect('home_profissional')
        elif request.user.perfil_paciente:
            return redirect('home_paciente')
        
    return wrapper_func

# Essa função impede o usuário de acessar a página de login caso esteja logado, sempre direcionadno para a home!!
def user_autenticado(view_func):
    def wrapper_func(request, *args, **kwargs):
        user = request.user 

        if user.is_authenticated:
            if user.perfil_paciente:
                return redirect('home_paciente')
            elif user.perfil_profissional:
                return redirect('home_profissional')
            elif user.perfil_coordenador:
                return redirect('home_coordenador')

            
        else:
            return view_func(request, *args, **kwargs)
            
    return wrapper_func
