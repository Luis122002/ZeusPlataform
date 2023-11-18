from ZCApp import models
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.forms import DateTimeInput, NumberInput, TimeInput

class FormUser(UserCreationForm):
    class Meta:
        model = models.Usuarios
        fields = ('first_name','last_name','email','username','telefono','is_superuser','is_trabajador')

class FormServices(forms.ModelForm):
    
    class Meta:
        model = models.Servicios
        fields = '__all__'

class FormCategory(forms.ModelForm):
    
    class Meta:
        model = models.categoria
        fields = '__all__'

class FormCatServ(forms.ModelForm):
    
    class Meta:
        model = models.Categoria_servicios
        fields = '__all__'

class FormAcquireService(forms.ModelForm):
    class Meta:
        model = models.Solicitud_servicios
        fields = '__all__'


