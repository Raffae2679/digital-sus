# Generated by Django 3.1.4 on 2020-12-20 03:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('administrativo', '0004_auto_20201220_0024'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vacinaus',
            name='unidade_saude',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='administrativo.unidadesaude', verbose_name='Unidade de saude que vai receber as vacinas'),
        ),
    ]
