# src/dominio/departamento.py
from dominio.empleado import Empleado
    
class Departamento:
    """Un departamento puede tener cero o muchos empleados."""

    def __init__(self, nombre, id=None):
        if not isinstance(nombre, str) or not nombre.strip():
            raise ValueError("El nombre del departamento no puede estar vacío")
        self.id = id
        self.nombre = nombre.strip()
        self.empleados = []
        self._gerente = None

    @property
    def gerente(self):
        return self._gerente

    @gerente.setter
    def gerente(self, empleado):
        if empleado is not None and not isinstance(empleado, Empleado):
            raise TypeError("El gerente debe ser una instancia de Empleado o None")
        if empleado is not None and empleado not in self.empleados:
            raise ValueError("El gerente debe estar registrado como empleado del departamento")
        self._gerente = empleado

    def agregar_empleado(self, empleado):
        if not isinstance(empleado, Empleado):
            raise TypeError("Se esperaba una instancia de Empleado")
        empleado.asignar_departamento(self)

    def quitar_empleado(self, empleado):
        if empleado in self.empleados:
            if self.gerente is empleado:
                self.gerente = None
            empleado.asignar_departamento(None)