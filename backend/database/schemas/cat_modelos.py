def crear_cat_modelos(cursor):
    """Crea la tabla catálogo de modelos si no existe"""
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS cat_modelos (
            id              SERIAL PRIMARY KEY,
            contenido_id    INTEGER NOT NULL,
            url_producto    TEXT NOT NULL UNIQUE,
            descripcion     VARCHAR(255) NOT NULL,
            marca           VARCHAR(100),
            modelo          VARCHAR(100),

            CONSTRAINT fk_contenidos_id_cat_modelos
                FOREIGN KEY (contenido_id)
                REFERENCES contenidos(id)
                ON DELETE NO ACTION
                ON UPDATE NO ACTION
);
     """)
    print("✅ Catálogo de modelos verificado.")