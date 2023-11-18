"""
URL configuration for ZeusPlataform project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from ZCApp.views import MainAdmin, AddServirce, AddCategory, AddLinkCat, MainPage, Login, AddUser, Unlogin, AcquireServce


urlpatterns = [
    path('Login/', Login),
    path('Exit/', Unlogin),
    path('Acquire_Service/', AcquireServce),
    path('Register/', AddUser),
    path('admin/', MainAdmin),
    path('admin/addServices', AddServirce),
    path('admin/AddCategory', AddCategory),
    path('admin/linkedService', AddLinkCat),
    path('', MainPage)
]
