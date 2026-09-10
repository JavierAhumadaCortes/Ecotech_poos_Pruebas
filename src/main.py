# src/main.py​
from dominio.empleado import Empleado
from dominio.departamento import Departamento
from dominio.departamento import RegistroTiempo

empleado = Empleado(
    nombre="Ana Torres",
    correo="ana.torres@ecotech.cl"
)
empleado2 = Empleado(
    nombre="Ana3 Torres",
    correo="ana.torres@ecotech.cl"
)
empleado3 = Empleado(
    nombre="Ana4 Torres",
    correo="ana.torres@ecotech.cl"
)

empleado3.registrar_tiempo(RegistroTiempo('10/12/2026','10:50'))
empleado3.registrar_tiempo(RegistroTiempo('11/12/2026','10:50'))
rgs1 = RegistroTiempo('12/12/2026','10:50')
empleado3.registrar_tiempo(rgs1)

#print(empleado.mostrar_datos())
desarrollo = Departamento("DEp Desarrollo")
desarrollo.agregar_empleado(empleado)
desarrollo.agregar_empleado(empleado2)
desarrollo.agregar_empleado(empleado3)


print(desarrollo.cantidad_empleados())

for empleado in desarrollo.empleados:
    print(empleado.mostrar_datos())