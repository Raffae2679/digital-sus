from django.db import models

# Create your models here.

""" Unidade_Saude:
    nome 
    endereco
    uf 
    cidade
    numero

Vacina_US:
    ForeignKey com a unidade de saude
    quantidade de vacinas
    nome da vacina 
    quantidade aplicada  """

class UnidadeSaude(models.Model):
    nome = models.CharField(max_length = 200, verbose_name = 'Nome da unidade de saúde')
    endereco = models.CharField(max_length = 300, verbose_name = 'endereço')
    uf = models.CharField(max_length = 3, verbose_name = 'Sigla da UF da unidade de saúde (ex: RN, SP, AM, AC...)')
    cidade = models.CharField(max_length = 200, verbose_name = 'Cidade da unidade de saúde')

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name 		= 'Unidade de Saúde'
        verbose_name_plural = 'Unidades de Saúde'

class VacinaUS(models.Model):
    nome = models.CharField(max_length = 200, verbose_name = 'Nome da vacina')
    unidade_saude = models.ForeignKey(UnidadeSaude, on_delete = models.CASCADE, verbose_name ="Unidade de saude que vai receber as vacinas", null=True,blank=True)
    qt_vacinas = models.BigIntegerField('Quantidade de vacinas', null=True, blank=True)
    qt_vacinas_aplicadas = models.BigIntegerField('Quantidade de vacinas aplicadas', null=True, blank=True)

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name 		= 'Vacina da Unidade de Saúde'
        verbose_name_plural = 'Vacinas da Unidade de Saúde'


