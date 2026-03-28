try:
    from database.connection import get_connection
    from database.init_db import inicializar_base_de_datos
except ModuleNotFoundError:
    from connection import get_connection
    from init_db import inicializar_base_de_datos

def resetear_base_de_datos():
    """Elimina todas las tablas y datos de la base de datos"""
    conn = None
    try:
        conn = get_connection()
        with conn.cursor() as cursor:
            cursor.execute("DROP TABLE IF EXISTS cat_listados CASCADE;")
            cursor.execute("DROP TABLE IF EXISTS contenidos CASCADE;")
            cursor.execute("DROP TABLE IF EXISTS cat_modelos CASCADE;")
            cursor.execute("DROP TABLE IF EXISTS historico_precios CASCADE;")
            # Agrega aquí cualquier otra tabla que necesites eliminar
        conn.commit()
        print("✅ Base de datos reseteada correctamente")

    except Exception as e:
        print(f"❌ Error al resetear la base de datos: {e}")
        if conn:
            conn.rollback()

    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    resetear_base_de_datos()
    inicializar_base_de_datos()