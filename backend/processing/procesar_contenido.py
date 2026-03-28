import sys
import psycopg2
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import time
from typing import Any
from bs4 import BeautifulSoup

from selenium.webdriver.common.by import By

from database.connection import get_connection
from database.queries import obtener_contenidos, insertar_producto_catalogo, actualizar_flag_contenido_procesado


class ContenidoProcessor:
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
                        # precio_actual = tarjeta.select_one("p.a-card-discount")
                        # precio_anterior = tarjeta.select_one("p.a-card-price")
                        marca = ''
                        modelo = ''
                        patrocinado = False
                        producto_propio = False
                        activo = True

                        descripcion = ""
                        if articulo:
                            descripcion = articulo.get_text(" ", strip=True).replace("\n", " ").strip()

                        # Extraer valores escalares de los Tags
                        url_producto = 'https://www.liverpool.com.mx'+enlace.get("href") if enlace else None
                        url_imagen = imagen.get("src") if imagen else None
                        # precio_actual_text = precio_actual.get_text(strip=True) if precio_actual else None
                        # precio_anterior_text = precio_anterior.get_text(strip=True) if precio_anterior else None
                        
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
                        descripcion = nombre.get_text(strip=True) if nombre else ""

                        imagen = tarjeta.select_one("img")
                        url_imagen = imagen.get("src") or imagen.get("data-src") if imagen else None

                        precio_regular_elemento = tarjeta.select_one("span.chakra-text.css-uwrhh6")
                        try:
                            precio_regular_float = float(precio_regular_elemento.get_text(strip=True).replace("$", "").replace(",", "")) if precio_regular_elemento else None
                        except (ValueError, AttributeError):
                            precio_regular_float = None

                        precio_descuento_elemento = tarjeta.select_one("span.chakra-text.css-44wgta")
                        try:
                            precio_descuento_float = float(precio_descuento_elemento.get_text(strip=True).replace("$", "").replace(",", "")) if precio_descuento_elemento else None
                        except (ValueError, AttributeError):
                            precio_descuento_float = None

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

                        precio_regular_elemento = tarjeta.select_one("span[class*='textUnderline']")
                        try:
                            precio_texto = precio_regular_elemento.get_text(strip=True).replace("$", "").replace(",", "").replace("MXN", "").strip() if precio_regular_elemento else ""
                            precio_regular_float = float(precio_texto) if precio_texto else None
                        except (ValueError, AttributeError):
                            precio_regular_float = None

                        precio_descuento_elemento = tarjeta.select_one("p[class*='precio1']")
                        try:
                            precio_texto = precio_descuento_elemento.get_text(strip=True).replace("$", "").replace(",", "").replace("MXN", "").strip() if precio_descuento_elemento else ""
                            precio_descuento_float = float(precio_texto) if precio_texto else None
                        except (ValueError, AttributeError):
                            precio_descuento_float = None

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
    

class ProductoProcessor:
    def __init__(self, contenido_id: int, descripcion_id: int, precio_actual: float, precio_anterior: float):
        self.producto_id = descripcion_id
        self.contenido_id = contenido_id
        self.precio_actual = precio_actual
        self.precio_anterior = precio_anterior

    def procesar(self) -> Any:
        # Aquí puedes agregar la lógica para procesar el producto individualmente
        print(f"Procesando producto {self.producto_id} del contenido {self.contenido_id} con URL: {self.url_producto}")
        # Ejemplo: podrías hacer un scraping adicional para obtener más detalles del producto

def procesar_contenidos():
    contenidos = obtener_contenidos()
    resultados = []
    for i, contenido in enumerate(contenidos):
        processor = ContenidoProcessor(contenido[0], contenido[2], contenido[3])  # Asumiendo que el contenido HTML está en la tercera columna
        resultado = processor.procesar()
        resultados.append(resultado)
    return resultados


if __name__ == "__main__":
    resultados = procesar_contenidos()
