from dominio.empleado import Empleado

class Proyecto:
    """Un proyecto puede tener cero o muchos empleados."""

    def __init__(self, nombre, id=None):
        if not isinstance(nombre, str) or not nombre.strip():
            raise ValueError("El nombre del proyecto no puede estar vacío")
        self.id = id
        self.nombre = nombre.strip()
        self.empleados = []

    def agregar_empleado(self, empleado):
        if not isinstance(empleado, Empleado):
            raise TypeError("Se esperaba una instancia de Empleado")
        empleado.agregar_proyecto(self)

    def quitar_empleado(self, empleado):
        if empleado in self.empleados:
            empleado.quitar_proyecto(self)
        
    def __str__(self):
        return f"Proyecto(id={self.id}, nombre={self.nombre})"

    def mostrar_datos(self) -> str:
        return f"id:{self.id} {self.nombre}"