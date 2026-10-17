# src/dominio/usuario.py
class Usuario:
    MIN_NOMBRE = 2
    MAX_NOMBRE = 100
    MIN_PASSWORD = 6
    MAX_PASSWORD = 254

    def __init__(self, nombre, password, id=None):
        self.id = id
        self.nombre = self.normalizar_usuario(nombre)
        self.password = self.validar_password(password)
    
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

    

    def __str__(self):
        return f"Usuario(id={self.id}, nombre={self.nombre}, password={self.password})"
