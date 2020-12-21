from .views import *
from django.urls import path, include


urlpatterns = [
    # Paciente Urls    
    path('paciente/pagina-inicial/', home_paciente, name="home_paciente"),
    path('paciente/cartao-vacina/',include('cartaoVacina.urls')),
    path('paciente/agendar-vacina/pesquisa/', agendarvacina, name="agendavacina"),
    path('paciente/agendar-vacina/unidade-de-saude/<pk>', escolhervacina, name="escolhevacina"),
    path('paciente/logout/', deslogar_user, name="deslogar"),

    # Profissional 
    path('profissional-saude/pagina-inicial/', home_profissional, name = "home_profissional"),
    path('profissional-saude/aprovar-agendamento/<pk>', aprovarAgendamento, name="aprovaragendamento"),
    path('profissional-saude/estoque-vacinas/', estoquevacinas, name="estoquevacinas"),
    path('profissional-saude/estoque-vacinas/<pk>', estoqueVacina, name="estoqueVacina"),
    path('profissional-saude/agendamento-vacina/<pk>', agendamentovacina, name = "agendamentovacina"),
    path('profissional-saude/periodo-vacina/', periodovacina, name="periodovacina"),
    path('profissional-saude/logout/', deslogar_user, name="deslogar"),



    # Coordenador 
    path('coordenador-sus/pagina-inicial/', home_coordenador, name= "home_coordenador"),
    path('coordenador-sus/cadastrar-unidade-saude/', cadastrarUS, name="cadastrarUS"),
    path('coordenador-sus/cadastrar-vacina-us/', cadastroVacinaUS, name= "cadastrarVacinaUS"),
    path('coordenador-sus/vinculo-profissional-saude/<pk>', vinculoProfissionalUS, name="vinculoprofissionalUS"),
    path('coordenador-sus/cadastrar-profissional-saude/', cadastroProfissional, name = "cadastrarProfissional"),
    path('coordenador-sus/relatorio/<pk>', relatorioUS, name="relatorioUS"),
    path('coordenador-sus/logout/', deslogar_user, name="deslogar"),

]
