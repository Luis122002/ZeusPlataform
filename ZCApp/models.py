#Documento de modelos de datos de la plataforma web, es l estructura de la base de datos de la plataforma.
#para su uso se tiene que estar conectado a una base de datos y escribir "python manage.py makemigrations" y "python manage.py migrate" para generar la estructura.

#Dependencias y paquetes de uso
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext as _
from phonenumber_field.modelfields import PhoneNumberField


#Listado de clasificación de tipo de limpieza para los datos de servicios
tipo_limpeza = [('LIMPIEZA PROFUNDA','limpieza profunda'),('LIMPIEZA NORMAL','limpieza normal'),('LIMPIEZA LIGERA','limpieza ligera')]



#Modelo de la clase de usuario, el "firs name / last name" son nombre y apellido, el "username" es el rut, el "is_superuser/ is_trabajador" es para clasificar usuarios y el resto de campos se dice por si mismo.
#El "def__str__(self)" es para referirse el nombre del usuario completo (nombre y apellido) como su propio registro.
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



#Modelo sobre las categorias para clasificar los servicio con el nombre y su descripción, el "def__str__(self)" se refiere al registro por su nombre.
class categoria(models.Model):

    Nombre_categoria = models.CharField(_('Nombre de categoria'),max_length=40, null=False)
    Descripcion_categoria = models.CharField(_('Descripción de categoria'),max_length=250, null=False)

    def __str__(self):
        Categoria = self.Nombre_categoria
        return Categoria


#Modelo que estructura los servicios de la platafora. utiliza el estado de disponibilidad, nombre de servicio, descripción, tipo de limpieza y el precio estimado
#el "def__str__(self)" se refiere a su nombre de servicio como registro.
class Servicios(models.Model):

    DISP_CHOICES = [
        ('Disponible', _('Disponible')),
        ('Desabilitado', _('Desabilitado'))
    ]

    Nombre_servicio = models.CharField(_('Nombre del servicio'),max_length=40, null=False)
    Descripcion_servicio = models.CharField(_('Descripción del servicio'),max_length=250, null=False)
    Precio_estimado = models.IntegerField(_('Asignar precio'),blank=False)
    Tipo_limpieza = models.CharField(_('Tipo de limpieza'),max_length=255, choices=tipo_limpeza, null=False, default = "limpieza ligera")
    Disponibilidad = models.CharField(_('Disponibilidad'),max_length=255, choices=DISP_CHOICES, null=False, default = "limpieza ligera")
    def __str__(self):
        Servicio = self.Nombre_servicio
        return Servicio


#Modelo que adjunta los registros de categoria y los servicios.
class Categoria_servicios(models.Model):

    Categoria = models.ForeignKey(categoria, on_delete=models.CASCADE, null=False)
    Servicios = models.ForeignKey(Servicios, on_delete=models.CASCADE, null=False)


#Modelo que estructuran las solicitudes de servicios por parte de los clientes, se obtiene su estado de servicio, el cliente refiriendose al usuario que lo adquirio,
#el numero de telefono del usuario para comunicarse, la fecha de servicio que el cliente solitio para que se realizar el servicio, la fecha del dato del servicio que se genero,
# y la dirección donde se tiene que llevar a cabo el servicio, el "def __str__(self)" se refiere por el nombre del cliente, el servicio y la fecha del servicio a realizar.
class Solicitud_servicios(models.Model):

    ESTADO_CHOICES = [
        ('Nuevo', _('Nuevo')),
        ('Aceptado', _('Aceptado')),
        ('Rechazado', _('Rechazado')),
        ('Pendiente', _('Pendiente')),
        ('Pagado', _('Pagado')),
        ('Cancelado', _('Cancelado')),
        ('Reembolsado', _('Reembolsado')),
        ('Finalizado', _('Finalizado'))
    ]

    cliente = models.ForeignKey(Usuarios, on_delete=models.CASCADE, limit_choices_to={'is_superuser': False, 'is_trabajador': False}, null=True, blank=True, default=None)
    Direccion_limpieza = models.CharField(_('Dirección del lugar'), max_length=255, null=False)
    telefono_contacto = PhoneNumberField(_('Número telefónico'), null=False, blank=False, unique=False)
    Fecha_servicio = models.DateTimeField(_('Fecha para realizar el servicio'), null=False)
    Servicios = models.ForeignKey(Servicios, on_delete=models.CASCADE, null=False)
    Fecha_data = models.DateTimeField(_('Fecha de creación'), auto_now_add=True)
    Estado =  models.CharField(_('Estado'), max_length=40, null=False, default='Nuevo')

    def __str__(self):
        Categoria = f"{self.cliente} | {self.Servicios} | {self.Fecha_servicio}"
        return Categoria

#Modelo que gestiona lod registros de transacciones y rembolsos realizados, contiene el usuario, servicio, el codigo generado de la transacción, la fecha que se realizo la transacción y la acción que si es un pago o un rembolso
class Transacciones(models.Model):
    Act_choices = [
        ('Compra', _('Compra')),
        ('Compra_deb', _('Compra_deb')),
        ('Devolución', _('Devolución')),
        ('Sin Rembolso', _('Sin Rembolso')),
    ]
    cliente = models.ForeignKey(Usuarios, on_delete=models.CASCADE, limit_choices_to={'is_superuser': False, 'is_trabajador': False}, null=True, blank=True, default=None)
    servicios = models.ManyToManyField(Solicitud_servicios, related_name='transacciones')
    codigo = models.CharField(_('Código'), max_length=255, null=False)
    fecha_realizada = models.DateTimeField(_('Fecha de creación'), auto_now_add=True)
    accion = models.CharField(_('Acción'), max_length=255, choices=Act_choices, null=False)