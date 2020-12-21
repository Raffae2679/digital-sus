# 💻 Digital SUS - Sistema de agendamento de vacinas

Sistema desenvolvido durante o processo seletivo para o Laboratório de Inovação Tecnológica em Saúde (LAIS).

## 🔗 Site

Clicando [aqui](https://digital-sus.herokuapp.com/login/) você consegue acessar o sistema que foi desenvolvido.

## Executando Localmente

> Caso você não tenha um ambiente virtual configurado para o projeto, como um VirtualEnv ou Anaconda, recomendo configurar um para que todos os passos funcionem sem erros.

1. Clone o repositório no seu ambiente local
```
$ git clone https://github.com/Raffae2679/digital-sus.git
```
2. Acesse o diretório que foi criado/clonado
```
$ cd digital-sus
```

3. Instale os pacotes python que são requisitos para o `build` do sistema
```
$ pip install -r requirements.txt
```

4.Agora você deve criar o banco de dados e realizar as migrações para que o DB esteja pronto para conexão e uso pelo Django
```
$ python manage.py makemigrations
$ python manage.py migrate
```

5. Crie um superusuário para ter acesso ao /admin
```
$ python manage.py createsuperuser
```

> A saída deve ser algo semelhante a isto:
```
Email:
Password:
Password (again):
Superuser created successfully.
```

6. Inicie seu servidor local Django
```
$ python manage.py runserver
```

> A saída deve ser algo semelhante a isto:
```
Watching for file changes with StatReloader
Performing system checks...
System check identified no issues (0 silenced).
December 21, 2020 - 19:00:00
Django version 3.1, using settings 'digitalSus.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CONTROL-C.
```

Pronto! O sistema está rodando no seu servidor local e você pode acessá-lo na URL http://localhost:8000/login/ .
