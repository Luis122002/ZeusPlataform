# Generated by Django 4.2.5 on 2023-12-25 04:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ZCApp', '0004_servicios_disponibilidad'),
    ]

    operations = [
        migrations.AlterField(
            model_name='servicios',
            name='Disponibilidad',
            field=models.CharField(choices=[('Disponible', 'Disponible'), ('Desabilitado', 'Desabilitado')], default='limpieza ligera', max_length=255, verbose_name='Disponibilidad'),
        ),
    ]