# persistencia/usuario_dao.py
from dominio.usuario import Usuario
from persistencia.conexion import abrir_conexion, marcador_sql

class UsuarioDAO:
    @staticmethod
    def insertar(usuario):
        conexion = None

        try:
            conexion = abrir_conexion()
            cursor = conexion.cursor()
            marcador = marcador_sql()
            sql = (
                "INSERT INTO usuario (empleado_id, nombre_usuario, password_hash) "
                f"VALUES ({marcador}, {marcador}, {marcador})"
            )

            cursor.execute(
                sql,
                (usuario.empleado_id, usuario.nombre_usuario, usuario.password_hash)
            )
            usuario.id = cursor.lastrowid
            conexion.commit()
            return usuario
        except Exception:
            if conexion:
                conexion.rollback()
            raise
        finally:
            if conexion:
                conexion.close()

    @staticmethod
    def _fila_a_usuario(fila):
        return Usuario(
            id=fila[0],
            empleado_id=fila[1],
            nombre_usuario=fila[2],
            password_hash=fila[3]
        )

    @staticmethod
    def buscar_por_id(id_usuario):
        conexion = abrir_conexion()
        try:
            cursor = conexion.cursor()
            marcador = marcador_sql()
            sql = (
                "SELECT id, empleado_id, nombre_usuario, password_hash "
                f"FROM usuario WHERE id = {marcador}"
            )
            cursor.execute(sql, (id_usuario,))
            fila = cursor.fetchone()
        finally:
            conexion.close()

        if fila is None:
            return None

        return UsuarioDAO._fila_a_usuario(fila)

    
    @staticmethod
    def buscar_por_nombre(nombre_usuario):
        conexion = abrir_conexion()
        try:
            cursor = conexion.cursor()
            marcador = marcador_sql()
            sql = (
                "SELECT id, empleado_id, nombre_usuario, password_hash "
                f"FROM usuario WHERE nombre_usuario = {marcador}"
            )

            cursor.execute(sql, (nombre_usuario,))
            fila = cursor.fetchone()
        finally:
            conexion.close()

        if fila is None:
            return None

        return UsuarioDAO._fila_a_usuario(fila)
    
    @staticmethod
    def listar(filtrar_por_empleado_id=None):
        conexion = abrir_conexion()
        try:
            cursor = conexion.cursor()
            sql = "SELECT id, empleado_id, nombre_usuario, password_hash FROM usuario"
            if filtrar_por_empleado_id is not None:
                marcador = marcador_sql()
                sql += f" WHERE empleado_id = {marcador}"
                cursor.execute(sql, (filtrar_por_empleado_id,))
            else:
                cursor.execute(sql)
                
            filas = cursor.fetchall()
            return [UsuarioDAO._fila_a_usuario(fila) for fila in filas]
        finally:
            conexion.close()

    @staticmethod
    def listar_por_empleado(empleado_id):
        conexion = abrir_conexion()
        try:
            cursor = conexion.cursor()
            marcador = marcador_sql()
            sql = (
                "SELECT id, empleado_id, nombre_usuario, password_hash "
                f"FROM usuario WHERE empleado_id = {marcador}"
            )
            cursor.execute(sql, (empleado_id,))
            filas = cursor.fetchall()
            return [UsuarioDAO._fila_a_usuario(fila) for fila in filas]
        finally:
            conexion.close()
    
    
    @staticmethod
    def actualizar(usuario):
        conexion = None

        try:
            conexion = abrir_conexion()
            cursor = conexion.cursor()

            marca = marcador_sql()
            sql = (
                "UPDATE usuario "
                f"SET empleado_id = {marca}, nombre_usuario = {marca}, password_hash = {marca} "
                f"WHERE id = {marca}"
            )

            cursor.execute(
                sql,
                (
                    usuario.empleado_id,
                    usuario.nombre_usuario,
                    usuario.password_hash,
                    usuario.id
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
    def eliminar(id_usuario):
        conexion = None

        try:
            conexion = abrir_conexion()
            cursor = conexion.cursor()
            marca = marcador_sql()
            sql = f"DELETE FROM usuario WHERE id = {marca}"

            cursor.execute(sql, (id_usuario,))
            conexion.commit()
            return cursor.rowcount > 0
        except Exception:
            if conexion:
                conexion.rollback()
            raise
        finally:
            if conexion:
                conexion.close()