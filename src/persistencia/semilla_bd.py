from getpass import getpass
from dominio.empleado import Empleado
from dominio.usuario import Usuario
from persistencia.empleado_dao import EmpleadoDAO
from persistencia.usuario_dao import UsuarioDAO
from servicios.autenticacion import registrar_usuario

CORREO_ADMIN = "admin@ecotech.cl"
USUARIO_ADMIN = "admin" 

def pedir_clave_inicial():
    while True:
        clave = getpass("Contraseña inicial de admin: ")

        try:
            clave = Usuario.validar_clave(clave)
        except (TypeError, ValueError) as error:
            print(error)
            continue

        confirmacion = getpass("Repita la contraseña: ")

        if clave != confirmacion:
            print("Las contraseñas no coinciden. Intenta nuevamente.")
            continue

        return clave


def verificar_vinculo(cuenta, empleado):
    if empleado is None:
        raise ValueError(
            "La cuenta admin existe, pero no encontramos "
            "al empleado esperado."
        )

    if cuenta.get("empleado_id") != empleado.id:
        raise ValueError(
            "La cuenta admin está vinculada a otro empleado "
            "o todavía no tiene un vínculo. Revíselo."
        )

def sembrar_admin():
    cuenta = UsuarioDAO.buscar_por_nombre(USUARIO_ADMIN)
    empleado = EmpleadoDAO.buscar_por_correo(CORREO_ADMIN)

    if cuenta is not None:
        verificar_vinculo(cuenta, empleado)
        print("La cuenta admin ya existe. Se conserva sin cambios.")
        return cuenta["id"]

    clave = pedir_clave_inicial()

    # Crear al empleado solamente si todavía no existe.
    if empleado is None:
        nuevo = Empleado("Administrador EcoTech", CORREO_ADMIN)
        EmpleadoDAO.insertar(nuevo)

        # Recuperar el registro persistido con su ID.
        empleado = EmpleadoDAO.buscar_por_correo(CORREO_ADMIN)

        if empleado is None:
            raise RuntimeError(
                "No se confirmó el guardado del empleado."
            )

    usuario_id = registrar_usuario(
        USUARIO_ADMIN,
        clave,
        empleado_id=empleado.id,
    )

    print("Empleado y cuenta inicial preparados.")
    return usuario_id