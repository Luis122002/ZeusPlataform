#Documento de direcciones URL de acceso a la plataforma y funcionalidades.

#Dependencias
from django.contrib import admin
from django.urls import path, include  
from django.contrib.auth import views as auth_views
from ZCApp.views import MainAdmin, MainPage, MainClient, InfoServices, AddServirce, EditService, deletService, AddCategory, EditCategory, deletCategory, Login, AddUser, ModRegister, Unlogin, AcquireServce, actualizar_estado_solicitud, setCatServ, setStadeServ, AlerService, AddIDCash, RembolsoService, EnvioMensaje, custom_404, ResetPassword, reset_password_from_key, UpdateProject
handler404 = custom_404


#URLS
urlpatterns = [
    #URL principal
    path('', MainPage),

    #Opciones de ingreso
    path('Login/', Login),
    path('Exit/', Unlogin),
    path('Register/', AddUser),
    path('ModRegister/', ModRegister),
    path('accounts/password/reset/', ResetPassword.as_view(), name='account_reset_password'),
    path('accounts/password/reset/done/', ResetPassword.as_view(), name='account_reset_password_done'),
    path('accounts/password/reset/key/<uidb36_key>/', reset_password_from_key, name='account_reset_password_from_key'),
    path('accounts/', include('allauth.urls')),

    #Modulo Cliente
    path('client/', MainClient),
    path('client/infoServices', InfoServices),
    path('client/Acquire_Service/', AcquireServce),
    
    #modulo Admin
    path('admin',MainAdmin),
    path('admin/addServices', AddServirce),
    path('admin/editServices/<int:id>', EditService),
    path('admin/deletServices/<int:id>', deletService),
    path('admin/AddCategory', AddCategory),
    path('admin/editCategory/<int:id>', EditCategory),
    path('admin/deletCategory/<int:id>', deletCategory),
    path('admin/SetSettingProject/<int:id>/', UpdateProject),

    #Peticiones
    path('admin/actualizar_estado_solicitud/<int:solicitud_id>/<str:estado>/', actualizar_estado_solicitud),
    path('admin/SetCatServ/<int:serv_id>/<int:cat_id>/<str:stade>', setCatServ),
    path('admin/SetStadeServ/<int:serv_id>', setStadeServ),
    path('admin/EnvioMensaje/<int:id>/', EnvioMensaje),
    path('client/AlterService/', AlerService),
    path('client/RembolsoServicio/', RembolsoService, name='rembolso_service'),
    path('client/Infotrans', AddIDCash, name='rembolso_service'),
]

ALLOWED_HOSTS = ['www.paypal.com']