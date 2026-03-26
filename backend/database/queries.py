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