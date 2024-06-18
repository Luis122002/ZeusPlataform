#Documento de acceso de servidor de forma asincroniza y libre de procesos lineales o con espera para la comunicación y conectvidad de la plataforma

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ZeusPlataform.settings')

application = get_asgi_application()
