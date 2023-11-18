from datetime import time
from django.forms import TimeInput
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext as _
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.


class Usuarios(AbstractUser):
    first_name = models.CharField(_('Nombre'),max_length=255, null=False)
    last_name = models.CharField(_('Apellido'),max_length=255, null=False)
    email = models.EmailField(_('Correo'), null=False, unique=True)
    username = models.CharField(_('rut (11111111-1)'),max_length=255, unique = True)
    password = models.CharField(_('Contraseña'),max_length=500, null=False)
    telefono = PhoneNumberField(null=False, blank=False, unique=True)
    is_superuser = models.BooleanField('Administrador',default=False)
    is_trabajador = models.BooleanField('trabajador',default=False)

    def __str__(self):
        Usuario = self.first_name + ' ' + self.last_name
        return Usuario


tipo_limpeza = [('LIMPIEZA PROFUNDA','limpieza profunda'),('LIMPIEZA NORMAL','limpieza normal'),('LIMPIEZA LIGERA','limpieza ligera')]

class categoria(models.Model):

    Nombre_categoria = models.CharField(max_length=40, null=False)
    Descripcion_categoria = models.CharField(max_length=250, null=False)
    Tipo_limpieza = models.CharField(max_length=255, choices=tipo_limpeza, null=False)

    def __str__(self):
        Categoria = self.Nombre_categoria
        return Categoria


class Servicios(models.Model):

    Nombre_servicio = models.CharField(max_length=40, null=False)
    Descripcion_servicio = models.CharField(max_length=250, null=False)
    Precio_estimado = models.IntegerField(blank=False)

    def __str__(self):
        Servicio = self.Nombre_servicio
        return Servicio

class Categoria_servicios(models.Model):

    Categoria = models.ForeignKey(categoria, on_delete=models.CASCADE, null=False)
    Servicios = models.ForeignKey(Servicios, on_delete=models.CASCADE, null=False)


class Solicitud_servicios(models.Model):

    Nombre_cliente = models.CharField(max_length=255, null=False)
    Direccion_limpieza = models.CharField(max_length=255, null=False)
    telefono_contacto = PhoneNumberField(null=False, blank=False, unique=True)
    Fecha_servicio = models.DateTimeField( null=False)
    Servicios = models.ForeignKey(Servicios, on_delete=models.CASCADE, null=False)
    
    def __str__(self):
        Categoria = self.Nombre_cliente + ' | ' + self.Servicios + ' | ' + self.Fecha_servicio
        return Categoria

