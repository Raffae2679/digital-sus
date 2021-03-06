# Generated by Django 3.1.4 on 2020-12-18 16:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('usuarios', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='VacinaPaciente',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=200, verbose_name='Nome da Vacina')),
                ('data_aplicacao', models.DateField(blank=True, verbose_name='Data de aplicação da vacina')),
                ('sus', models.BooleanField(default=False, verbose_name='Vacina aplicada no SUS')),
                ('paciente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='usuarios.paciente', verbose_name='Paciente que tomou a vacina')),
            ],
            options={
                'verbose_name': 'Vacina do Paciente',
                'verbose_name_plural': 'Vacinas do Paciente',
            },
        ),
    ]
