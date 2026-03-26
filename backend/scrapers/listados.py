import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from database.connection import get_connection


def obtener_listados():
    """Obtiene los listados de la base de datos."""
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT id, competencia, url_listado FROM cat_listados;")
            return cursor.fetchall()
    except Exception as e:
        print(f"Error al obtener listados: {e}")
        return []
    finally:
        conn.close()

if __name__ == "__main__":
    listados = obtener_listados()
    print("Listados obtenidos:")
    for listado in listados:
        if listado[1] == 'Liverpool':  # Verifica que la URL no esté vacía
            print(f"ID: {listado[0]}, Competencia: {listado[1]}, URL: {listado[2]}")