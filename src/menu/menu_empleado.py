# main.py
import os
import subprocess

def clear():
    command = "cls" if os.name == "nt" else "clear"
    subprocess.run(command, shell=True, check=False)

def pedir_dato(mensaje, validador, valor_actual=None):
    while True:
        entrada = input(mensaje)

        # En una actualización, Enter conserva el valor actual.
        if valor_actual is not None and not entrada.strip():
            return valor_actual

        try:
            return validador(entrada)
        except (TypeError, ValueError) as error:
            print(f"{error} Intenta nuevamente.")

def crear_empleado():
    from dominio.empleado import Empleado
    from persistencia.empleado_dao import EmpleadoDAO

    nombre = pedir_dato(
        "Nombre: ",
        Empleado.validar_nombre,
    )

    correo = pedir_dato(
        "Correo: ",
        Empleado.validar_correo,
    )

    empleado = Empleado(nombre=nombre, correo=correo)

    # El DAO debe confirmar el guardado o lanzar una excepción.
    EmpleadoDAO.insertar(empleado)

    print("Empleado creado correctamente.")

def actualizar_empleado():
    from dominio.empleado import Empleado
    from persistencia.empleado_dao import EmpleadoDAO

    empleado_id = pedir_id("ID del empleado a actualizar: ")
    if empleado_id is None:
        return

    empleado = EmpleadoDAO.buscar_por_id(empleado_id)

    if empleado is None:
        print("Empleado no encontrado.")
        return

    nombre = pedir_dato(
        f"Nuevo nombre [{empleado.nombre}] (Enter para conservar): ",
        Empleado.validar_nombre,
        valor_actual=empleado.nombre,
    )

    correo = pedir_dato(
        f"Nuevo correo [{empleado.correo}] (Enter para conservar): ",
        Empleado.validar_correo,
        valor_actual=empleado.correo,
    )

    empleado.actualizar_datos(nombre, correo)

    if EmpleadoDAO.actualizar(empleado):
        print("Empleado actualizado correctamente.")
    else:
        print("No fue posible actualizar el empleado.")
        
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
