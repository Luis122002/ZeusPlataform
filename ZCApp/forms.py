from ZCApp import models
from django import forms
from django.forms.widgets import DateTimeInput
from datetime import datetime
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm, PasswordChangeForm
from django.contrib.auth.password_validation import validate_password
from django.forms import DateTimeInput, NumberInput, TimeInput, widgets
from datetime import datetime, timedelta, timezone
import re

class FormUser(UserCreationForm):
    class Meta:
        model = models.Usuarios
        fields = ('first_name','last_name','email','username','telefono')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


        for field_name, field in self.fields.items():
            if isinstance(field.widget, (forms.TextInput, forms.EmailInput, forms.Textarea)):
                field.widget.attrs.update({'class': 'form-control'})


        self.fields['password1'].widget.attrs.update({'class': 'form-control'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control'})
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        
        # Regex para validar el formato del RUT: "12345678-9" o "12345678-K"
        rut_regex = re.compile(r'^\d{7,8}-[\dkK]$')
        
        if not rut_regex.match(username):
            raise forms.ValidationError("El RUT debe tener el formato '12345678-9' o '12345678-K'.")
        
        return username


class EditUserForm(UserChangeForm):
    new_password = forms.CharField(label='Nueva contraseña', required=False, widget=forms.PasswordInput, help_text='Deje este campo vacío para mantener la contraseña actual')
    confirm_password = forms.CharField(label='Confirmar contraseña', required=False, widget=forms.PasswordInput, help_text='')

    class Meta:
        model = models.Usuarios
        fields = ('first_name', 'last_name', 'email', 'username', 'telefono')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            if field_name != 'new_password' and field_name != 'confirm_password' and isinstance(field.widget, (forms.TextInput, forms.EmailInput, forms.Textarea)):
                field.widget.attrs.update({'class': 'form-control'})

        self.fields['password'].help_text = ''  # Elimina el mensaje de ayuda de password
        self.fields['new_password'].widget.attrs.update({'class': 'form-control'})
        self.fields['confirm_password'].widget.attrs.update({'class': 'form-control'})

    def clean_new_password(self):
        new_password = self.cleaned_data.get('new_password')
        if new_password:
            validate_password(new_password, self.instance)  # Aplica las condiciones de seguridad de Django
        return new_password

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get('new_password')
        confirm_password = cleaned_data.get('confirm_password')

        if not new_password and not confirm_password:
            return cleaned_data  # Si ambos están vacíos, no hacemos ninguna validación y mantenemos la contraseña actual

        if new_password and confirm_password and new_password != confirm_password:
            raise ValidationError(_('Las contraseñas no coinciden.'), code='password_mismatch')

        return cleaned_data
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        
        # Regex para validar el formato del RUT: "12345678-9" o "12345678-K"
        rut_regex = re.compile(r'^\d{7,8}-[\dkK]$')
        
        if not rut_regex.match(username):
            raise forms.ValidationError("El RUT debe tener el formato '12345678-9' o '12345678-K'.")
        
        return username


class LoginUsers(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        for field_name, field in self.fields.items():
            if isinstance(field.widget, (forms.TextInput, forms.PasswordInput)):
                field.widget.attrs.update({'class': 'form-control'})
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        
        # Regex para validar el formato del RUT: "12345678-9" o "12345678-K"
        rut_regex = re.compile(r'^\d{7,8}-[\dkK]$')
        
        if not rut_regex.match(username):
            raise forms.ValidationError("El RUT debe tener el formato '12345678-9' o '12345678-K'.")
        
        return username


class FormServices(forms.ModelForm):
    class Meta:
        model = models.Servicios
        fields = '__all__'
        widgets = {
            'Descripcion_servicio': forms.Textarea(attrs={'class': 'form-control', 'rows': '4'}),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Asigna las clases de Bootstrap a todos los campos
        for field_name, field in self.fields.items():
            if isinstance(field.widget, (forms.TextInput, forms.EmailInput)):
                field.widget.attrs.update({'class': 'form-control'})
            elif isinstance(field.widget, forms.Textarea):
                # Si es el campo Descripcion_servicio, ajusta el widget a Textarea
                field.widget.attrs.update({'class': 'form-control', 'rows': '4'})


class FormCategory(forms.ModelForm):

    class Meta:
        model = models.categoria
        fields = '__all__'
        widgets = {
            'Descripcion_categoria': forms.Textarea(attrs={'class': 'form-control', 'rows': '4'}),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


        for field_name, field in self.fields.items():
            if isinstance(field.widget, (forms.TextInput, forms.EmailInput, forms.Textarea)):
                field.widget.attrs.update({'class': 'form-control'})

class FormCatServ(forms.ModelForm):

    class Meta:
        model = models.Categoria_servicios
        fields = '__all__'
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


        for field_name, field in self.fields.items():
            if isinstance(field.widget, (forms.TextInput, forms.EmailInput, forms.Textarea)):
                field.widget.attrs.update({'class': 'form-control'})


class FormAcquireService(forms.ModelForm):
    class Meta:
        model = models.Solicitud_servicios
        fields = ['Direccion_limpieza', 'Fecha_servicio', 'Servicios']

    Fecha_servicio = forms.DateTimeField(
        widget=forms.widgets.DateTimeInput(
            format='%Y-%m-%d %H:%M',
            attrs={'type': 'datetime-local', 'class': 'form-control'}
        ),
        input_formats=['%Y-%m-%d %H:%M']
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Define la zona horaria para Santiago
        santiago_tz = timezone(timedelta(hours=-3))  # UTC-3 para Chile/Continental

        # Obtiene la fecha y hora actual en la zona horaria de Santiago
        now_santiago = datetime.now(santiago_tz)

        # Establece el valor predeterminado para el campo 'Fecha_servicio'
        self.fields['Fecha_servicio'].widget.attrs['value'] = now_santiago.strftime('%Y-%m-%dT%H:%M')

    def clean_Fecha_servicio(self):
        fecha_servicio = self.cleaned_data.get('Fecha_servicio')
        if fecha_servicio <= datetime.now(fecha_servicio.tzinfo) + timedelta(days=1):
            raise forms.ValidationError("La fecha de servicio debe ser al menos 1 día en el futuro.")
        return fecha_servicio