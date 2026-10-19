# src/dominio/usuario.py
class Usuario:
    MIN_USUARIO = 3
    MAX_USUARIO = 40
    MIN_CLAVE = 15

    def __init__(self, nombre_usuario, password_hash, id=None):
        self.id = id
        self.nombre_usuario = self.normalizar_usuario(nombre_usuario)
        self.password_hash = password_hash

    @classmethod
    def normalizar_usuario(cls, nombre):
        if not isinstance(nombre, str):
            raise TypeError("El usuario debe ser texto.")
        nombre = nombre.strip().lower()
        if not cls.MIN_USUARIO <= len(nombre) <= cls.MAX_USUARIO:
            raise ValueError(
                f"Usuario: entre {cls.MIN_USUARIO} y "
                f"{cls.MAX_USUARIO} caracteres."
            )
        if not all(c.isascii() and (c.isalnum() or c == "_")
                for c in nombre):
            raise ValueError("Use letras ASCII, números o guion bajo.")
        return nombre
    
    @classmethod
    def validar_clave(cls, clave):
        if not isinstance(clave, str):
            raise TypeError("La contraseña debe ser texto.")
        if len(clave) < cls.MIN_CLAVE:
            raise ValueError(
                f"Use una frase de al menos {cls.MIN_CLAVE} caracteres."
            )
        return clave  # Conservar espacios y mayúsculas.

    def __str__(self):
        return f"Usuario(id={self.id}, nombre={self.nombre})"
    


