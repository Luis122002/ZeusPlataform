from django.shortcuts import render, redirect
import hashlib
from django.contrib.auth.forms import  AuthenticationForm
from django.contrib import messages
from ZCApp.models import categoria, Servicios, Categoria_servicios, Usuarios, Solicitud_servicios
from django.contrib.auth import login, logout, authenticate
from ZCApp.forms import FormUser, FormUser ,FormServices, FormCategory, FormCatServ, FormAcquireService

def MainAdmin(request):

    if request.user.is_authenticated and request.user.is_superuser:

        datos0 = Usuarios.objects.all()
        datos1 = categoria.objects.all()
        datos2 = Servicios.objects.all()
        datos3 = Categoria_servicios.objects.all()
        datos4 = Solicitud_servicios.objects.all()
        data = {'datos0':datos0,'datos1':datos1,'datos2':datos2, 'datos3':datos3, 'datos4':datos4}

        return render(request, "admin/PageAdmin.html", data)
    else:
        return redirect("../Login")

def AddServirce(request):

    if request.user.is_authenticated and request.user.is_superuser:

        form = FormServices()
        if request.method == 'POST':
            form = FormServices(request.POST)
            if form.is_valid():
                form = form.save()
                #crypt = form.save(commit=False)
                return redirect("../../admin")

        data = {'form':form}
        return render(request, 'admin/PageAdminServices.html', data)
    
    else:
        return redirect("../Login")


def AddCategory (request):

    if request.user.is_authenticated and request.user.is_superuser:

        form = FormCategory()
        if request.method == 'POST':
            form = FormCategory(request.POST)
            if form.is_valid():
                form = form.save()
                #crypt = form.save(commit=False)
                return redirect("../../admin")
                
        data = {'form':form}
        return render(request, 'admin/PageAdminCategory.html', data)
    else:
        return redirect("../Login")

def AddLinkCat(request):

    if request.user.is_authenticated and request.user.is_superuser:
        form = FormCatServ()
        if request.method == 'POST':
            form = FormCatServ(request.POST)
            if form.is_valid():
                form = form.save()
                #crypt = form.save(commit=False)
                return redirect("../../admin")
                
        data = {'form':form}
        return render(request, 'admin/PageAdminServicesCat.html', data)
    else:
        return redirect("../Login")




def Login(request):

    if request.user.is_authenticated:
        if request.user.is_superuser:
            messages.add_message(request=request, level=messages.SUCCESS, message=f'Registro de usuario cargado')
            return redirect("../admin")
    else:
        form=AuthenticationForm()
        if request.method == 'POST':
            form = AuthenticationForm(data=request.POST)
            user = authenticate(username=request.POST['username'], password=request.POST['password'])
            if user is None:
                messages.add_message(request=request, level=messages.ERROR, message=f'El usuario o la contraseña ingresada son incorrectas')
            else:
                if form.is_valid():
                        login(request,user)
                        if request.user.is_superuser:
                            return redirect("../admin")
                        messages.add_message(request=request, level=messages.SUCCESS, message=f'Bienvenido a la aplicación ')
                else:
                        messages.add_message(request=request, level=messages.ERROR, message=f'Los registros no son validos')
    data = {'form':form}
    return render(request, 'Cliente/PageClientLogin.html', data)

def Unlogin(request):
    logout(request)
    return redirect('/')

def AddUser(request):
    
    form = FormUser()
    if request.method == 'POST':
        form = FormUser(request.POST)
        if form.is_valid():
            form = form.save()
            return redirect("../../admin")
    data = {'form':form}
    return render(request, 'Cliente/PageClientLogin.html', data)


def MainPage(request):

    return render(request, 'Cliente/PageClient.html')

def AcquireServce(request):

    form = FormAcquireService()
    if request.method == 'POST':
        form = FormAcquireService(request.POST)
        if form.is_valid():
            form = form.save()
            return redirect("../../admin")
    data = {'form':form}
    return render(request, 'Cliente/PageClient_Services.html', data)
