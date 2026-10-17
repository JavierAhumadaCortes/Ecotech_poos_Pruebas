# En servicios/autenticacion.py, junto a los helpers.
# Importar UsuarioDAO desde la ruta real del proyecto.
from persistencia.usuario_dao import UsuarioDAO
import bcrypt


def registrar_usuario(nombre, clave):
    nombre = normalizar_usuario(nombre)
    if UsuarioDAO.buscar_por_nombre(nombre) is not None:
        raise ValueError("No se pudo crear esa cuenta.")
    hash_guardado = crear_hash(clave)
    return UsuarioDAO.insertar(nombre, hash_guardado)

def crear_hash(clave):
    if len(clave) < 15:
        raise ValueError("Use una frase de al menos 15 caracteres.")
    clave_bytes = clave.encode("utf-8")
    if len(clave_bytes) > 72:
        raise ValueError("Máximo 72 bytes UTF-8 para bcrypt.")
    return bcrypt.hashpw(
        clave_bytes, bcrypt.gensalt()
    ).decode("utf-8")
    

@classmethod    
def normalizar_usuario(nombre):
    # 1. LIMPIEZA: Elimina espacios en blanco a los 
    # lados y convierte todo a minúsculas para 
    # evitar duplicados como "Admin" y "admin".
    nombre = nombre.strip().lower()
    
    # 2. SEGURIDAD (Longitud): Evita nombres vacíos y 
    # previene ataques enviando textos inmensos que 
    # saturen la base de datos.
    if not 3 <= len(nombre) <= 40:
        raise ValueError("Usuario: entre 3 y 40 caracteres.")
        
    # 3. SEGURIDAD (Formato): Solo permite letras, números y guiones bajos estándar (ASCII). 
    # Bloquea caracteres especiales (<, >, ', ") previniendo ataques de inyección (SQL/XSS).
    if not all(c.isascii() and (c.isalnum() or c == "_")
            for c in nombre):
        raise ValueError("Use letras, números o guion bajo.")
        
    # 4. RETORNO: Devuelve el nombre ya validado y seguro para guardarlo en tu objeto o modelo.
    return nombre

@classmethod
def validar_password(cls, password):
    if not isinstance(password, str):
        raise TypeError("La contraseña debe ser texto")
    password = password.strip()
    if not cls.MIN_PASSWORD <= len(password) <= cls.MAX_PASSWORD:
        raise ValueError(
            f"La contraseña debe tener entre {cls.MIN_PASSWORD} y {cls.MAX_PASSWORD} caracteres"
        )
    return password


def autenticar(nombre, clave):
    nombre = normalizar_usuario(nombre)
    clave_bytes = clave.encode("utf-8")
    if not clave_bytes or len(clave_bytes) > 72:
        return None
    usuario = UsuarioDAO.buscar_por_nombre(nombre)
    if usuario is None:
        return None
    valido = bcrypt.checkpw(
        clave_bytes, usuario["password_hash"].encode("utf-8")
    )
    if not valido:
        return None
    return {"id": usuario["id"], "nombre_usuario": usuario["nombre_usuario"]}