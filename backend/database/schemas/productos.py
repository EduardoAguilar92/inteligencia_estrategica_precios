def crear_tabla_productos(cursor):
    """Crea la tabla de productos si no existe"""
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS productos (
            id              SERIAL PRIMARY KEY,
            contenido_id    INTEGER,
            descripcion_id  INTEGER,
            precio_actual   NUMERIC(12,2),
            precio_anterior NUMERIC(12,2) NOT NULL,
            patrocinado     BOOLEAN,
            url_producto    TEXT,
            url_imagen      TEXT,
            created_at      TIMESTAMP,

            CONSTRAINT fk_contenidos_id_productos
                FOREIGN KEY (contenido_id)
                REFERENCES contenidos(id)
                ON DELETE NO ACTION
                ON UPDATE NO ACTION,

            CONSTRAINT fk_cat_modelos_id_productos
                FOREIGN KEY (descripcion_id)
                REFERENCES cat_modelos(id)
                ON DELETE NO ACTION
                ON UPDATE NO ACTION
        );
     """)
    print("✅ Tabla productos verificada.")