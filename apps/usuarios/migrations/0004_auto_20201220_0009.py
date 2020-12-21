# Generated by Django 3.1.4 on 2020-12-20 03:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0003_remove_paciente_numero_carteira'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='perfil_paciente',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='paciente', to='usuarios.paciente', verbose_name='Perfil do Paciente'),
        ),
    ]