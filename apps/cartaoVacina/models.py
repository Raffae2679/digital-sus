from django.db import models
from usuarios.models import Paciente

# Create your models here.

""" Vacina_Paciente
    nome da vacina
    ForeignKey com o paciente
    data da aplicação
    Boolean Aplicado No SuS T or F """

class VacinaPaciente(models.Model):
    nome = models.CharField(max_length = 200, verbose_name = 'Nome da Vacina')
    paciente = models.ForeignKey(Paciente, on_delete = models.CASCADE, verbose_name ="Paciente que tomou a vacina", null=True, blank=True)
    data_aplicacao = models.DateField('Data de aplicação da vacina', blank = True)
    sus = models.BooleanField('Vacina aplicada no SUS', default= False )

	
    def __str__(self):
        return self.nome

    class Meta:
        verbose_name 		= 'Vacina do Paciente'
        verbose_name_plural = 'Vacinas do Paciente'


