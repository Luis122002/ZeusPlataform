#Documento de configuraciónes de la plataforma para la ejecución. Incluye ajustes de idioma, hora, dirección de puertos a ejecutar, acceso a credencales y uso de paquetes.


#Dependencias y paquetes necesarios
from ZCApp.credentials import PAYPAL_CLIENT_ID, PAYPAL_CLIENT_SECRET, EMAIL_HOST_USER, EMAIL_HOST_PASSWORD, PLATAFORM_2_RESOURCE, PLATAFORM_2_PRODUCTS
from pathlib import Path
import os

#Ruta de ejecución del proyecto
BASE_DIR = Path(__file__).resolve().parent.parent


#Codigo secreto del proyecto
SECRET_KEY = 'django-insecure-uoc^a=0zona&)v1z0-b2koimg3@@vzkr&w_n(3=7@h(lv@7o2k'

#Opciones de seguridad y de depuración
DEBUG = True
SECURE_SSL_REDIRECT = False
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SAMESITE = 'None'
CSRF_COOKIE_SAMESITE = 'None'
SECURE_HSTS_SECONDS = 31536000 

#Permisos de acceso de direcciones IPV4
ALLOWED_HOSTS = ['*']

#Opciones de mensajes y accesos
MESSAGE_STORAGE = "django.contrib.messages.storage.cookie.CookieStorage"
AUTH_USER_MODEL = 'ZCApp.Usuarios'
LOGIN_URL = '/Login'


#Definición de aplicaciónes
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'phonenumber_field',
    'paypalrestsdk',
    'ZCApp',
    'allauth',
    'allauth.account',
    'django.contrib.sites'
]
SITE_ID = 1
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware'
]
ROOT_URLCONF = 'ZeusPlataform.urls'

#Ruta de acceso de archivos dela plataforma
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

#Documento de inicio de plataforma en el servidor
WSGI_APPLICATION = 'ZeusPlataform.wsgi.application'



#Base de datos del proyecto (Editar para usar la base de datos)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'zeus_clean_db',
        'USER': 'root',
        'PORT': 3316,
        'PASSWORD': ''
    }
}



#Validadores
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]



#Idioma y zona horaria
LANGUAGE_CODE = 'es-esp'
TIME_ZONE = 'America/Santiago'
USE_I18N = True
USE_TZ = True


#Dirección de archivos estaticos
STATIC_URL = 'static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR,'static')]


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

#Ajustes del correo electronico y acceso de cuenta en el proyecto
PROJECT_NAME = "Zeus Clean"
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = EMAIL_HOST_USER
EMAIL_HOST_PASSWORD = EMAIL_HOST_PASSWORD
ACCOUNT_AUTHENTICATION_METHOD = 'username_email'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_USERNAME_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'
ACCOUNT_LOGIN_ON_PASSWORD_RESET = False
ACCOUNT_SIGNUP_ENABLED = False

ACCOUNT_PASSWORD_RESET_CONFIRM = "ZCAPP:custom_reset_password"
PASSWORD_RESET_EMAIL_TEMPLATE = 'account/email/password_reset_key_message.txt'

#Ajuste de redirección de cuenta
LOGIN_REDIRECT_URL = '/Login'
LOGOUT_REDIRECT_URL = '/'

#Credenciales
PAYPAL_CLIENT_ID = PAYPAL_CLIENT_ID
PAYPAL_CLIENT_SECRET = PAYPAL_CLIENT_SECRET

PLATAFORM_2_RESOURCE = PLATAFORM_2_RESOURCE
PLATAFORM_2_PRODUCTS = PLATAFORM_2_PRODUCTS

CORS_ALLOWED_ORIGINS = [
    "https://www.paypal.com/",
    "https://www.paypal.com/sdk/js?client-id=" + PAYPAL_CLIENT_ID,
    "https://www.sandbox.paypal.com/",
    "https://www.sandbox.paypal.com/sdk/js?client-id=" + PAYPAL_CLIENT_ID,
]





