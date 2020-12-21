from django.db import models
from administrativo.models import *
from digitalSus.settings import EMAIL_HOST_USER
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db.models.signals import post_save
from django.dispatch import receiver

class Coordenador(models.Model):
	
    nome = models.CharField(max_length = 200, verbose_name = 'Nome do (a) coordenador (a)')

    username = models.CharField(max_length = 200, verbose_name = 'Apelido do (a) coordenador (a)')

    email = models.EmailField(unique = True, verbose_name = 'E-mail do (a) coordenador (a)')

    cpf	= models.CharField(unique = True, max_length = 25, verbose_name = 'CPF do (a) coordenador (a)')

    cel	= models.CharField(max_length = 25, verbose_name = 'Telefone do (a) coordenador (a)')
	
    def __str__(self):
        return self.nome

    class Meta:
        verbose_name 		= 'Coordenador'
        verbose_name_plural = 'Coordenadores'


class Paciente(models.Model):
	
    nome = models.CharField(max_length = 200, verbose_name = 'Nome do (a) paciente')

    email = models.EmailField(unique = True, verbose_name = 'E-mail do (a) paciente')

    cpf	= models.CharField(unique = True, max_length = 25, verbose_name = 'CPF do (a) paciente')

    cel	= models.CharField(max_length = 25, verbose_name = 'Telefone do (a) paciente')

    # Foreing Key com as vacinas 

	
    def __str__(self):
        return self.nome

    class Meta:
        verbose_name 		= 'paciente'
        verbose_name_plural = 'pacientes'


class Profissional(models.Model):
	
    nome = models.CharField(max_length = 200, verbose_name = 'Nome do (a) profissional')

    email = models.EmailField(unique = True, verbose_name = 'E-mail do (a) profissional')

    cpf	= models.CharField(unique = True, max_length = 25, verbose_name = 'CPF do (a) profissional')

    cel	= models.CharField(max_length = 25, verbose_name = 'Telefone do (a) profissional')

    unidade_saude = models.ForeignKey(UnidadeSaude, on_delete = models.CASCADE, verbose_name ="Unidade de saúde onde o profissional trabalha", null= True, blank=True)
    
	
    def __str__(self):
        return self.nome

    class Meta:
        verbose_name 		= 'Profissional da saúde'
        verbose_name_plural = 'Profissionais da saúde'

# Modelo customizado de cadastro de usuário
class MyAccountManager(BaseUserManager):
	def create_user(self, email, password=None):
		if not email:
			raise ValueError("É necessário um email para realizar o cadastro")

		user  = self.model(
				email=self.normalize_email(email))

		user.set_password(password)
		user.save(using=self._db)
		return user

	def create_superuser(self, email, password):
		user  = self.create_user(
				email=self.normalize_email(email),
				password=password)

		user.is_admin = True
		user.is_staff = True
		user.is_superuser = True
		user.save(using=self._db)

		return user

# Modelo customizado de conta de usuário
class User(AbstractBaseUser):

    email 					= models.EmailField(
								max_length=60, unique = True,
								verbose_name="E-mail do usuário")


    perfil_coordenador		= models.ForeignKey(
								Coordenador, on_delete = models.CASCADE,
								blank = True, null = True,
								verbose_name = 'Perfil do Coordenador')

    perfil_profissional			= models.ForeignKey(
								Profissional, on_delete = models.CASCADE,
								blank = True, null = True,
								verbose_name = 'Perfil do Profissional da Saúde')

    perfil_paciente 		= models.ForeignKey(
								Paciente, on_delete = models.CASCADE,
								blank = True, null = True,
								related_name= "paciente", verbose_name = 'Perfil do Paciente')
	
    date_joined				= models.DateTimeField(
								auto_now_add = True,
								verbose_name = 'Data de Adesão')

    last_login				= models.DateTimeField(
								auto_now = True, verbose_name = 'Último Login')
    
    is_admin				= models.BooleanField(
								default = False, verbose_name = 'Administrador')
    
    is_active				= models.BooleanField(
								default = True, verbose_name = 'Ativo')

    is_staff				= models.BooleanField(
								default = False, verbose_name = 'Staff')
    
    is_superuser			= models.BooleanField(
								default = False, verbose_name = 'Superusuário')

    USERNAME_FIELD = 'email'

    objects = MyAccountManager()
	
    def __str__(self):
        return self.email
	
    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True
    
	
    class Meta:
        verbose_name = 'Usuário'
        verbose_name_plural = 'Usuários'



# Vincula perfil do usuário à conta do usuário
@receiver(post_save, sender = Coordenador or Profissional or Paciente)
def vincula_perfil_ao_usuario(sender, instance, created, **kwargs):
    password= "sus?digital2020?"
    if created:
        if not User.objects.filter(email = instance.email).exists():
            User.objects.create_user(email=instance.email, password=password)

        u = User.objects.get(email = instance.email)

        subject = "Bem vindo ao Digital SUS"
        message = "Sua senha para acessar o sistema é " + password+" . Caso tenha algum problema, por favor entrar em contato." 
        email = u.email

        send_mail(subject, message, EMAIL_HOST_USER, [email], fail_silently= False )

        if sender == Coordenador and u.perfil_coordenador == None:
            u.is_admin= True
            u.perfil_coordenador = instance
	
        elif sender == Profissional and u.perfil_profissional == None:
            u.is_staff = True
            u.perfil_profissional = instance

        elif sender == Paciente and u.perfil_paciente == None:
            u.is_staff = True
            u.perfil_paciente = instance
        
        
        u.save()

lista_senders = [Profissional, Coordenador, Paciente]

for s in lista_senders:
	post_save.connect(vincula_perfil_ao_usuario, sender = s)

