#servicios/autenticacion.py
import bcrypt
from dominio.usuario import Usuario
from persistencia.usuario_dao import UsuarioDAO

MAX_BYTES_BCRYPT = 72

def crear_hash(clave):
    clave = Usuario.validar_clave(clave)
    clave_bytes = clave.encode("utf-8")
    if len(clave_bytes) > MAX_BYTES_BCRYPT:
        raise ValueError("Máximo 72 bytes UTF-8 para bcrypt.")
    return bcrypt.hashpw(
        clave_bytes, bcrypt.gensalt()
    ).decode("utf-8")

#servicios/autenticacion.py  
def registrar_usuario(nombre, clave):
    nombre = Usuario.normalizar_usuario(nombre)
    if UsuarioDAO.buscar_por_nombre(nombre) is not None:
        raise ValueError("No se pudo crear esa cuenta.")
    
    hash_guardado = crear_hash(clave)
    usuario = Usuario(nombre, hash_guardado)
    
    return UsuarioDAO.insertar(
        usuario.nombre_usuario, usuario.password_hash
    )
    
#servicios/autenticacion.py
def autenticar(nombre, clave):
    nombre = Usuario.normalizar_usuario(nombre)
    
    if not isinstance(clave, str):
        return None
    clave_bytes = clave.encode("utf-8")
    
    if not 0 < len(clave_bytes) <= MAX_BYTES_BCRYPT:
        return None
    
    cuenta = UsuarioDAO.buscar_por_nombre(nombre)
    
    if cuenta is None:
        return None
    
    if not bcrypt.checkpw(
        clave_bytes, cuenta["password_hash"].encode("utf-8")
    ):
        return None
    
    return {"id": cuenta["id"], "nombre_usuario": cuenta["nombre_usuario"]}