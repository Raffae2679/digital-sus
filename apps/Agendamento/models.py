from django.db import models
from administrativo.models import UnidadeSaude, VacinaUS
from usuarios.models import Paciente

# Create your models here.

""" Agendar_Vacina
    ForeignKey com o paciente
    ForeignKey como Unidade de saude
    ForeignKey com a vacina
    Data da solicitação da vacina
    Data escolhida para agendamento

Periodo_Vacina
    Data disponivel para vacinação 
    Turno de vacinação manha/tarde/noite """

class AgendarVacina(models.Model):
    horario = (
        ('Manhã','Manhã'), ('Tarde','Tarde'), ('Noite','Noite')
    )

    paciente = models.ForeignKey(Paciente, on_delete = models.CASCADE, verbose_name ="Paciente que agendou", null = True, blank = True)
    unidade_saude = models.ForeignKey(UnidadeSaude, on_delete = models.CASCADE, verbose_name ="Unidade de saúde que foi escolhida")
    vacina = models.ForeignKey(VacinaUS, on_delete = models.CASCADE, verbose_name ="Vacina escolhida para aplicação")
    data_agendada = models.CharField('Data agendada', max_length = 100,  blank=True, null = True) 
    pos_fila = models.BigIntegerField('Posição do paciente na fila', null=True, blank=True)
    turno = models.CharField('Turno do agendamento', max_length = 100, choices = horario, blank=True, null = True) 
    agendamento_stts = models.BooleanField('Agendamento Aprovado', default= False )
    vacina_aplicada = models.BooleanField('Vacina Aplicada', default= False )


    def __str__(self):
        return self.data_agendada

    class Meta:
        verbose_name 		= 'Agendamento da vacina'
        verbose_name_plural = 'Agendamentos de vacina'

class PeriodoVacina(models.Model):
    horario = (
        ('Manhã','Manhã'), ('Tarde','Tarde'), ('Noite','Noite')
    )

    data = models.DateField( 'Data do dia para vacinação')
    turno = models.CharField('Turno disponivel para vacinação', max_length= 100,  choices = horario)
    unidade_saude = models.ForeignKey(UnidadeSaude, on_delete= models.CASCADE, verbose_name = "Unidade de saúde referente ao periodo de vacina")

    
    def __str__(self):
        return self.unidade_saude.nome

    class Meta:
        verbose_name 		= 'Periodo de vacinação'
        verbose_name_plural = 'Periodos de vacinação'


