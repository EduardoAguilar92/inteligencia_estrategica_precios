import psycopg2

try:
    from database.connection import get_connection
except ModuleNotFoundError:
    from connection import get_connection


def insertar_productos(listado_id: int, contenido: str, pagina: int):
    """Inserta los productos extraídos en la base de datos."""
    conn = get_connection()
    cursor = None
    try:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO contenidos (
                listado_id,
                contenido,
                pagina
            )
            VALUES (%s, %s, %s)
        """, (
            listado_id,
            contenido,
            pagina
        ))
        conn.commit()
    except psycopg2.errors.UniqueViolation:
        print(f"Producto de la página {pagina} del listado {listado_id} ya existe. Omitiendo inserción.")
        pass  # El producto ya existe, no hacemos nada
    except Exception as e:
        print(f"Error al insertar productos: {e}")
    finally:
        if cursor:
            cursor.close()
        conn.close()


def obtener_contenidos(fecha: str):
    conn = get_connection()
    cursor = None
    try:
        cursor = conn.cursor()
        if fecha:
            cursor.execute("SELECT * FROM contenidos WHERE fecha = %s and procesado = FALSE;", (fecha,))
        else:
            cursor.execute("SELECT * FROM contenidos WHERE fecha = CURRENT_DATE and procesado = FALSE;")
        contenidos = cursor.fetchall()
        return contenidos
    except Exception as e:
        print(f"Error al obtener contenidos: {e}")
        return []
    finally:
        if cursor:
            cursor.close()
        conn.close()


def insertar_producto_catalogo(conn, 
                               contenido_id, 
                               url_producto, 
                               descripcion, 
                               url_imagen, 
                               marca, 
                               modelo, 
                               patrocinado, 
                               producto_propio, 
                               activo):
    """Ejemplo de función para insertar un producto en la base de datos."""
    cursor = None
    try:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO cat_modelos (
                contenido_id,
                url_producto,
                descripcion,
                url_imagen,
                marca,
                modelo,
                patrocinado,
                producto_propio,
                activo
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (url_producto, descripcion) DO NOTHING
        """, (
            contenido_id,  # contenido_id
            url_producto,  # enlace
            descripcion,  # descripcion
            url_imagen,  # imagen
            marca,  # marca
            modelo,  # modelo
            patrocinado,  # patrocinado
            producto_propio,  # producto_propio
            activo   # activo
        ))
        conn.commit()
    except Exception as e:
        print(f"Error al insertar producto: {e}")
        if conn:
            conn.rollback()
    finally:
        if cursor:
            cursor.close()

def buscar_modelo_id(conn, descripcion: str, url_producto: str) -> int:
    """Ejemplo de función para buscar el modelo_id en la base de datos utilizando la descripción del producto."""
    cursor = None
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id FROM cat_modelos
            WHERE descripcion ILIKE %s
            LIMIT 1
        """, (f"%{descripcion}%",))
        result = cursor.fetchone()
        return result[0] if result else None
    except Exception as e:
        print(f"Error al buscar modelo_id: {e}")
        return None
    finally:
        if cursor:
            cursor.close()


def insertar_producto_precio(conn, contenido_id: int, modelo_id: int, precio_actual: str, precio_anterior: str):
    """Ejemplo de función para insertar el precio de un producto en la base de datos."""
    cursor = None
    try:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO historico_precios (
                contenido_id,
                cat_modelo_id,
                precio_actual,
                precio_anterior,
                fecha
            )
            VALUES (%s, %s, %s, %s, CURRENT_DATE)
        """, (
            contenido_id,
            modelo_id,
            precio_actual,
            precio_anterior
        ))
        conn.commit()
    except Exception as e:
        print(f"Error al insertar precio: {e}")
        if conn:
            conn.rollback()
    finally:
        if cursor:
            cursor.close()

def marcar_contenido_procesado(contenido_id: int):
    """Marca un contenido como procesado en la base de datos."""
    conn = get_connection()
    cursor = None
    try:
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE contenidos
            SET procesado = TRUE
            WHERE id = %s
        """, (contenido_id,))
        conn.commit()
    except Exception as e:
        print(f"Error al marcar contenido como procesado: {e}")
        if conn:
            conn.rollback()
    finally:
        if cursor:
            cursor.close()
        conn.close()