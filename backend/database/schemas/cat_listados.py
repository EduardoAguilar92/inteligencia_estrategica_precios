def crear_cat_listados(cursor):
    """Crea la tabla catálogo de listados si no existe"""
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS cat_listados (
            id              SERIAL PRIMARY KEY,
            competencia     VARCHAR(100) NOT NULL,
            mundo           VARCHAR(100) NOT NULL,
            departamento    VARCHAR(100) NOT NULL,
            clase           VARCHAR(100) NOT NULL,
            categoria       VARCHAR(100) NOT NULL,
            url_listado     VARCHAR(255) NOT NULL,
            vigente         BOOLEAN DEFAULT TRUE,
            created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            modified_at     TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
     """)
    print("✅ Catálogo de listados verificado.")