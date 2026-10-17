from persistencia.conexion import abrir_conexion
from dominio.usuario import Usuario 


class UsuarioDAO:
	"""Persistencia CRUD para la entidad Usuario."""

	TABLA = "usuario"
	CAMPO_ID = "id_usuario"

	@staticmethod
	def _columnas(usuario):
		datos = vars(usuario)
		if not datos:
			raise ValueError("El usuario no contiene atributos para persistir")
		if any(not campo.replace("_", "").isalnum() for campo in datos):
			raise ValueError("El usuario contiene un nombre de atributo no válido")
		return datos

	@staticmethod
	def _cerrar(conexion, cursor):
		if cursor is not None:
			cursor.close()
		if conexion is not None:
			conexion.close()

	def crear(self, usuario):
		datos = self._columnas(usuario)
		campos = ", ".join(datos)
		marcadores = ", ".join(["%s"] * len(datos))
		conexion = cursor = None
		try:
			conexion = abrir_conexion()
			cursor = conexion.cursor()
			cursor.execute(
				f"INSERT INTO {self.TABLA} ({campos}) VALUES ({marcadores})",
				tuple(datos.values()),
			)
			conexion.commit()
			return cursor.lastrowid
		finally:
			self._cerrar(conexion, cursor)

	def obtener_todos(self):
		conexion = cursor = None
		try:
			conexion = abrir_conexion()
			cursor = conexion.cursor()
			cursor.execute(f"SELECT * FROM {self.TABLA}")
			return cursor.fetchall()
		finally:
			self._cerrar(conexion, cursor)

	def obtener_por_id(self, id_usuario):
		conexion = cursor = None
		try:
			conexion = abrir_conexion()
			cursor = conexion.cursor()
			cursor.execute(
				f"SELECT * FROM {self.TABLA} WHERE {self.CAMPO_ID} = %s",
				(id_usuario,),
			)
			return cursor.fetchone()
		finally:
			self._cerrar(conexion, cursor)

	def actualizar(self, usuario):
		datos = self._columnas(usuario)
		if self.CAMPO_ID not in datos:
			raise ValueError(f"El usuario debe incluir el atributo {self.CAMPO_ID}")
		id_usuario = datos.pop(self.CAMPO_ID)
		if not datos:
			raise ValueError("No hay atributos para actualizar")
		asignaciones = ", ".join(f"{campo} = %s" for campo in datos)
		conexion = cursor = None
		try:
			conexion = abrir_conexion()
			cursor = conexion.cursor()
			cursor.execute(
				f"UPDATE {self.TABLA} SET {asignaciones} WHERE {self.CAMPO_ID} = %s",
				(*datos.values(), id_usuario),
			)
			conexion.commit()
			return cursor.rowcount
		finally:
			self._cerrar(conexion, cursor)

	def eliminar(self, id_usuario):
		conexion = cursor = None
		try:
			conexion = abrir_conexion()
			cursor = conexion.cursor()
			cursor.execute(
				f"DELETE FROM {self.TABLA} WHERE {self.CAMPO_ID} = %s",
				(id_usuario,),
			)
			conexion.commit()
			return cursor.rowcount
		finally:
			self._cerrar(conexion, cursor)

 


