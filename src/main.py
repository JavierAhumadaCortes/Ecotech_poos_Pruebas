# main.py
import os

from persistencia.crear_bd import crear_tablas
from menu.menu_empleado import menu_empleado
from servicios.autenticacion import registrar_usuario

crear_tablas()
def menu():
    while True:
        os.system("cls" if os.name == "nt" else "clear")
        print("\n--- Menú de Empleados ---")
        print("1. menu empleado")
        print("5. Salir")

        opcion = input("Selecciona una opción: ").strip()

        if opcion == "1":
            menu_empleado()
        elif opcion == "5":
            print("Saliendo del programa.")
            break
        else:
            print("Opción no válida. Intenta de nuevo.")


    
# main.py
from menu_usuario import solicitar_login, menu_privado

def main():
    while True:
        usuario_actual = solicitar_login()
        if usuario_actual is None:
            if input("Enter para reintentar o 0 para salir: ") == "0":
                return
            continue
        opcion = menu_privado(usuario_actual)
        usuario_actual = None  # Terminar el acceso de esta sesión.
        if opcion == "0":
            return
        print("Sesión cerrada. Ingrese nuevamente.")

if __name__ == "__main__":
    
    #registrar_usuario(2, "admin", "admin123123")
    main()

