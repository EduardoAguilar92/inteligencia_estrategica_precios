def crear_tabla_contenidos(cursor):
    """Crea la tabla de contenidos si no existe"""
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS contenidos (
            id              SERIAL PRIMARY KEY,
            listado_id      INTEGER NOT NULL,
            contenido       TEXT NOT NULL,
            pagina          INTEGER NOT NULL,
            fecha           DATE NOT NULL DEFAULT CURRENT_DATE,  
            created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            modified_at     TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                   
            CONSTRAINT fk_cat_listados_id_contenidos
                FOREIGN KEY (listado_id)
                REFERENCES cat_listados(id)
                ON DELETE NO ACTION
                ON UPDATE NO ACTION,
                   
            CONSTRAINT unique_listado_pagina_fecha
                UNIQUE (listado_id, pagina, fecha)
        );
     """)
    print("✅ Tabla contenidos verificada.")