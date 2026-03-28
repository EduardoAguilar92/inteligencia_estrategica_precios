def crear_cat_modelos(cursor):
    """Crea la tabla catálogo de modelos si no existe"""
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS cat_modelos (
            id                 SERIAL PRIMARY KEY,
            contenido_id       INTEGER NOT NULL,
            url_producto       TEXT NOT NULL,
            descripcion        VARCHAR(255) NOT NULL,
            url_imagen         TEXT,
            marca              VARCHAR(100),
            modelo             VARCHAR(100),
            patrocinado        BOOLEAN DEFAULT FALSE,
            producto_propio    BOOLEAN DEFAULT FALSE,
            activo             BOOLEAN DEFAULT TRUE,
            created_at         TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            modified_at        TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

            CONSTRAINT fk_contenidos_id_cat_modelos
                FOREIGN KEY (contenido_id)
                REFERENCES contenidos(id)
                ON DELETE NO ACTION
                ON UPDATE NO ACTION
);
     """)

    cursor.execute("""
        ALTER TABLE cat_modelos
        DROP CONSTRAINT IF EXISTS cat_modelos_url_producto_key;
    """)

    cursor.execute("""
        DO $$
        BEGIN
            IF NOT EXISTS (
                SELECT 1
                FROM pg_constraint
                WHERE conname = 'unique_url_producto_descripcion'
            ) THEN
                ALTER TABLE cat_modelos
                ADD CONSTRAINT unique_url_producto_descripcion
                UNIQUE (url_producto, descripcion);
            END IF;
        END $$;
    """)

    print("✅ Catálogo de modelos verificado.")