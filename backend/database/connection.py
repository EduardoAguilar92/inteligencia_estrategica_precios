import psycopg2
import os
from dotenv import load_dotenv

try:
    load_dotenv(encoding="utf-8")
except UnicodeDecodeError:
    load_dotenv(encoding="latin-1")

def get_connection():
    """Retorna una conexión a la base de datos PostgreSQL"""
    print("🔌 Conectando a la base de datos...")
    print(f"Host: {os.getenv('DB_HOST')}, Port: {os.getenv('DB_PORT')}, Database: {os.getenv('DB_NAME')}, User: {os.getenv('DB_USER')}")
    return psycopg2.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD")
    )

if __name__ == "__main__":
    try:
        conn = get_connection()
        print("✅ Conexión exitosa a la base de datos.")
        conn.close()
    except Exception as e:
        print(f"❌ Error al conectar a la base de datos: {e}")