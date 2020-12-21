from django.forms import ModelForm
from django import forms
from .models import *

class vacina_paciente(ModelForm):
    class Meta:
        model = VacinaPaciente
        fields = ['nome','paciente','data_aplicacao','sus']


        widgets = {
            'data_aplicacao': forms.TextInput(attrs={'type':'date','required':'True'}),
            'nome': forms.TextInput(attrs={'type':'text','required':'True'})
        }


        