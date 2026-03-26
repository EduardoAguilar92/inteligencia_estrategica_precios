try:
    from database.connection import get_connection
    from database.schemas.cat_listados import crear_cat_listados
    from database.schemas.contenidos import crear_tabla_contenidos
    from database.schemas.cat_modelos import crear_cat_modelos
    from database.schemas.productos import crear_tabla_productos
    from database.carga_inicial import carga_inicial
except ModuleNotFoundError:
    from connection import get_connection
    from schemas.cat_listados import crear_cat_listados
    from schemas.contenidos import crear_tabla_contenidos
    from schemas.cat_modelos import crear_cat_modelos
    from schemas.productos import crear_tabla_productos
    from carga_inicial import carga_inicial


def inicializar_base_de_datos():
    """Crea las tablas necesarias en la base de datos"""
    conn = None
    try:
        conn = get_connection()

        with conn.cursor() as cursor:
            crear_cat_listados(cursor)
            crear_tabla_contenidos(cursor)
            crear_cat_modelos(cursor)
            crear_tabla_productos(cursor)
            carga_inicial(cursor)
            # Agrega aquí la creación de otras tablas necesarias

            # Crear relaciones entre tablas si es necesario (FOREIGN KEY, etc.)

        conn.commit()
        print("✅ Base de datos inicializada correctamente")

    except Exception as e:
        print(f"❌ Error al inicializar la base de datos: {e}")
        if conn:
            conn.rollback()

    finally:
        if conn:
            conn.close()


if __name__ == "__main__":
    inicializar_base_de_datos()