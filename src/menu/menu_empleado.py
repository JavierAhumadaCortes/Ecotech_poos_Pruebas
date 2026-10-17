# main.py
import os
import subprocess

def clear():
    command = "cls" if os.name == "nt" else "clear"
    subprocess.run(command, shell=True, check=False)

def crear_empleado():
    # Cargar el dominio al ejecutar la opción, no al importar el menú.
    from dominio.empleado import Empleado
    from persistencia.empleado_dao import EmpleadoDAO

    while True:
        try:
            nombre = Empleado.validar_nombre(input("Nombre: ").strip())
            break
        except Exception as error:
            print(f"Datos inválidos: {error}. Intenta nuevamente.")
            continue
        
    while True:   
        try:
            correo = Empleado.validar_correo(input("Correo: ").strip())
            break
        except Exception as error:
            print(f"Datos inválidos: {error}. Intenta nuevamente.")
            continue

    try:
        empleado = Empleado(nombre=nombre, correo=correo)
        EmpleadoDAO.insertar(empleado)
    except Exception as error:
        print(f"No fue posible guardar el empleado: {error}")
        return
    print("Empleado creado correctamente.")


def listar_empleados():
    from persistencia.empleado_dao import EmpleadoDAO

    empleados = EmpleadoDAO.listar()
    if not empleados:
        print("No hay empleados registrados.")
        return
    for empleado in empleados:
        print(empleado)


def pedir_id(mensaje):
    try:
        return int(input(mensaje))
    except ValueError:
        print("Ingresa un ID válido.")
        return None


def buscar_empleado():
    from persistencia.empleado_dao import EmpleadoDAO

    empleado_id = pedir_id("ID del empleado: ")
    if empleado_id is None:
        return
    empleado = EmpleadoDAO.buscar_por_id(empleado_id)
    if empleado is None:
        print("Empleado no encontrado.")
    else:
        print(empleado.mostrar_datos())


def actualizar_empleado():
    from persistencia.empleado_dao import EmpleadoDAO

    empleado_id = pedir_id("ID del empleado a actualizar: ")
    if empleado_id is None:
        return
    empleado = EmpleadoDAO.buscar_por_id(empleado_id)
    if empleado is None:
        print("Empleado no encontrado.")
        return

    nombre = input(f"Nuevo nombre [{empleado.nombre}]: ").strip()
    correo = input(f"Nuevo correo [{empleado.correo}]: ").strip()
    if nombre:
        empleado.nombre = nombre
    if correo:
        empleado.correo = correo

    if EmpleadoDAO.actualizar(empleado):
        print("Empleado actualizado correctamente.")
    else:
        print("No fue posible actualizar el empleado.")


def eliminar_empleado():
    from persistencia.empleado_dao import EmpleadoDAO

    empleado_id = pedir_id("ID del empleado a eliminar: ")
    if empleado_id is None:
        return
    if EmpleadoDAO.eliminar(empleado_id):
        print("Empleado eliminado correctamente.")
    else:
        print("Empleado no encontrado.")


def menu_empleado():
    opciones = {
        "1": crear_empleado,
        "2": listar_empleados,
        "3": buscar_empleado,
        "4": actualizar_empleado,
        "5": eliminar_empleado,
    }
    
    while True:
        print("\n--- Menú de empleados ---")
        print("1. Crear empleado")
        print("2. Listar empleados")
        print("3. Buscar empleado por ID")
        print("4. Actualizar empleado")
        print("5. Eliminar empleado")
        print("0. Salir")
        opcion = input("Selecciona una opción: ").strip()

        if opcion == "0":
            print("Hasta luego.")
            clear()
            break
        accion = opciones.get(opcion)
        if accion:
            accion()
        else:
            print("Opción no válida.")

