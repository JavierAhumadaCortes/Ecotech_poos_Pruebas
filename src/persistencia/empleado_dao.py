# persistencia/empleado_dao.py
from dominio.empleado import Empleado
from persistencia.conexion import abrir_conexion, marcador_sql

class EmpleadoDAO:
    @staticmethod
    def insertar(empleado):
        conexion = None

        try:
            conexion = abrir_conexion()
            cursor = conexion.cursor()
            marcador = marcador_sql()
            sql = (
                "INSERT INTO empleado (nombre, correo) "
                f"VALUES ({marcador}, {marcador})"
            )

            cursor.execute(sql, (empleado.nombre, empleado.correo))
            empleado.id = cursor.lastrowid
            conexion.commit()
            return empleado
        except Exception:
            if conexion:
                conexion.rollback()
            raise
        finally:
            if conexion:
                conexion.close()

    @staticmethod
    def insertar_departamento(empleado, departamento_id):
        conexion = None

        try:
            conexion = abrir_conexion()
            cursor = conexion.cursor()
            marcador = marcador_sql()
            sql = (
                "INSERT INTO empleado (nombre, correo, departamento_id) "
                f"VALUES ({marcador}, {marcador}, {marcador})"
            )

            cursor.execute(sql, (empleado.nombre, empleado.correo, departamento_id))
            empleado.id = cursor.lastrowid
            empleado.departamento = departamento_id
            conexion.commit()
            return empleado
        except Exception:
            if conexion:
                conexion.rollback()
            raise
        finally:
            if conexion:
                conexion.close()
    
    @staticmethod
    def _fila_a_empleado(fila):
        return Empleado(
            id=fila[0],
            nombre=fila[1],
            correo=fila[2]
        )

    @staticmethod
    def buscar_por_id(id_empleado):
        conexion = abrir_conexion()
        try:
            cursor = conexion.cursor()
            marcador = marcador_sql()
            sql = (
                "SELECT id, nombre, correo "
                f"FROM empleado WHERE id = {marcador}"
            )
            cursor.execute(sql, (id_empleado,))
            fila = cursor.fetchone()
        finally:
            conexion.close()

        if fila is None:
            return None

        return EmpleadoDAO._fila_a_empleado(fila)

    @staticmethod
    def listar(is_departamento: bool = None, filtrar_por_departamento_id=None):
        conexion = abrir_conexion()
        try:
            cursor = conexion.cursor()
            if filtrar_por_departamento_id is not None:
                cursor.execute("SELECT id, nombre, correo, departamento_id FROM empleado WHERE departamento_id = ?", (filtrar_por_departamento_id,))
            else:
                if is_departamento is True:
                    cursor.execute("SELECT id, nombre, correo, departamento_id FROM empleado WHERE departamento_id IS NOT NULL")
                elif is_departamento is False:
                    cursor.execute("SELECT id, nombre, correo, departamento_id FROM empleado WHERE departamento_id IS NULL")
                else:
                    cursor.execute("SELECT id, nombre, correo, departamento_id FROM empleado")
                
            filas = cursor.fetchall()
            return [EmpleadoDAO._fila_a_empleado(fila) for fila in filas]
        finally:
            conexion.close()
    
    @staticmethod
    def listar_empleados_y_departamentos():
        conexion = abrir_conexion()
        try:
            cursor = conexion.cursor()
            cursor.execute(
                "SELECT e.id, e.nombre, e.correo, d.id as departamento_id, d.nombre as departamento_nombre "
                "FROM empleado e "
                "LEFT JOIN departamento d ON e.departamento_id = d.id"
            )
            filas = cursor.fetchall()
            empleados = []
            for fila in filas:
                empleado = EmpleadoDAO._fila_a_empleado(fila[:3])
                if fila[3] is not None:
                    empleado.departamento = {
                        "id": fila[3],
                        "nombre": fila[4]
                    }
                empleados.append(empleado)
            return empleados
        finally:
            conexion.close()
    
    @staticmethod
    def listar_por_departamento(departamento_id):
        conexion = abrir_conexion()
        try:
            cursor = conexion.cursor()
            marcador = marcador_sql()
            sql = (
                "SELECT id, nombre, correo "
                f"FROM empleado WHERE departamento_id = {marcador}"
            )
            cursor.execute(sql, (departamento_id,))
            filas = cursor.fetchall()
            return [EmpleadoDAO._fila_a_empleado(fila) for fila in filas]
        finally:
            conexion.close()
    
    
    @staticmethod
    def actualizar(empleado):
        conexion = None

        try:
            conexion = abrir_conexion()
            cursor = conexion.cursor()

            marca = marcador_sql()
            sql = (
                "UPDATE empleado "
                f"SET nombre = {marca}, correo = {marca} "
                f"WHERE id = {marca}"
            )

            cursor.execute(
                sql,
                (
                    empleado.nombre,
                    empleado.correo,
                    empleado.id
                )
            )

            conexion.commit()
            return cursor.rowcount > 0

        except Exception:
            if conexion:
                conexion.rollback()
            raise

        finally:
            if conexion:
                conexion.close()

    @staticmethod
    def eliminar(id_empleado):
        conexion = None

        try:
            conexion = abrir_conexion()
            cursor = conexion.cursor()
            marca = marcador_sql()
            sql = f"DELETE FROM empleado WHERE id = {marca}"

            cursor.execute(sql, (id_empleado,))
            conexion.commit()
            return cursor.rowcount > 0
        except Exception:
            if conexion:
                conexion.rollback()
            raise
        finally:
            if conexion:
                conexion.close()