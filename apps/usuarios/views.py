from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import *
import json
from administrativo.models import *
from Agendamento.models import *
from cartaoVacina.models import *
from django.db.models import Q
from .models import Profissional
from digitalSus.settings import DEFAULT_FROM_EMAIL
from django.core.mail import send_mail
from datetime import date
from django.contrib.auth.decorators import login_required
from .decorators import *

## =-=-=-=-=-=-=-=-=-=-=-=-=-= Views Gerais do Sistema =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
@user_autenticado
def login_user(request):

    if request.method == "POST":
    	form_login = AuthenticationForm(request.POST)
    	
    	username = request.POST["email"]
    	password = request.POST["password"]
    	usuario = authenticate(request, username= username, password=password)
    	if usuario is not None:
            login(request,usuario)
            if request.user.perfil_paciente:
                return redirect('home_paciente')
            elif request.user.perfil_profissional:
                return redirect('home_profissional')
            elif request.user.perfil_coordenador:
                return redirect('home_coordenador')
    else:
        form_login = AuthenticationForm()

    return render(request,'sistema_login.html',{'form_login': form_login})

def deslogar_user(request):
    logout(request)
    return redirect('login')

def cadastroUsuario(request):
    context = {}

    valido = False
    if request.method == 'POST':
        form = UserRegister(request.POST)

        if form.is_valid():
            valido = True
            form.save()

            form = UserRegister()
    else:
        form = UserRegister()

    context['form'] = form
    context['valido'] = valido
    return render(request, 'sistema_cadastrarpaciente.html', context)

## =-=-=-=-=-=-=-=-=-=-=-=- Fim das views gerais =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

## =-=-=-=-=-=-=-=-=-=-=-=- Views do Paciente =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-==

@login_required(login_url='/login')
@paciente_user
def home_paciente(request):
    context = {}

    agendamentos = AgendarVacina.objects.filter(paciente = request.user.perfil_paciente)
    vacinas = VacinaPaciente.objects.filter(paciente = request.user.perfil_paciente).order_by('-data_aplicacao')[:3]

    context['agendamentos'] = agendamentos
    context['vacinas'] = vacinas

    return render(request, 'paciente_home.html', context)

@login_required(login_url='/login')
@paciente_user
def agendarvacina(request):
    context = {}

    context['options'] = UnidadeSaude.objects.all()

    if request.method == 'POST':
        print("Entrou aqu")
        pesquisa = request.POST['pesquisa']

        query = Q(uf=pesquisa) | Q(cidade=pesquisa)

        context['unidade'] = UnidadeSaude.objects.filter(query)

        return render(request, 'paciente_agendarvacina.html', context)
 



    context['unidade'] = UnidadeSaude.objects.all()

    return render(request, 'paciente_agendarvacina.html', context)

@login_required(login_url='/login')
@paciente_user
def escolhervacina(request,pk):
    context = {}

    valido = False
    
    us = UnidadeSaude.objects.get(pk=pk)
    vacinas = VacinaUS.objects.filter(unidade_saude=us)
    periodo_vac = PeriodoVacina.objects.filter(unidade_saude=us)

    if request.method == 'POST':
        valido = True
        date = request.POST['date']
        vacpk = request.POST['vacinas']
        turno = request.POST['turno']


        vacina = VacinaUS.objects.get(pk=vacpk)
        

        agendamento = AgendarVacina.objects.create(paciente= request.user.perfil_paciente, unidade_saude= us, vacina= vacina,
        data_agendada= date, pos_fila=0, turno= turno )
        agendamento.save()

        # Reduz a quantidade de vacinas quando é agendado uma nova vacina
        num =  int(vacina.qt_vacinas)
        num-=1
        vacina.qt_vacinas = num
        vacina.save()

        
        


    context['us'] = us
    context['vacina'] = vacinas
    context['periodo'] = periodo_vac
    context['valido'] = valido


    return render(request,'paciente_us_vacina.html', context)


## =-=-=-=-=-=-=-=-=-=-=-=-= Fim das views do paciente =-=--=-=-=-=-=-=-=-=-=-=-=-=-==


## =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-= Views do Coordenador do SUS =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

@login_required(login_url='/login')
@coordenador_user
def home_coordenador(request):
    context = {}

    us = UnidadeSaude.objects.all()
    us2 = UnidadeSaude.objects.all().order_by('uf')
    profissionais = Profissional.objects.all()

    ufs = []

    for i in us2:
        ufs.append(i.uf)
    
    ufs = set(ufs)
    print(ufs)
    context['us'] = us
    context['profissional'] = profissionais
    context['ufs'] = ufs 
    return render(request, 'coordenador_home.html', context)


    ## Views de cadastro das unidades de saude
@login_required(login_url='/login')
@coordenador_user
def cadastrarUS(request):
    context = {}

    valido = False
    if request.method == 'POST':
        form = cadastroUS(request.POST)

        if form.is_valid():
            valido = True
            form.save()

            form = cadastroUS()
    else:
        form = cadastroUS()

    context['form'] = form
    context['valido'] = valido

    return render(request, 'coordenador_cadastrarUS.html', context)

    ## Views de cadastro de vacinas das unidades de saude
@login_required(login_url='/login')
@coordenador_user
def cadastroVacinaUS(request):
    context = {}

    valido = False
    if request.method == 'POST':
        form = cadastrarVacinaUS(request.POST)
        
        if form.is_valid():
            
            formulario = form.save(commit=False)

            formulario.qt_vacinas = 0
            formulario.qt_vacinas_aplicadas = 0

            us = UnidadeSaude.objects.get(pk=request.POST['unidades'])
            formulario.unidade_saude = us

            valido = True
            formulario.save()

            form = cadastrarVacinaUS()
    else:
        form = cadastrarVacinaUS()

    context['form'] = form
    context['valido'] = valido
    context['us'] = UnidadeSaude.objects.all()
    
    return render(request, 'coordenador_cadastrarVacinaUS.html', context)

    ## Views para atualizar informações do profissional
@login_required(login_url='/login')
@coordenador_user
def vinculoProfissionalUS(request,pk):
    context = {}

    profissional = Profissional.objects.get(pk=pk)

    valido = False
    if request.method == 'POST':
        valido = True
        vinculo = request.POST['unidades']
        vinculo_us = UnidadeSaude.objects.get(pk=vinculo)
        profissional.unidade_saude = vinculo_us

        profissional.save()


    
    context['valido'] = valido
    context['profissional'] = profissional
    context['us'] = UnidadeSaude.objects.all()
    
    return render(request, 'coordenador_vinculoProfissionalUS.html', context)

    ## Views de cadastro do profissional da saúde
@login_required(login_url='/login')
@coordenador_user
def cadastroProfissional(request):
    context = {}

    valido = False
    if request.method == 'POST':
        form = ProfissionalRegister(request.POST)

        if form.is_valid():
            print("Nao entrou aqui né")
            valido = True
            formulario = form.save(commit=False)

            us = UnidadeSaude.objects.get(pk=request.POST['unidades'])
            formulario.unidade_saude = us


            formulario.save()

            form = ProfissionalRegister()
    else:
        form = ProfissionalRegister()

    context['form'] = form
    context['valido'] = valido
    context['us'] = UnidadeSaude.objects.all()
    return render(request, 'coordenador_cadastrarProfissional.html', context)

@login_required(login_url='/login')
@coordenador_user
def relatorioUS(request, pk):
    context = {}

    dados = []
    nomes = []

    us = UnidadeSaude.objects.get(pk=pk)
    vacinas = VacinaUS.objects.filter(unidade_saude=us)

    for i in vacinas:
        nomes.append(i.nome)
        dados.append(i.qt_vacinas_aplicadas)


    context['us'] = us
    context['data'] = json.dumps(dados)
    context['labels'] = json.dumps(nomes)
    return render(request, 'coordenador_relatorio.html', context)
## =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-= Fim das Views do Coordenador do SUS =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-==-=



## =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-= Views do Profissional da Saúde =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-= 

@login_required(login_url='/login')
@profissional_user
def home_profissional(request):
    context = {}
    datas = []
    agendamentos = AgendarVacina.objects.filter(unidade_saude = request.user.perfil_profissional.unidade_saude).order_by('-data_agendada')
    periodo = PeriodoVacina.objects.filter(unidade_saude = request.user.perfil_profissional.unidade_saude)
    

    for i in agendamentos:
        datas.append(i.data_agendada)
    
    
    
    
    context['agendamentos'] = agendamentos
    context['diasAgendados'] = AgendarVacina.objects.filter(unidade_saude = request.user.perfil_profissional.unidade_saude).order_by('turno').order_by('pos_fila')
    context['datas'] = set(datas)
    context['periodo'] = periodo
    return render(request, 'profissional_home.html',context)

    ## Views onde é feito a lógica de aprovar o agendamento + enviar o email de confirmação pro paciente
@login_required(login_url='/login')
@profissional_user
def aprovarAgendamento(request,pk):
    context = {}

    agen = AgendarVacina.objects.filter(pk=pk)[0]

    if request.POST.get('yes'):
        agen.agendamento_stts = True
        
        subject = "Agendamento da Vacina Aprovado"
        message = "Olá "+ agen.paciente.nome+"! \n Seu agendamento da "+agen.vacina.nome+" no estabelecimento de saude "+ agen.unidade_saude.nome+", foi aprovado! \n" 
        email = agen.paciente.email

        send_mail(subject, message, DEFAULT_FROM_EMAIL, [email], fail_silently= False )


        lista_agendamentos = AgendarVacina.objects.filter(agendamento_stts=True).filter(vacina_aplicada=False).filter(data_agendada=agen.data_agendada).filter(turno = agen.turno)

        print(len(lista_agendamentos))

        if len(lista_agendamentos) == 0:
            agen.pos_fila = 1
            #salva
        else:
            agen.pos_fila = len(lista_agendamentos) +1 
            print(agen.pos_fila)
        
        agen.save()


        return redirect('home_profissional')

    if request.POST.get('no'):
        subject = "Agendamento da Vacina Recusado"
        message = "Olá "+ agen.paciente.nome+"! \n Seu agendamento da "+agen.vacina.nome+" no estabelecimento de saude "+ agen.unidade_saude.nome+", foi recusado! \n Pedimos que tente agendar novamente!!!" 
        email = agen.paciente.email

        send_mail(subject, message, DEFAULT_FROM_EMAIL, [email], fail_silently= False )        
        agen.delete()

        vac = VacinaUS.objects.get(nome=agen.vacina.nome)

        vac.qt_vacinas = vac.qt_vacinas +1
        vac.save()

        return redirect('home_profissional')    

    context['agen'] = agen
    return render(request, 'profissional_aprovarAgendamento.html', context)

    ## Views com a listagem das vacinas da unidade de saude do profissional
@login_required(login_url='/login')
@profissional_user
def estoquevacinas(request):
    context = {}

    vacinas = VacinaUS.objects.filter(unidade_saude = request.user.perfil_profissional.unidade_saude)

    context['vacinas'] = vacinas
    return render(request, 'profissional_estoquevacinas.html', context)

    ## Views onde é feito a logica de incrementar e decrementar o estoque de vacinas pelo profissional.
@login_required(login_url='/login')
@profissional_user
def estoqueVacina(request,pk):
    context = {}
    valido = False
    vac = VacinaUS.objects.get(pk=pk)
    
    if request.POST.get('qt_vacinas'):
        valido = True
        n_vac = request.POST['qt_vacinas']
        vac.qt_vacinas = n_vac
        vac.save()

    context['vac'] = vac
    context['valido'] = valido
    return render(request, 'profissional_estoqueVacina.html', context)

    ## Views que executa a lógica da aplicação da vacina + email enviado ao paciente + adicionando vacina ao cartão do paciente
@login_required(login_url='/login')
@profissional_user
def agendamentovacina(request,pk):
    context = {}

    agendamento = AgendarVacina.objects.get(pk=pk)
    
    

    if request.POST.get('yes'):
        subject = "Confirmação de Vacinação"
        message = "Olá "+ agendamento.paciente.nome+"! \n Sua "+agendamento.vacina.nome+" foi confirmada pelo estabelecimento de saude "+ agendamento.unidade_saude.nome+". \n Sua vacina já se encontra disponivel no seu cartão de vacina." 
        email = agendamento.paciente.email
        send_mail(subject, message, DEFAULT_FROM_EMAIL, [email], fail_silently= False )

        data = date.today()
        vacina_cartao = VacinaPaciente.objects.create(nome= agendamento.vacina.nome, paciente = agendamento.paciente, data_aplicacao=data, sus=True)

        agendamento.vacina_aplicada = True

        agendamento.save()

        lista_agendamentos = AgendarVacina.objects.filter(agendamento_stts=True).filter(vacina_aplicada=False).filter(data_agendada=agendamento.data_agendada).filter(turno = agendamento.turno)

        print(len(lista_agendamentos))

        for i in range(0,len(lista_agendamentos)):
            lista_agendamentos[i].pos_fila = i+1
            lista_agendamentos[i].save()

        
        return redirect('home_profissional')
    
    if request.POST.get('no'):
        vacina = VacinaUS.objects.get(nome=agendamento.vacina.nome)
        
        vacina.qt_vacinas = vacina.qt_vacinas+1
        vacina.save()

        subject = "Ausência no estabelecimento de saúde"
        message = "Olá "+ agendamento.paciente.nome+"! \n Seu agendamento da "+agendamento.vacina.nome+" no estabelecimento de saude "+ agendamento.unidade_saude.nome+" está sendo cancelado devido sua ausência na hora marcada. \n Qualquer coisa, basta acessar o sistema novamente e agendar para um novo dia.!" 
        email = agendamento.paciente.email
        send_mail(subject, message, DEFAULT_FROM_EMAIL, [email], fail_silently= False )    

        agendamento.delete()
        return redirect('home_profissional')     
        



    context['agendamento'] = agendamento
    return render(request, 'profissional_agendamentoVacina.html', context)

    ## Views para visualizar e cadastrar novos dias para agendamento de vacinas
@login_required(login_url='/login')
@profissional_user
def periodovacina(request):
    context = {}

    valido = False

    periodo = PeriodoVacina.objects.filter(unidade_saude=request.user.perfil_profissional.unidade_saude)
    
    if request.method == 'POST':
        valido = True
        date = request.POST['date']
        turno = request.POST['turno']
        us = request.user.perfil_profissional.unidade_saude

        per_vac = PeriodoVacina.objects.create(data=date, turno=turno, unidade_saude=us)
        per_vac.save()

    context['valido'] = valido
    context['periodo'] = periodo
    return render(request, 'profissional_cadastrarperiodovacina.html', context)