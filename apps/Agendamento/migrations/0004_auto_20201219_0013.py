# Generated by Django 3.1.4 on 2020-12-19 03:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0002_profissional_unidade_saude'),
        ('Agendamento', '0003_auto_20201218_1420'),
    ]

    operations = [
        migrations.AlterField(
            model_name='agendarvacina',
            name='paciente',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='usuarios.paciente', verbose_name='Paciente que agendou'),
        ),
        migrations.AlterField(
            model_name='agendarvacina',
            name='pos_fila',
            field=models.BigIntegerField(blank=True, null=True, verbose_name='Posição do paciente na fila'),
        ),
    ]