# menu_usuario.py
from getpass import getpass
from servicios.autenticacion import (
    registrar_usuario,
    autenticar,
)

def solicitar_login():
    nombre = input("Usuario: ")
    clave = getpass("Contraseña: ")
    
    try:
        usuario = autenticar(nombre, clave)
    except (TypeError, ValueError):
        print("No se pudo validar el acceso.")
        return None
    if usuario is None:
        print("Usuario o contraseña incorrectos.")
    else:
        print("Sesión iniciada correctamente.")
    return usuario

def consultar_indicador(usuario_actual):
    if usuario_actual is None:
        print("Inicie sesión para consultar indicadores.")
        return
    #mostrar_indicador()  # Reutilizar la consulta de la clase 2.