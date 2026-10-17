# src/dominio/empleado.py​
class Empleado:
    MIN_NOMBRE = 2
    MAX_NOMBRE = 100
    MIN_CORREO = 6
    MAX_CORREO = 254

    def __init__(self, nombre, correo, id=None):
        self.id = id
        self.nombre = self.validar_nombre(nombre)
        self.correo = self.validar_correo(correo)
        self.departamento = None
        self.proyectos = []
        self.registros_tiempo = []

    @classmethod
    @staticmethod
    def validar_nombre(cls, nombre):
        if not isinstance(nombre, str):
            raise TypeError("El nombre debe ser texto")
        nombre = nombre.strip()
        if not cls.MIN_NOMBRE <= len(nombre) <= cls.MAX_NOMBRE:
            raise ValueError(
                f"El nombre debe tener entre {cls.MIN_NOMBRE} y {cls.MAX_NOMBRE} caracteres"
            )
        return nombre

    @classmethod
    @staticmethod
    def validar_correo(cls, correo):
        if not isinstance(correo, str):
            raise TypeError("El correo debe ser texto")
        correo = correo.strip()
        if not cls.MIN_CORREO <= len(correo) <= cls.MAX_CORREO or correo.count("@") != 1:
            raise ValueError("Ingrese un correo válido dentro del largo permitido")
        usuario, dominio = correo.split("@")
        if not usuario or "." not in dominio or dominio.startswith(".") or dominio.endswith("."):
            raise ValueError("Ingrese un correo válido")
        return correo

    def asignar_departamento(self, departamento):
        from dominio.departamento import Departamento

        if departamento is not None and not isinstance(departamento, Departamento):
            raise TypeError("El departamento debe ser Departamento o None")
        if self.departamento is departamento:
            return
        if self.departamento is not None:
            if self.departamento.gerente is self:
                self.departamento.gerente = None
            self.departamento.empleados.remove(self)
        self.departamento = departamento
        if departamento is not None and self not in departamento.empleados:
            departamento.empleados.append(self)

    def agregar_proyecto(self, proyecto):
        from dominio.proyecto import Proyecto

        if not isinstance(proyecto, Proyecto):
            raise TypeError("El proyecto debe ser una instancia de Proyecto")
        if proyecto not in self.proyectos:
            self.proyectos.append(proyecto)
        if self not in proyecto.empleados:
            proyecto.empleados.append(self)

    def quitar_proyecto(self, proyecto):
        if proyecto in self.proyectos:
            self.proyectos.remove(proyecto)
        if self in proyecto.empleados:
            proyecto.empleados.remove(self)

    def registrar_tiempo(self, registro_tiempo, proyecto):
        from dominio.registroTiempo import RegistroTiempo

        if proyecto not in self.proyectos:
            raise ValueError("El empleado debe estar asignado al proyecto")
        if not isinstance(registro_tiempo, RegistroTiempo):
            raise TypeError("El registro debe ser una instancia de RegistroTiempo")
        self.registros_tiempo.append(registro_tiempo)

    def mostrar_datos(self) -> str:
        return f"id:{self.id} {self.nombre} - {self.correo}"

    def __str__(self):
        return f"Empleado(id={self.id}, nombre={self.nombre}, correo={self.correo})"
