#Documento de vistas y accesos de la plataforma a travez del servidor, todas las pticiones que hace el usuario en la plataforma se manipulan en el servidor a travez de este archivo
#
#  Declaración de paquetes, herramientas, modelos y formularios.
from django.http import JsonResponse
from django.db import IntegrityError
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.sites.models import Site
from django.contrib import messages
from ZCApp.models import categoria, Servicios, Categoria_servicios, Usuarios, Solicitud_servicios, Transacciones
from django.contrib.auth import login, logout, authenticate
from ZCApp.forms import FormUser, FormUser, LoginUsers ,FormServices, FormCategory, FormAcquireService, EditUserForm
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required
from allauth.account.views import PasswordResetView
from allauth.account.forms import ResetPasswordKeyForm, UserTokenForm
from .credentials import PAYPAL_CLIENT_ID, PAYPAL_CLIENT_SECRET, EMAIL_HOST_USER, EMAIL_HOST_PASSWORD, PAYPAL_PROJECT_MODE, PLATAFORM_2_RESOURCE, PLATAFORM_2_PRODUCTS, update_credential, obtener_detalles_transaccion_paypal
from django.urls import reverse_lazy
from datetime import timezone, timedelta
from paypalrestsdk import Sale, Capture
from urllib.parse import quote
import traceback
from django.views.decorators.http import require_POST


#Función de pagina de administrador

def MainAdmin(request):

    if request.user.is_authenticated and request.user.is_superuser:

        datos0 = Usuarios.objects.all()
        datos1 = categoria.objects.all()
        datos2 = Servicios.objects.all()
        datos3 = Categoria_servicios.objects.all()
        datos4 = Solicitud_servicios.objects.all().order_by('Fecha_servicio')
        datos5 = Transacciones.objects.all().order_by('fecha_realizada')
        datos6 = Site.objects.all()
        datos7 = {
            'paypal_client_id': PAYPAL_CLIENT_ID,
            'paypal_client_secret': PAYPAL_CLIENT_SECRET,
            'email_host_user': EMAIL_HOST_USER,
            'email_host_password': EMAIL_HOST_PASSWORD,
            'PAYPAL_PROJECT_MODE': PAYPAL_PROJECT_MODE,
            'PLATAFORM_2_RESOURCE':PLATAFORM_2_RESOURCE,
            'PLATAFORM_2_PRODUCTS':PLATAFORM_2_PRODUCTS
        }
        data = {'datos0':datos0,'datos1':datos1,'datos2':datos2, 'datos3':datos3, 'datos4':datos4, 'datos5':datos5, 'datos6':datos6,'datos7':datos7}
        return render(request, "admin/PageAdmin.html", data)
    else:
        messages.add_message(request=request, level=messages.ERROR, message=f'El usuario no tiene permiso para acceder aquí')
        return redirect("../../Login")


#Función de pagina de cliente

def MainClient(request):
    if request.user.is_authenticated and request.user:
        return render(request, "Cliente/PageClient.html")
    else:
        messages.add_message(request=request, level=messages.ERROR, message=f'El usuario no tiene permiso para acceder aquí')
        return redirect("../../Login")



#Función de pagian del cliente para ver su solicitud de servicios

def InfoServices(request):
    if request.user.is_authenticated and request.user:
        datos0 = Usuarios.objects.get(id=request.user.id)
        datos1 = categoria.objects.all()
        datos2 = Servicios.objects.all()
        datos3 = Categoria_servicios.objects.all()
        datos4 = Solicitud_servicios.objects.filter(cliente_id = datos0).order_by('Fecha_servicio')
        datos5 = Transacciones.objects.filter(cliente_id = datos0).order_by('fecha_realizada')
        PAYPAL_BUTTON_CODE = quote(PAYPAL_CLIENT_ID)
        data = {'datos0':datos0,'datos1':datos1,'datos2':datos2, 'datos3':datos3, 'datos4':datos4, 'datos5':datos5, 'PaypalButton':PAYPAL_BUTTON_CODE, 'paypalMode': PAYPAL_PROJECT_MODE}
        return render(request, "Cliente/MainClient.html", data)
    else:
        messages.add_message(request=request, level=messages.ERROR, message=f'El usuario no tiene permiso para acceder aquí')
        return redirect("../../Login")



#Función de pagian del cliente para adquirir servicios

def AddServirce(request):

    if request.user.is_authenticated and request.user.is_superuser:
        form = FormServices()
        if request.method == 'POST':
            form = FormServices(request.POST)
            if form.is_valid():
                form = form.save()
                return redirect("../../admin")
        data = {'form':form}
        return render(request, 'admin/PageAdminForm.html', data)
    else:
        messages.add_message(request=request, level=messages.ERROR, message=f'El usuario no tiene permiso para acceder aquí')
        return redirect("../../Login")



#función para editar servicios

def EditService(request, id):

    if request.user.is_authenticated and request.user.is_superuser:
        servicio = Servicios.objects.get(id=id)
        form = FormServices(instance=servicio)
        if request.method == 'POST':
            form = FormServices(request.POST, instance=servicio)
            if form.is_valid():
                form = form.save()
                return redirect("../../admin")

        data = {'form':form}
        return render(request, 'admin/PageAdminForm.html', data)

    else:
        messages.add_message(request=request, level=messages.ERROR, message=f'El usuario no tiene permiso para acceder aquí')
        return redirect("../../Login")



 #función para borrar algun servicio

def deletService(request, id):
    if request.user.is_authenticated and request.user.is_superuser:
        try:
            data = Servicios.objects.get(id=id)
            datos4 = Solicitud_servicios.objects.filter(Servicios=data)

            # Verificar el estado antes de eliminar
            if data.Disponibilidad not in ['Pendiente', 'Nuevo', 'Aceptado']:
                # Verificar si el servicio está en datos4 con los estados mencionados
                if not datos4.filter(Estado__in=['Pendiente', 'Nuevo', 'Aceptado']).exists():
                    data.delete()
                    messages.add_message(request=request, level=messages.SUCCESS, message=f'Servicio eliminado exitosamente')
                else:
                    messages.add_message(request=request, level=messages.ERROR, message=f'No se puede eliminar el servicio, está asociado a una solicitud con estado permitido')
            else:
                messages.add_message(request=request, level=messages.ERROR, message=f'No se puede eliminar el servicio con estado {data.Disponibilidad}')

        except Servicios.DoesNotExist:
            messages.add_message(request=request, level=messages.ERROR, message='Servicio no encontrado')
        except Exception as e:
            # Capturar excepción y registrarla (puedes imprimir o registrar el error en tu sistema)
            print(f"Error al eliminar servicio: {e}")
            messages.add_message(request=request, level=messages.ERROR, message='Error interno al eliminar el servicio')

        return redirect("../../admin")
    else:
        messages.add_message(request=request, level=messages.ERROR, message=f'El usuario no tiene permiso para acceder aquí')
        return redirect("../../Login")



#función para añadir categorías

def AddCategory (request):

    if request.user.is_authenticated and request.user.is_superuser:

        form = FormCategory()
        if request.method == 'POST':
            form = FormCategory(request.POST)
            if form.is_valid():
                form = form.save()
                return redirect("../../admin")

        data = {'form':form}
        return render(request, 'admin/PageAdminForm.html', data)
    else:
        messages.add_message(request=request, level=messages.ERROR, message=f'El usuario no tiene permiso para acceder aquí')
        return redirect("../../Login")



#Función para editar categorías

def EditCategory(request, id):

    if request.user.is_authenticated and request.user.is_superuser:
        Categoria = categoria.objects.get(id=id)
        form = FormCategory(instance=Categoria)
        if request.method == 'POST':
            form = FormCategory(request.POST, instance=Categoria)
            if form.is_valid():
                form = form.save()
                return redirect("../../admin")

        data = {'form':form}
        return render(request, 'admin/PageAdminForm.html', data)

    else:
        messages.add_message(request=request, level=messages.ERROR, message=f'El usuario no tiene permiso para acceder aquí')
        return redirect("../../Login")



#función para borrar categorías
def deletCategory(request, id):
    if request.user.is_authenticated and request.user.is_superuser:
        data = categoria.objects.get(id=id)
        data.delete()
        messages.add_message(request=request, level=messages.SUCCESS, message=f'Categoría eliminadada exitosamete')
        return redirect("../../admin")
    else:
        messages.add_message(request=request, level=messages.ERROR, message=f'El usuario no tiene permiso para acceder aquí')
        return redirect("../../Login")



#Función para iniciar sesión

def Login(request):
    form=LoginUsers()
    if request.method == 'POST':
        form = LoginUsers(data=request.POST)
        user = authenticate(username=request.POST['username'], password=request.POST['password'])
        if user is None:
             messages.add_message(request=request, level=messages.ERROR, message=f'El usuario o la contraseña ingresada son incorrectas')
        else:
            if form.is_valid():
                    username = form.cleaned_data.get('username')
                    password = form.cleaned_data.get('password')
                    user = authenticate(username=username, password=password)
                    if user is not None:
                        login(request, user)
                        if user.is_superuser:
                            return redirect("../admin")
                        else:
                            return redirect("/client")
                    else:
                        messages.error(request, 'El usuario o la contraseña ingresada son incorrectas')

                    messages.add_message(request=request, level=messages.SUCCESS, message=f'Bienvenido a la aplicación ')
            else:
                    messages.add_message(request=request, level=messages.ERROR, message=f'Los registros no son validos')
    data = {'form':form}
    return render(request, 'Cliente/PageClientLogin.html', data)



#Función para salir de la seción

def Unlogin(request):
    logout(request)
    return redirect('/')


#Función para crear un usuario de la plataforma (Solo del tipo cliente, por otro acceso de crea el administrador y el trabajador)
def AddUser(request):
    form = FormUser()
    if request.method == 'POST':
        form = FormUser(request.POST)
        if form.is_valid():
            form = form.save()
            return redirect("../Login")
    data = {'form':form}
    return render(request, 'Cliente/PageClientRegister.html', data)



#Función para modificar datos de sesión de usuario

@login_required
def ModRegister(request):
    if request.user is None:
        return redirect("/")
    else:

        user = get_object_or_404(Usuarios, id= request.user.id)

        if request.method == 'POST':
            form = EditUserForm(request.POST, instance=user)
            if form.is_valid():
                new_password = form.cleaned_data.get('new_password')
                if new_password:
                    user.password = make_password(new_password)
                form.save()
                return redirect("../Login/")
        else:
            form = EditUserForm(instance=user)

        data = {'form': form, 'user': user}
        return render(request, 'Cliente/PageClientLogin.html', data)



#Funión para recuperar contraseña con envio por correo.

class ResetPassword(PasswordResetView):
    
    template_name = 'Cliente/ResetPass.html'
    success_url = reverse_lazy('account_reset_password_done')


#Función para cambiar la contraseña para recuperar la cuenta por envio de correo.

def reset_password_from_key(request, uidb36_key):
    try:
        uidb36, key = uidb36_key.split('-', 1)
        user_token_form_class = UserTokenForm
        token_form = user_token_form_class(data={"uidb36": uidb36, "key": key})
        if token_form.is_valid():
            reset_user = token_form.reset_user
            form = ResetPasswordKeyForm(user=reset_user, temp_key = key)
            if request.method == "POST":
                print(form.user)
                form = ResetPasswordKeyForm(user=reset_user, temp_key = key, data=request.POST)
                print(form.temp_key)
                if form.is_valid():
                    form.save()
                    messages.add_message(request=request, level=messages.SUCCESS, message=f'Contraseña actualizada')
                    return redirect("/Login")
                else:
                    messages.add_message(request=request, level=messages.ERROR, message=f'Ocurrio un problema con la contraseña nueva, intentalo denuevo')
            return render(request, "Cliente/ResetPass.html", {'reset_user': reset_user, 'form': form})
        else:
            return render(request, "Cliente/ResetPass.html")
    except:
        return render(request, "Cliente/ResetPass.html")
    


#Funión de pagina principal de la plataforma

def MainPage(request):

    datos1 = {
            'PLATAFORM_2_RESOURCE':PLATAFORM_2_RESOURCE,
            'PLATAFORM_2_PRODUCTS':PLATAFORM_2_PRODUCTS
        }
    data = {'datos0':datos1}
    return render(request, 'Cliente/inicio.html', data)



#Función del cliente para adquirir servicios

def AcquireServce(request):

    if request.user.is_authenticated:
        datos2 = Servicios.objects.filter(Disponibilidad = "Disponible")
        form = FormAcquireService()

        if request.method == 'POST':

            form = FormAcquireService(request.POST)

            if form.is_valid():
                # Asignar el cliente al usuario actual antes de guardar el formulario
                form.instance.cliente = request.user
                form.instance.telefono_contacto = request.user.telefono
                form.save()
                messages.add_message(request=request, level=messages.SUCCESS, message='Pedido adquirido exitosamente')
                return redirect("../../client")

        data = {'form': form, 'datos2':datos2}
        return render(request, 'Cliente/PageClient_Services.html', data)
    else:
        return redirect("/client")



#Función del administrador para definir relación de servicio y categoría

def setCatServ(request, serv_id, cat_id, stade):
    if request.user.is_authenticated and request.user.is_superuser:
        try:
            categoria_instance = categoria.objects.get(id=cat_id)
            servicio_instance = Servicios.objects.get(id=serv_id)
        except categoria.DoesNotExist or Servicios.DoesNotExist:
            return JsonResponse({'codigo': 1})
        if stade == "add":
            if Categoria_servicios.objects.filter(Categoria=categoria_instance, Servicios=servicio_instance).exists():
                return JsonResponse({'titulo': "Ocurrio un problema", 'mensaje':"La categoria ya se encuentra en el servicio", "icono":"warning"})
            else:
                try:
                    Categoria_servicios.objects.create(Categoria=categoria_instance, Servicios=servicio_instance)
                except IntegrityError:
                    return JsonResponse({'titulo': "Ocurrio un problema", 'mensaje':"La conexión con el servidor o la base de datos se interrumpio", "icono":"warning"})
                return JsonResponse({'titulo': "Operación exitosa", 'mensaje':"Ya se asigno la categoria al servicio", "icono":"success"})
        elif stade == "delete":
            try:
                relacion = Categoria_servicios.objects.get(Categoria=categoria_instance, Servicios=servicio_instance)
                relacion.delete()
                return JsonResponse({'titulo': "Operación exitosa", 'mensaje':"Se eliminó la relación entre la categoria y el servicio", "icono":"success"})
            except Categoria_servicios.DoesNotExist:
                return JsonResponse({'titulo': "Ocurrio un problema", 'mensaje':"La relación no existe", "icono":"warning"})
            except IntegrityError:
                return JsonResponse({'titulo': "Ocurrio un problema", 'mensaje':"La conexión con el servidor o la base de datos se interrumpio", "icono":"warning"})
        else:
            return JsonResponse({'titulo': "Ocurrio un problema", 'mensaje':"Operación no válida", "icono":"warning"})
    else:
        messages.add_message(request=request, level=messages.ERROR, message=f'El usuario no tiene permiso para acceder aquí')
        return redirect("../../../../Login")



#Función del administrador para definir la disponibilidad del servicio

def setStadeServ(request, serv_id):
    if request.user.is_authenticated and request.user.is_superuser:
        valStade = request.POST['Estado']
        servicio_instance = Servicios.objects.get(id=serv_id)
        if valStade == "1":
            servicio_instance.Disponibilidad = "Disponible"
            servicio_instance.save()
            return JsonResponse({'titulo': "Servicio habilitado", "icono":"success"})
        else:
            servicio_instance.Disponibilidad = "Desabilitado"
            servicio_instance.save()
            return JsonResponse({'titulo': "Servicio deshabilitado", "icono":"success"})
    else:
        messages.add_message(request=request, level=messages.ERROR, message=f'El usuario no tiene permiso para acceder aquí')
        return redirect("../../../../Login")

#Función del administrador pra actualizar los estados de solicitudes
def actualizar_estado_solicitud(request, solicitud_id, estado):

    if request.user.is_authenticated and request.user.is_superuser:
        solicitud = Solicitud_servicios.objects.get(id=solicitud_id)
        Cliente = Usuarios.objects.get(id = solicitud.cliente_id)
        servicio = Servicios.objects.get(id = solicitud.Servicios_id)
        stade = 0

        if solicitud.Estado != estado:

            print("Nuevo estado: " + estado)
            stade = 1

        solicitud.Estado = estado
        solicitud.save()

        if stade == 1:

            fecha_hora = solicitud.Fecha_servicio
            diferencia_utc = timedelta(hours=-3)
            zona_horaria_santiago = timezone(diferencia_utc)

            # Convierte la fecha y hora a la zona horaria de Santiago
            Fecha_nacional = fecha_hora.replace(tzinfo=timezone.utc).astimezone(zona_horaria_santiago)
            Dia = str(Fecha_nacional.date())
            Hora = str(Fecha_nacional.hour) + ":" + str(Fecha_nacional.minute)
            asunto = ""
            mensaje = ""
            if estado == "Aceptado":

                asunto = servicio.Nombre_servicio + " ha sido aceptado"
                mensaje = "¡Hola " + Cliente.first_name + " " + Cliente.last_name + "! \nNos complace informarte que tu solicitud para el servicio de limpieza programado para el " + Dia + " a las " + Hora + " ha sido aceptada. Estamos emocionados de poder ayudarte y proporcionarte un entorno limpio y ordenado.\n\n Si tienes alguna pregunta o necesitas realizar ajustes, no dudes en contactarnos. \n¡Gracias por elegir nuestro servicio de limpieza! \nAtentamente, Zeus Clean"

            if estado == "Rechazado":

                asunto = servicio.Nombre_servicio + " ha sido rechazado"
                mensaje = "¡Hola " + Cliente.first_name + " " + Cliente.last_name + "! \nLamentamos informarte que, por razones internas y la decision tomada, tu solicitud para el servicio de limpieza programado para el " + Dia + " a las " + Hora + " ha sido rechazada. Estamos aquí para ayudarte en futuras ocasiones. Si tienes alguna pregunta o necesitas más información, no dudes en contactarnos. \nGracias por considerar nuestro servicio. \nAtentamente, Zeus Clean"

            if estado == "Pendiente":

                asunto ="¡Hola " + Cliente.first_name + " " + Cliente.last_name + "!"

                mensaje = "Hemos recibido tu solicitud para el servicio de limpieza programado para el " + Dia + " a las " + Hora + ", Estamos procesando tu solicitud y te informaremos tan pronto como haya una actualización. Si tienes alguna pregunta o necesitas realizar ajustes, no dudes en contactarnos. \n¡Gracias por elegir nuestro servicio de limpieza! \nAtentamente, Zeus Clean"

            if estado == "Pagado":

                return JsonResponse({'mensaje': 'Pago realizado exitosamente'})

            if enviar_correo(Cliente.email, asunto, mensaje):
                messages.add_message(request=request, level=messages.SUCCESS, message='Correo electrónico enviado exitosamente')
            else:
                messages.add_message(request=request, level=messages.ERROR, message='Error al enviar el correo electrónico')

        return JsonResponse({'mensaje': 'Estado actualizado exitosamente'})
    else:
        messages.add_message(request=request, level=messages.ERROR, message=f'El usuario no tiene permiso para acceder aquí')
        return redirect("../.././../../Login")



#Función del usuario para registrar su adquisicion pagada

def AddIDCash(request):
    if 'descripcion' not in request.POST or len(request.POST['descripcion']) == 0 or request.POST['descripcion'] is None:
        messages.add_message(request=request, level=messages.ERROR, message='No existen datos de transacción')
        return redirect("/")
    post_data = request.POST
    subdata_keys = [key for key in post_data.keys() if 'Subdata' in key]
    subdata_lists = [post_data.getlist(key) for key in subdata_keys]
    Subdata = [item for sublist in subdata_lists for item in sublist]
    descripcion = request.POST['descripcion']
    Action = request.POST['Act']
    precioServ = request.POST['precioTotal']
    code = request.POST['codigo']
    client = request.POST['usuario']
    ClienteData = Usuarios.objects.get(username=client)
    transaccion = Transacciones.objects.create(
        cliente=ClienteData,
        codigo=code,
        accion=Action
    )
    transaccion.servicios.set(Solicitud_servicios.objects.filter(id__in=Subdata))
    Solicitud_servicios.objects.filter(id__in=Subdata).update(Estado="Pagado")
    asunto = "Zeus Clean - Pago realizado con éxito"
    mensaje = f"Hola {client},\n\nTu pago ha sido procesado exitosamente. A continuación, te proporcionamos los detalles:\n\nCódigo de orden PayPal: {code}\n\nServicios:\n{descripcion}\n\nPrecioTotal: CLP{precioServ}\n\nGracias por confiar en nosotros.\n\nAtentamente,\nZeus Clean."
    print("enviando correo")
    enviar_correo(transaccion.cliente.email, asunto, mensaje)
    print("fin correo")
    return JsonResponse({'mensaje': 'ID de transacción aceptada'})

#Función del administrador para concretar con el termino del servio realizado (hacer esto evita la opción de realizar un rembolso)
def AlerService(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            id_estado = request.POST.get('ID_Estado')
            estado = request.POST.get('Estado')
            servicio = Solicitud_servicios.objects.get(id=id_estado)
            if request.user == servicio.cliente or request.user.is_superuser and estado == "Finalizado":
                try:
                    servicio.Estado = estado
                    Cliente = Usuarios.objects.get(id=servicio.cliente_id)
                    servicio.save()
                    asunto = "Zeus Clean - ¡Tu servicio ha sido completado!"
                    mensaje =  f"Hola {Cliente},\n\nTu servicio [{servicio.Servicios}] ha sido completado satisfactoriamente.\n\nPor favor, ten en cuenta que cualquier transacción realizada con este servicio finalizado no tiene opción de reembolso, si ocurrió algún problema o inconveniente, por favor contactarse con nosotros para resolver algún problema. Gracias por su atención y contar con nosotros, Zeus Clean."
                    request.POST = request.POST.copy()
                    request.POST['asunto'] = asunto
                    request.POST['mensaje'] = mensaje
                    EnvioMensaje(request, id_estado)
                    return JsonResponse({'mensaje': 'Servicio aplicado exitosamente'})
                except Solicitud_servicios.DoesNotExist:
                    return JsonResponse({'error': 'Ocurrio un problema con la petición'}, status=403)
            else:
                return JsonResponse({'error': 'El servicio no pertenece al usuario autenticado'}, status=400)
        else:
            return JsonResponse({'error': 'La solicitud debe ser de tipo POST'}, status=405)
    else:
        messages.add_message(request=request, level=messages.ERROR, message='El usuario no tiene permiso para acceder aquí')
        return redirect("../.././../../Login")
    
#Función del cliente para solicitar el rembolso, La función acepta codigo con inicio de "PAYID-"
@require_POST
def RembolsoService(request):
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Usuario no autenticado'}, status=401)

    id_transaccion = request.POST.get('id')
    codigo_paypal = request.POST.get('code')
    if not id_transaccion or not codigo_paypal:
        return JsonResponse({'error': 'Datos incompletos'}, status=400)

    try:
        transaccion = Transacciones.objects.get(id=id_transaccion)
    except Transacciones.DoesNotExist:
        return JsonResponse({'error': 'La transacción no existe'}, status=400)

    if transaccion.cliente != request.user:
        return JsonResponse({'error': 'El usuario no está autorizado para realizar esta acción'}, status=400)

    servicios_data = transaccion.servicios.all()
    for servicio in servicios_data:
        if servicio.Estado == 'Finalizado':
            return JsonResponse({'error': 'No se puede realizar el reembolso. Uno de los servicios ya está finalizado.'}, status=400)
    
    detalles_transaccion = obtener_detalles_transaccion_paypal(transaccion.codigo)

    if codigo_paypal == detalles_transaccion.get('id') or transaccion.codigo.startswith("PAYID-"):
       
        capture_id = ""
        if transaccion.codigo.startswith("PAYID-"):
            capture_id = detalles_transaccion['transactions'][0]['related_resources'][0]['sale']['id']
        else:
            capture_id = detalles_transaccion['purchase_units'][0]['payments']['captures'][0]['id']
        try:
            if transaccion.codigo.startswith("PAYID-"):
                refund_attributes = {
                    'amount': {
                        'currency': detalles_transaccion['transactions'][0]['amount']['currency'],
                        'total': detalles_transaccion['transactions'][0]['amount']['total']
                    }
                }
                sale = Sale.find(capture_id)
                refund = sale.refund(refund_attributes)
                refund.success() 
            else:
                capture = Capture.find(capture_id)
                refund_attributes = {
                    'amount': {
                        'currency': detalles_transaccion['purchase_units'][0]['amount']['currency_code'],
                        'total': detalles_transaccion['purchase_units'][0]['amount']['value']
                    }
                }
                refund = capture.refund(refund_attributes)

            for servicio in transaccion.servicios.all():
                servicio.Estado = 'Reembolsado'
                servicio.save()
            
            nueva_transaccion = Transacciones.objects.get(codigo = transaccion.codigo)
            nueva_transaccion.accion = "Devolución"
            nueva_transaccion.servicios.set(Solicitud_servicios.objects.filter(id__in=transaccion.servicios.all()))
            nueva_transaccion.save()

            Cliente = nueva_transaccion.cliente
            
            asunto = "Zeus Clean - ¡Tu servicio ha sido rembolsado!"
            mensaje = f"Hola {Cliente},\n\nTu solicitud de reembolso para los siguientes [{nueva_transaccion.servicios}] ha sido procesada.\n\nPor favor, ten en cuenta que el reembolso ha sido realizado satisfactoriamente.\n\nSi tienes alguna pregunta o necesitas más información, no dudes en contactarnos. \n\nCodigo de transacción en el sistema paypal de nuestros servicios: {nueva_transaccion.codigo}  \n\n¡Gracias por contar con nosotros! Atentamente, Zeus Clean."
            request.POST = request.POST.copy()
            enviar_correo(Cliente.email, asunto, mensaje)
            return JsonResponse({'mensaje': 'Reembolso realizado con éxito'})
        except Exception as e:
            print("Error al realizar el reembolso:", e)
            return JsonResponse({'error': 'Error al realizar el reembolso'}, status=400)
    else:
        print("ERROR")
        return JsonResponse({'error': 'Código de PayPal inválido'}, status=400)

def custom_404(request, exception):
    return render(request, 'Errors/404.html', status=404)


#Función del administrador para enviar mensajes

def EnvioMensaje(request, id):

    if request.user.is_authenticated and request.user.is_superuser:
        servicio = Solicitud_servicios.objects.get(id=id)
        Cliente = Usuarios.objects.get(id=servicio.cliente_id)
        asunto = request.POST.get('asunto', '')
        mensaje = request.POST.get('mensaje', '')

        enviar_correo(Cliente.email, asunto, mensaje)
        return JsonResponse({'mensaje': 'Correo electrónico enviado'})
    else:
        messages.add_message(request=request, level=messages.ERROR, message=f'El usuario no tiene permiso para acceder aquí')
        return redirect("../.././../../Login")



#Función de formato de mensajes utilizado por otras funciones o de forma manual por el administrador

def enviar_correo(destinatario, asunto, mensaje):
    remitente = settings.EMAIL_HOST_USER
    try:
        send_mail(
            asunto,
            mensaje,
            remitente,
            [destinatario],
            fail_silently=False,
        )
        print("Correo electrónico enviado exitosamente.")
        return True
    except Exception as e:

        print(f"Error al enviar el correo electrónico: {str(e)}")
        traceback.print_exc()
        return False

#Funcion del administrador para actualizar las credeciales y ajustes de la plataforma
def UpdateProject(request, id):
    if request.user.is_authenticated and request.user.is_superuser:
        new_value = request.POST.get('data_input', '')
        if id in [1, 2]:
            site = Site.objects.get_current()
            if id == 1:
                site.name = new_value
            elif id == 2:
                site.domain = new_value
            site.save()
            return JsonResponse({'mensaje': 'Credencial actualizada correctamente'})
        elif id in [3, 4, 5, 6, 7, 8, 9]:
            # Actualizar una de las credenciales
            credential_name = {
                3: 'PAYPAL_CLIENT_ID',
                4: 'PAYPAL_CLIENT_SECRET',
                5: 'EMAIL_HOST_USER',
                6: 'EMAIL_HOST_PASSWORD',
                7: "PAYPAL_PROJECT_MODE",
                8: "PLATAFORM_2_RESOURCE",
                9: "PLATAFORM_2_PRODUCTS"

            }.get(id)
            if credential_name:
                print(credential_name)
                print(new_value)
                update_credential(credential_name, new_value)
                return JsonResponse({'mensaje': f'{credential_name} actualizado correctamente'})
            else:
                return JsonResponse({'mensaje': 'ID de credencial no válido'}, status=400)    
        else:
            return JsonResponse({'mensaje': 'ID no válido'}, status=400)
    else:
        return JsonResponse({'mensaje': 'El usuario no tiene permiso para acceder aquí'}, status=403)
    
