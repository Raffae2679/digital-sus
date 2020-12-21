from .views import *
from django.urls import path, include


urlpatterns = [
    # Cartão de Vacina Urls
    path('', cartaovacina, name = "cartao-vacina"),
    path('cadastrar-vacina/',cadastrarVacinaPaciente, name="cadastrar-vacina-paciente"),
]
