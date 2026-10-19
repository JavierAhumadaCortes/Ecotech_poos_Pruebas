# persistencia/crear_bd.py
from persistencia.conexion import (abrir_conexion,obtener_motor )

def crear_tablas():
    conexion = abrir_conexion()
    cursor = conexion.cursor()

    sqlite = obtener_motor() == "sqlite"
    tipo_id = "INTEGER PRIMARY KEY AUTOINCREMENT" if sqlite else "INT PRIMARY KEY AUTO_INCREMENT"
    tipo_texto = "TEXT" if sqlite else "VARCHAR(255)"

    tablas = [
        f'''
            CREATE TABLE IF NOT EXISTS departamento (
                id {tipo_id},
                nombre {tipo_texto} NOT NULL,
                gerente_id INTEGER,
                UNIQUE (gerente_id),
                FOREIGN KEY (gerente_id) REFERENCES empleado(id)
            )
        ''',
        f'''
            CREATE TABLE IF NOT EXISTS empleado (
                id {tipo_id},
                nombre {tipo_texto} NOT NULL,
                correo {tipo_texto} NOT NULL,
                departamento_id INTEGER,
                UNIQUE (id, departamento_id),
                FOREIGN KEY (departamento_id) REFERENCES departamento(id)
            )
        ''',
        f'''
            CREATE TABLE IF NOT EXISTS proyecto (
                id {tipo_id},
                nombre {tipo_texto} NOT NULL
            )
        ''',
        f'''
            CREATE TABLE IF NOT EXISTS usuario (
                id {tipo_id},
                empleado_id INTEGER NOT NULL UNIQUE,
                nombre_usuario {tipo_texto} NOT NULL UNIQUE,
                password_hash {tipo_texto} NOT NULL,
                FOREIGN KEY (empleado_id) REFERENCES empleado(id)
            )
        ''',
        f'''
            CREATE TABLE IF NOT EXISTS registro_tiempo (
                id {tipo_id},
                empleado_id INTEGER NOT NULL,
                proyecto_id INTEGER NOT NULL,
                horas DECIMAL(8, 2) NOT NULL,
                observacion {tipo_texto},
                incidente {tipo_texto},
                fecha DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (empleado_id, proyecto_id)
                    REFERENCES empleado_proyecto(empleado_id, proyecto_id)
            )
        '''
    ]

    try:
        for sql in tablas:
            cursor.execute(sql)
        conexion.commit()
    except Exception:
        conexion.rollback()
        raise
    finally:
        conexion.close()

if __name__ == "__main__":
    crear_tablas()
    print("Base de datos preparada correctamente.")


# actualizame esta consulta para solucionar este problematica, 
# un empleado pertenece a un departamento  y un departamento es pertenecido por muchos empleados, 
# un empleado puede ser gerente de un departamento pero un 
# departamento solo puede tener un solo gerente, un 