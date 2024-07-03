Instalación de proyecto.

requisistos previos:
-Equipo computacional o servidor operativo
-Conectividad con una base de datos vacia
-Acceso con modificación de archivos
-Instalación y acceso a Python, Github y ENV
-(AWS) Tener una VPC y relacionar el sistema EC2 con una DB de AWS Aurora y ajustar reglas de seguridad para la entrada y salida para el acceso propio del sistema

Instalación:
-Tenienod instalado Python, Github y ENV, escribibos los siguientes codigos:
  - pip install git+https://github.com/Usuario/Proyecto   | para descargar e instalar el proyecto se usa este comando en el CMD para Windows y Bash para linux, usa la dirección URL de este repositorio
  - una vez instalado accede a la carpeta con "ls" para saber el nombre de la carpeta y con "cd [nombre de carpeta]" para acceder
  - python -m venv env  | Para instalar el entorno de desarollo (env) en el que se utilizaran paquetes de python propios
  - pip install requirements.txt  | primero tiene que abrir la carpeta del proyecto donde se encuentra el archivo requrements.txt para instalar todos los paquetes necesarios
-Instalado todo el proyecto, tiene que cambiar la configuración del archivo "[proyecto/ZeusPlataform/setting.py]" en la sección de la base de datos, ajusta la configuración de acuerdo a la base de dats que tiene instalado de forma local o en AWS
-Una vez esta la base de datos conectada al proyecto se realiza los siguientes codigos para preparar el entorno de la plataforma:
  - python manage.py makemigrations
  - python manage.py makemigrations ZCAPP
  - python manage.py migrate
  - python manage.py migrate ZCAPP
- Los codigos previos son para crear y migrar la base de datos de la plataforma en la base de datos que tiene conectividad con el proyecto.
- El ultim paso para habilitar el proyecto es el siguiente codigo:
  - Python manage.py createsuperuser
- El codigo previo es para crear el usuario administrador, escribe los registros que el sistema le va indicando siendo el usuario (rut), correo, telefono y contraseña ( con confirmación)
- Corre el servidor para quepueda ejecutar la platafora y comprueba la conectividad que se puede realizar, asegurate de tener habilitado los puertos en los grupos de seguridad en caso de AWS.

Disfruta del proyecto.
