from django.forms import ModelForm
from django import forms
from usuarios.models import Paciente, Profissional
from administrativo.models import UnidadeSaude, VacinaUS

class UserRegister(ModelForm):
    class Meta:
        model = Paciente
        fields = ['nome','email','cpf','cel']

        widgets = {
            'nome': forms.TextInput(attrs={'type':'text','required':'True', 'class':'form-control', 'style':'width: 600px;' }),
            'email': forms.TextInput(attrs={'type':'email','required':'True', 'class':'form-control', 'style':'width: 600px;'}),
            'cpf': forms.TextInput(attrs={'type':'text','required':'True', 'class':'form-control', 'style':'width: 600px;'}),
            'cel': forms.TextInput(attrs={'type':'text','required':'True', 'class':'form-control', 'style':'width: 600px;'}),
        }

class ProfissionalRegister(ModelForm):
    class Meta:
        model = Profissional 
        fields = ['nome','email','cpf','cel','unidade_saude']

class cadastroUS(ModelForm):
    class Meta:
        model = UnidadeSaude
        fields = ['nome','endereco','cidade','uf']



class cadastrarVacinaUS(ModelForm):
    class Meta:
        model = VacinaUS
        fields = ['nome','unidade_saude','qt_vacinas','qt_vacinas_aplicadas']

        widgets = {
            'qt_vacinas': forms.TextInput(attrs ={'type':'number'})
        }

        


