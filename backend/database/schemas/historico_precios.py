def crear_tabla_historico_precios(cursor):
    """Crea la tabla de precios historicos si no existe"""
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS historico_precios (
            id                SERIAL PRIMARY KEY,
            contenido_id      INTEGER NOT NULL,
            cat_modelo_id     INTEGER NOT NULL,
            precio_actual     NUMERIC(10, 2) NOT NULL,
            precio_anterior   NUMERIC(10, 2),
            fecha             DATE NOT NULL DEFAULT CURRENT_DATE,  
            created_at        TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            modified_at         TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                   
            CONSTRAINT fk_contenido_id_historico_precios
                FOREIGN KEY (contenido_id)
                REFERENCES contenidos(id)
                ON DELETE NO ACTION
                ON UPDATE NO ACTION,
                   
            CONSTRAINT unique_contenido_fecha
                UNIQUE (contenido_id, cat_modelo_id, fecha)
        );
     """)
    print("✅ Tabla historico_precios verificada.")