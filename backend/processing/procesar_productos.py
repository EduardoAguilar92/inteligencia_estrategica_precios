import sys
import psycopg2
import argparse
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import time
from typing import Any
from bs4 import BeautifulSoup, NavigableString

from selenium.webdriver.common.by import By

from database.connection import get_connection
from database.queries import obtener_contenidos, buscar_modelo_id, insertar_producto_precio, marcar_contenido_procesado


class ProductProcessor:
    def __init__(self, contenido_id: int, contenido_html: str, pagina: int):
        self.contenido_id = contenido_id
        self.contenido_html = contenido_html
        self.pagina = pagina

    def _init_db_connection(self):
        self.conn = get_connection()

    def _extraer_precio_liverpool(self, precio_elemento) -> float | None:
        if not precio_elemento:
            return None

        precio_regular_entero = "".join(
            nodo.strip()
            for nodo in precio_elemento.contents
            if isinstance(nodo, NavigableString)
        ).strip()

        centavos_tag = precio_elemento.find("sup")
        centavos = centavos_tag.get_text(strip=True) if centavos_tag else "00"

        precio_regular = f"{precio_regular_entero}.{centavos}"
        precio_regular = (
            precio_regular
            .replace("$", "")
            .replace(",", "")
            .replace(" ", "")
            .strip()
        )

        try:
            return float(precio_regular)
        except (ValueError, TypeError):
            precio_texto_completo = (
                precio_elemento.get_text("", strip=True)
                .replace("$", "")
                .replace(",", "")
                .replace(" ", "")
                .strip()
            )
            try:
                return float(precio_texto_completo)
            except (ValueError, TypeError):
                return None

    def _extraer_precio_coppel(self, precio_elemento) -> float | None:
        if not precio_elemento:
            return None

        precio_texto = precio_elemento.text.strip()
        precio_texto = precio_texto.replace("$", "").replace(",", "").strip()
        try:
            return float(precio_texto)
        except (ValueError, TypeError):
            return None

    def _extraer_precio_sears(self, precio_elemento) -> float | None:
        if not precio_elemento:
            return None

        precio_texto = precio_elemento.text.strip()
        precio_texto = precio_texto.replace("$", "").replace(",", "").replace("MXN", "").strip()
        try:
            return float(precio_texto)
        except (ValueError, TypeError):
            return None

    def procesar(self) -> Any:
        # Aquí puedes agregar la lógica para procesar el producto individualmente
        self._init_db_connection()
        if self.conn is None:
            print("❌ No se pudo establecer conexión a la base de datos")
            return
        
        try:
            # Aquí puedes agregar la lógica para procesar el contenido HTML
            if self.contenido_html.startswith('<ul class="m-product__listingPlp">'):
                print("Procesando contenido de Liverpool...")
                soup = BeautifulSoup(self.contenido_html, 'html.parser')
                tarjetas = soup.select("ul.m-product__listingPlp li.m-product__card")
                if not tarjetas:
                    tarjetas = soup.select("ul.m-product__listingPlp li")

                for tarjeta in tarjetas:
                    try:
                        enlace = tarjeta.select_one("a[target='_self']")
                        articulo = tarjeta.select_one("article.ipod-d-block")
                        precio_actual = tarjeta.select_one("p.a-card-discount")
                        precio_anterior = tarjeta.select_one("p.a-card-price")

                        descripcion = ""
                        if articulo:
                            descripcion = articulo.get_text(" ", strip=True).replace("\n", " ").strip()

                        url_producto = 'https://www.liverpool.com.mx' + enlace.get("href") if enlace else None
                        precio_actual_float = self._extraer_precio_liverpool(precio_actual)
                        precio_anterior_float = self._extraer_precio_liverpool(precio_anterior)

                        print(
                            f"Descripción del producto: {descripcion} | "
                            f"Precio actual: {precio_actual_float} | "
                            f"Precio anterior: {precio_anterior_float}"
                        )

                        modelo_id = buscar_modelo_id(self.conn, descripcion, url_producto)
                        if modelo_id and precio_actual_float is not None:
                            insertar_producto_precio(
                                self.conn,
                                self.contenido_id,
                                modelo_id,
                                precio_actual_float,
                                precio_anterior_float,
                            )

                    except Exception as e:
                        print(f"⚠️ Error procesando tarjeta Liverpool: {e}")

                marcar_contenido_procesado(self.contenido_id)
            
            elif self.contenido_html.startswith('<div id="productContainer"'):
                print("Procesando contenido de Coppel...")
                soup = BeautifulSoup(self.contenido_html, 'html.parser')
                tarjetas = soup.select("div.chakra-card.css-eak602")

                for tarjeta in tarjetas:
                    try:
                        enlace = tarjeta.select_one("a")
                        articulo = tarjeta.select_one("h3.chakra-text.css-12u5nxr")
                        precio_actual = tarjeta.select_one("span.chakra-text.css-44wgta")
                        precio_anterior = tarjeta.select_one("span.chakra-text.css-uwrhh6")

                        descripcion = ""
                        if articulo:
                            descripcion = articulo.get_text(" ", strip=True).replace("\n", " ").strip()

                        url_producto = 'https://www.coppel.com'+enlace.get("href") if enlace else None
                        precio_actual_float = self._extraer_precio_coppel(precio_actual)
                        precio_anterior_float = self._extraer_precio_coppel(precio_anterior)

                        print(
                            f"Descripción del producto: {descripcion} | "
                            f"Precio actual: {precio_actual_float} | "
                            f"Precio anterior: {precio_anterior_float}"
                        )

                        modelo_id = buscar_modelo_id(self.conn, descripcion, url_producto)
                        if modelo_id and precio_actual_float is not None:
                            insertar_producto_precio(
                                self.conn,
                                self.contenido_id,
                                modelo_id,
                                precio_actual_float,
                                precio_anterior_float,
                            )

                    except Exception as e:
                        print(f"⚠️ Error procesando tarjeta Coppel: {e}")

                marcar_contenido_procesado(self.contenido_id)

            elif self.contenido_html.startswith('<div class="boxProductosCategory cardGrid">'):
                print("Procesando contenido de Sears...")
                soup = BeautifulSoup(self.contenido_html, 'html.parser')
                tarjetas = soup.select("article[class*='CardProduct_cardProduct']")

                for tarjeta in tarjetas:
                    try:
                        enlace = tarjeta.select_one("aa")
                        articulo = tarjeta.select_one("h3[class*='CardProduct_h4']")
                        precio_actual = tarjeta.select_one("p[class*='precio1']")
                        precio_anterior = tarjeta.select_one("span[class*='textUnderline']")

                        descripcion = ""
                        if articulo:
                            descripcion = articulo.get_text(" ", strip=True).replace("\n", " ").strip()

                        url_producto = 'https://www.sears.com.mx' + enlace.get("href") if enlace else None
                        precio_actual_float = self._extraer_precio_sears(precio_actual)
                        precio_anterior_float = self._extraer_precio_sears(precio_anterior)

                        print(
                            f"Descripción del producto: {descripcion} | "
                            f"Precio actual: {precio_actual_float} | "
                            f"Precio anterior: {precio_anterior_float}"
                        )

                        modelo_id = buscar_modelo_id(self.conn, descripcion, url_producto)
                        if modelo_id and precio_actual_float is not None:
                            insertar_producto_precio(
                                self.conn,
                                self.contenido_id,
                                modelo_id,
                                precio_actual_float,
                                precio_anterior_float,
                            )

                    except Exception as e:
                        print(f"⚠️ Error procesando tarjeta Sears: {e}")

                marcar_contenido_procesado(self.contenido_id)
        finally:
            if self.conn:
                self.conn.close()

        # print(f"Procesando producto {self.contenido_id} del contenido {self.contenido_id} con URL: {self.url_producto}")
        # Ejemplo: podrías hacer un scraping adicional para obtener más detalles del producto

def procesar_productos(fecha: str = None):
    contenidos = obtener_contenidos(fecha)
    for i, contenido in enumerate(contenidos):
        print(f"Procesando contenido {i+1}/{len(contenidos)} (ID: {contenido[0]})")
        print(f"Página: {contenido[3]}")
        ProductProcessor(contenido_id=contenido[0], contenido_html=contenido[2], pagina=contenido[3]).procesar()

    return None

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


if __name__ == "__main__":
    print("Iniciando procesamiento de productos...")
    args = parsear_argumentos()
    print("Ejecutando el script principal")
    if args.date:
        print(f"Procesando contenidos para la fecha: {args.date}")
        procesar_productos(args.date)
    else:
        procesar_productos()
