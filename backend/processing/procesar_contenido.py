import sys
import psycopg2
import argparse
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import time
from typing import Any
from bs4 import BeautifulSoup

from selenium.webdriver.common.by import By

from database.connection import get_connection
from database.queries import obtener_contenidos, insertar_producto_catalogo


class ContentProcessor:
    def __init__(self, contenido_id: int, contenido: str, pagina: int):
        self.contenido_id = contenido_id
        self.contenido = contenido
        self.pagina = pagina
        self.conn = None

    def _init_db_connection(self):
        self.conn = get_connection()

    def procesar(self) -> Any:
        # Inicializar conexión a la base de datos
        self._init_db_connection()
        if self.conn is None:
            print("❌ No se pudo establecer conexión a la base de datos")
            return

        try:
            # Aquí puedes agregar la lógica para procesar el contenido HTML
            if self.contenido.startswith('<ul class="m-product__listingPlp">'):
                print("Procesando contenido de Liverpool...")
                soup = BeautifulSoup(self.contenido, 'html.parser')
                tarjetas = soup.select("ul.m-product__listingPlp li.m-product__card")
                if not tarjetas:
                    tarjetas = soup.select("ul.m-product__listingPlp li")

                for tarjeta in tarjetas:
                    try:
                        enlace = tarjeta.select_one("a[target='_self']")
                        articulo = tarjeta.select_one("article.ipod-d-block")
                        imagen = tarjeta.select_one("img")
                        marca = ''
                        modelo = ''
                        patrocinado = False
                        producto_propio = False
                        activo = True

                        descripcion = ""
                        if articulo:
                            descripcion = articulo.get_text(" ", strip=True).replace("\n", " ").strip()
                            descripcion = " ".join(descripcion.split())

                        # Extraer valores escalares de los Tags
                        url_producto = 'https://www.liverpool.com.mx'+enlace.get("href") if enlace else None
                        url_imagen = imagen.get("src") if imagen else None
                        
                        insertar_producto_catalogo(self.conn,
                                                    self.contenido_id,
                                                    url_producto,
                                                    descripcion,
                                                    url_imagen,
                                                    marca,
                                                    modelo,
                                                    patrocinado,
                                                    producto_propio,
                                                    activo
                                                    )

                    except Exception as e:
                        print(f"⚠️ Error procesando tarjeta Liverpool: {e}")

            elif self.contenido.startswith('<div id="productContainer"'):
                print("Procesando contenido de Coppel...")
                soup = BeautifulSoup(self.contenido, 'html.parser')
                tarjetas = soup.select("div.chakra-card.css-eak602")

                for tarjeta in tarjetas:
                    try:
                        enlace = tarjeta.select_one("a")
                        url_producto = 'https://www.coppel.com'+enlace.get("href") if enlace else None

                        nombre = tarjeta.select_one("h3.chakra-text.css-12u5nxr")
                        descripcion = nombre.get_text(" ", strip=True).replace("\n", " ").strip() if nombre else ""
                        descripcion = " ".join(descripcion.split())

                        imagen = tarjeta.select_one("img")
                        url_imagen = imagen.get("src") or imagen.get("data-src") if imagen else None

                        marca = ''
                        modelo = ''
                        patrocinado = False
                        producto_propio = False
                        activo = True
                        
                        insertar_producto_catalogo(self.conn,
                                                    self.contenido_id,
                                                    url_producto,
                                                    descripcion,
                                                    url_imagen,
                                                    marca,
                                                    modelo,
                                                    patrocinado,
                                                    producto_propio,
                                                    activo
                                                    )

                    except Exception as e:
                        print(f"⚠️ Error procesando tarjeta Coppel: {e}")


            elif self.contenido.startswith('<div class="boxProductosCategory cardGrid">'):
                print("Procesando contenido de Sears...")
                soup = BeautifulSoup(self.contenido, 'html.parser')
                tarjetas = soup.select("article[class*='CardProduct_cardProduct']")

                for tarjeta in tarjetas:
                    try:
                        enlace = tarjeta.select_one("a")
                        url_producto = 'https://www.sears.com.mx'+enlace.get("href") if enlace else None

                        titulo = tarjeta.select_one("h3[class*='CardProduct_h4']")
                        descripcion = titulo.get_text(" ", strip=True).replace("\n", " ").strip() if titulo else ""
                        descripcion = " ".join(descripcion.split())

                        imagen = tarjeta.select_one("picture img")
                        url_imagen = (imagen.get("src") if imagen else None) or (imagen.get("data-src") if imagen else None)

                        marca = ''
                        modelo = ''
                        patrocinado = False
                        producto_propio = False
                        activo = True

                        insertar_producto_catalogo(self.conn,
                                                    self.contenido_id,
                                                    url_producto,
                                                    descripcion,
                                                    url_imagen,
                                                    marca,
                                                    modelo,
                                                    patrocinado,
                                                    producto_propio,
                                                    activo
                                                    )

                    except Exception as e:
                        print(f"⚠️ Error procesando tarjeta Sears: {e}")
        finally:
            if self.conn:
                self.conn.close()

def parsear_argumentos() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Procesar contenidos HTML de listados de productos")
    parser.add_argument(
        "-d",
        "--date",
        required=False,
        help="Fecha de los contenidos a procesar (formato: YYYY-MM-DD). Si no se especifica, se procesan los contenidos del día actual.",
    )

    args = parser.parse_args()

    return args

def procesar_catalogo(fecha: str = None):
    contenidos = obtener_contenidos(fecha)
    for i, contenido in enumerate(contenidos):
        print(f"Procesando contenido {i+1}/{len(contenidos)} (ID: {contenido[0]})")
        ContentProcessor(contenido[0], contenido[2], contenido[3]).procesar()  # Asumiendo que el contenido HTML está en la tercera columna
        
    return None


if __name__ == "__main__":
    print("Iniciando procesamiento de contenidos...")
    args = parsear_argumentos()
    print("Ejecutando el script principal")
    if args.date:
        print(f"Procesando contenidos para la fecha: {args.date}")
        procesar_catalogo(args.date)
    else:
        procesar_catalogo()