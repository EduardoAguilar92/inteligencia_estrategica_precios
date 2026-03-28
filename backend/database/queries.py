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


def obtener_contenidos():
    conn = get_connection()
    cursor = None
    try:
        cursor = conn.cursor()
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


def actualizar_flag_contenido_procesado(contenido_id: int):
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
        print(f"Error al actualizar flag de contenido procesado: {e}")
        if conn:
            conn.rollback()
    finally:
        if cursor:
            cursor.close()
        conn.close()