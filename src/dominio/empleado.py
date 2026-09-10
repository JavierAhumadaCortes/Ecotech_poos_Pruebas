# src/dominio/empleado.py​
from dominio.registroTiempo import RegistroTiempo

class Empleado:
    def __init__(self, nombre: str, correo: str):
        self.nombre = nombre
        self.correo = correo
        self._registro_tiempo = list[RegistroTiempo] = []

    def mostrar_datos(self) -> str:
        return f"{self.nombre} - {self.correo}"

    def registrar_tiempo(self, registroTiempo: RegistroTiempo) -> bool:
        if registroTiempo in self._registro_tiempo:
            return False

        self._registro_tiempo.append(registroTiempo)
        return True