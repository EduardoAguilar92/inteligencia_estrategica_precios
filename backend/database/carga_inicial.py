import pandas as pd

try:
    from database.connection import get_connection
except ModuleNotFoundError:
    from connection import get_connection


def carga_inicial(cursor):
    # 1. Leer Excel
    df = pd.read_excel('backend/raw_data/listados.xlsx')
    print("📊 Excel cargado correctamente:")
    print(df.head())

    try:
        # 3. Insertar datos
        for _, row in df.iterrows():
            cursor.execute("""
                INSERT INTO cat_listados (
                    competencia,
                    mundo,
                    departamento,
                    clase,
                    categoria,
                    url_listado,
                    vigente
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (
                row['competencia'],
                row['mundo'],
                row['departamento'],
                row['clase'],
                row['categoria'],
                row['url_listado'],
                row['vigente']
            ))

        print("Datos insertados correctamente")

    except Exception as e:
        print(f"Error durante la carga inicial: {e}")


if __name__ == "__main__":
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        carga_inicial(cursor)
        conn.commit()
    except Exception as e:
        print(f"Error durante la carga inicial: {e}")
        if conn:
            conn.rollback()
    finally:
        if conn:
            conn.close()