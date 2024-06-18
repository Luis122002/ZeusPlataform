#Documento propio para gestionar las credenciales y registros de validación, en el que se obtiene el token de trancacción de los clientes para validad su rembolso
# y los registros encriptados por el sistema y utilizados en un archivo "json" protegido.

#Dependencias y paquetes de uso
from django.core.cache import cache
import json
import os
import requests
import paypalrestsdk
from cryptography.fernet import Fernet

# Ruta al archivo JSON donde se almacenan las credenciales
JSON_FILE = 'credentials.json'

#Funcion de encriptación, crea una clave unica para el archivo json.
def generate_secret_key():
    return Fernet.generate_key()

#Función para cargar credenciales, si el servidor es nuevo crea un documento vacio.
def load_credentials():
    credentials = cache.get('credentials')
    if credentials is None:
        if not os.path.exists(JSON_FILE):
            secret_key = generate_secret_key()
            credentials = {
                'PAYPAL_CLIENT_ID': '',
                'PAYPAL_CLIENT_SECRET': '',
                'EMAIL_HOST_USER': '',
                'EMAIL_HOST_PASSWORD': '',
                'PAYPAL_PROJECT_MODE':'',
                'PLATAFORM_2_RESOURCE':'',
                'PLATAFORM_2_PRODUCTS':'',
                'KEY_CODE': secret_key
            }
            save_credentials(credentials)
        else:
            try:
                with open(JSON_FILE, 'r') as file:
                    credentials = json.load(file)
                for key, value in credentials.items():
                    if isinstance(value, bytes):  
                        value = decrypt_value(value, credentials['KEY_CODE']) 
                    credentials[key] = value
            except json.decoder.JSONDecodeError:
                credentials = {}
        cache.set('credentials', credentials)
    return credentials


#Función para guardar los registros de las credenciales, Requiere reiniciar el servidor para aplicar los cambios.
def save_credentials(credentials):
    encrypted_credentials = {}
    for key, value in credentials.items():
        if isinstance(value, bytes): 
            value = value.decode() 
        encrypted_credentials[key] = value
    with open(JSON_FILE, 'w') as file:
        json.dump(encrypted_credentials, file)
    # Guardar las credenciales en la caché
    cache.set('credentials', credentials)

#Función para actualizar credenciales, primero toma los valores y luego aplica la función de guardado de credenciales
def update_credential(name, value):

    credentials = load_credentials()
    credentials[name] = encrypt_value(value, credentials['KEY_CODE'])  # Encriptar el valor
    save_credentials(credentials)

#Función de encriptar credenciales, toma el valor y lo encripta de acuerdo a la clave generada por el sistema
def encrypt_value(value, secret_key):
    cipher_suite = Fernet(secret_key)
    encrypted_value = cipher_suite.encrypt(value.encode())
    return encrypted_value

#Funcion de desencriptar credenciales, toma el valor encriptado y lo traduce junto con la clave generada por el sistema,
# se ejecuta al iniciar la plataforma y muestra al administrador los valores del JSON traducidos
def decrypt_value(encrypted_value, secret_key):
    if encrypted_value == "":
        return ""
    cipher_suite = Fernet(secret_key)
    decrypted_value = cipher_suite.decrypt(encrypted_value)
    return decrypted_value.decode()
    

#función para obtener detalles de una transacción, disponible para formato encriptado y con inicial "PAYID-", funcion manejado solo por el servidor para autentificar el rembolso.
def obtener_detalles_transaccion_paypal(id_transaccion_paypal):
    token = obtener_token_paypal(PAYPAL_CLIENT_ID, PAYPAL_CLIENT_SECRET)
    if token:
        if id_transaccion_paypal.startswith("PAYID-"):
            try:
                sale = paypalrestsdk.Payment.find(id_transaccion_paypal)
                return sale.to_dict()
            except paypalrestsdk.exceptions.ResourceNotFound as e:
                print("Error: Transacción no encontrada en PayPal")
                return None
            except Exception as e:
                print(f"Error al obtener detalles de la transacción en PayPal: {e}")
                return None
        else:
            paypalrestsdk.configure({
            "mode": PAYPAL_PROJECT_MODE,
            "client_id": PAYPAL_CLIENT_ID,
            "client_secret": PAYPAL_CLIENT_SECRET
            })
            headers = {
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json"
            }
            url = ""
            if PAYPAL_PROJECT_MODE == "sandbox":
                url = f"https://api.sandbox.paypal.com/v2/checkout/orders/{id_transaccion_paypal}"
            else:
                url = f"https://api.paypal.com/v2/checkout/orders/{id_transaccion_paypal}"
            try:
                response = requests.get(url, headers=headers)
                if response.status_code == 200:
                    return response.json()
                else:
                    print("Error al obtener detalles de la transacción en PayPal:", response.text)
                    return None
            except Exception as e:
                print("Error al realizar la solicitud a PayPal:", e)
                return None
    else:
        print("Error al obtener el token de acceso de PayPal.")
        return None


#Función de obtención de token de paypal, comprueba la seguridad de Paypal sobre el acceso por la transacción realizada al dueño de la cuenta empresarial
# accediendo por el id y clave secreta, la acción es condicionado por el modo de paypal que la plataforma utiliza en modo "Sandbox" para probar y "Live" para producción.
def obtener_token_paypal(client_id, secret):
    if PAYPAL_PROJECT_MODE == "sandbox":
        url = "https://api.sandbox.paypal.com/v1/oauth2/token"
    else:
        url = "https://api.paypal.com/v1/oauth2/token"
    data = {
        "grant_type": "client_credentials"
    }
    headers = {
        "Accept": "application/json",
        "Accept-Language": "en_US"
    }
    auth = (client_id, secret)

    try:
        response = requests.post(url, data=data, headers=headers, auth=auth)
        if response.status_code == 200:
            return response.json()["access_token"]
        else:
            print("Error al obtener token de acceso de PayPal:", response.text)
            return None
    except Exception as e:
        print("Error al realizar la solicitud de token de acceso a PayPal:", e)
        return None




# Variables que representan las claves de las credenciales
credentials = load_credentials()
secret_key = credentials.get('KEY_CODE', '')
PAYPAL_CLIENT_ID = decrypt_value(credentials.get('PAYPAL_CLIENT_ID', ''), secret_key)
PAYPAL_CLIENT_SECRET = decrypt_value(credentials.get('PAYPAL_CLIENT_SECRET', ''), secret_key)
EMAIL_HOST_USER = decrypt_value(credentials.get('EMAIL_HOST_USER', ''), secret_key)
EMAIL_HOST_PASSWORD = decrypt_value(credentials.get('EMAIL_HOST_PASSWORD', ''), secret_key)
PAYPAL_PROJECT_MODE = decrypt_value(credentials.get('PAYPAL_PROJECT_MODE', ''), secret_key)
PLATAFORM_2_RESOURCE = decrypt_value(credentials.get('PLATAFORM_2_RESOURCE', ''), secret_key)
PLATAFORM_2_PRODUCTS = decrypt_value(credentials.get('PLATAFORM_2_PRODUCTS', ''), secret_key)