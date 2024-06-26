# Generated by Django 4.2.5 on 2023-12-25 21:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ZCApp', '0006_alter_solicitud_servicios_direccion_limpieza'),
    ]

    operations = [
        migrations.CreateModel(
            name='Transacciones',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codigo', models.CharField(max_length=255, verbose_name='Código')),
                ('fecha_realizada', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')),
                ('accion', models.CharField(choices=[('Compra', 'Compra'), ('Devolución', 'Devolución')], max_length=255, verbose_name='Acción')),
                ('cliente', models.ForeignKey(blank=True, default=None, limit_choices_to={'is_superuser': False, 'is_trabajador': False}, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('servicios', models.ManyToManyField(related_name='transacciones', to='ZCApp.servicios')),
            ],
        ),
    ]
