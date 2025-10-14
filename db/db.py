import psycopg

DB_CONFIG = {
    "dbname": "inventario_db",
    "user": "postgres",
    "password": "cuvl1234",
    "host": "localhost",
    "port": "5432"
}


def get_connection():
    try:
        return psycopg.connect(**DB_CONFIG)
    except Exception as e:
        print(f"[ERROR DB] {e}")
        return None
    

conexion = get_connection()