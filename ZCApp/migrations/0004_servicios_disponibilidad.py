# Generated by Django 4.2.5 on 2023-12-25 04:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ZCApp', '0003_alter_solicitud_servicios_direccion_limpieza_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='servicios',
            name='Disponibilidad',
            field=models.CharField(choices=[('LIMPIEZA PROFUNDA', 'limpieza profunda'), ('LIMPIEZA NORMAL', 'limpieza normal'), ('LIMPIEZA LIGERA', 'limpieza ligera')], default='limpieza ligera', max_length=255, verbose_name='Disponibilidad'),
        ),
    ]
