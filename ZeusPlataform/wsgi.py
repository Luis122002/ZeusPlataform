#Documento de acceso del servidor con la plataforma

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ZeusPlataform.settings')

application = get_wsgi_application()
