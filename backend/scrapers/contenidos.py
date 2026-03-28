import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import time
from typing import Any

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


from database.queries import insertar_productos

class ListadosScraper:
    def __init__(self,listado_id: int = None, url_listado: str = None, headless: bool = True, timeout: int = 10):
        self.listado_id = listado_id
        self.url_listado = url_listado
        self.timeout = timeout
        self.contenido = None
        self.headless = headless

    def _configurar_driver(self) -> webdriver.Chrome:
        """Configura y retorna la instancia del webdriver de Chrome."""
        opciones = Options()
        if self.headless:
            opciones.add_argument("--headless=new") # Nueva sintaxis recomendada para headless
        
        # Opciones recomendadas para evitar bloqueos y errores de memoria
        opciones.add_argument("--disable-gpu")
        opciones.add_argument("--no-sandbox")
        opciones.add_argument("--disable-dev-shm-usage")
        opciones.add_argument("--disable-blink-features=AutomationControlled")
        opciones.add_experimental_option("excludeSwitches", ["enable-automation"])
        opciones.add_experimental_option("useAutomationExtension", False)
                
        return webdriver.Chrome(options=opciones)
    
    def scrape_listado_liverpool(self):
        try:
            # Inicializamos el driver al crear la instancia
            self.driver = self._configurar_driver()
            self.driver.maximize_window()
            self.driver.get(self.url_listado+'?gfeed=true')
            print(f"🔍 Cargando página: {self.url_listado+'?gfeed=true'}")
            self.driver.get(self.url_listado+'?gfeed=true')
            pagina_actual = 1
            url_anterior = ""
        
            while True:
                print(f"📄 Scrapeando página {pagina_actual}...")
                # ── ESPERA A QUE CARGUEN LOS PRODUCTOS ────────────────────────────────────
                try:
                    WebDriverWait(self.driver, 15).until(
                        EC.presence_of_element_located((By.CLASS_NAME, "o-listing__products"))
                    )
                except:
                    print("❌ No cargaron los productos")
                    break
                # ── VERIFICA SI LA URL CAMBIÓ (DETECTA ÚLTIMA PÁGINA) ─────────────────────
                url_actual = self.driver.current_url
                if url_actual == url_anterior:
                    print(f"✅ Última página alcanzada: página {pagina_actual-1}")
                    break
                url_anterior = url_actual
                time.sleep(5)  # Espera adicional para asegurar que los productos estén completamente cargados
                contenedor = WebDriverWait(self.driver, 15).until(
                                EC.presence_of_element_located(
                                    (By.XPATH, "//ul[@class='m-product__listingPlp']")
                                )
                            )
                html = contenedor.get_attribute("outerHTML")
                insertar_productos(self.listado_id, html, pagina_actual)
                # print(html[:500])  # Imprime los primeros 500 caracteres del HTML del contenedor para verificación
                # ── INTENTA PASAR A LA SIGUIENTE PÁGINA ───────────────────────────────────
                try:
                    boton_siguiente = self.driver.find_element(
                        By.XPATH, "//nav[@aria-label='Pagination']//a[.//i[@class='icon-arrow_right']]"
                    )
                    self.driver.execute_script("arguments[0].click();", boton_siguiente)
                    pagina_actual += 1
                    time.sleep(3)
                except:
                    print(f"✅ Última página alcanzada: página {pagina_actual}")
                    break
        except TimeoutException:
            # print(f"⏰ Error: La página tardó demasiado en cargar después de {self.wait_seconds} segundos.")
            return []
        except NoSuchElementException as e:
            print(f"❌ Error: No se encontró el elemento esperado. Detalles: {e}")
            return []
        except Exception as e:
            print(f"❌ Ocurrió un error inesperado: {e}")
            return []
        finally:
            self.driver.quit()

    def scrape_listado_coppel(self):
        try:
            # Inicializamos el driver al crear la instancia
            self.driver = self._configurar_driver()
            self.driver.maximize_window()
            self.driver.get(self.url_listado+'?gfeed=true')
            print(f"🔍 Cargando página: {self.url_listado+'?gfeed=true'}")
            self.driver.get(self.url_listado+'?gfeed=true')
            pagina_actual = 1
            url_anterior = ""
        
            while True:
                print(f"📄 Scrapeando página {pagina_actual}...")
                # ── ESPERA A QUE CARGUEN LOS PRODUCTOS ────────────────────────────────────
                try:
                    WebDriverWait(self.driver, 15).until(
                        EC.presence_of_element_located((By.ID, "productContainer"))
                    )
                except:
                    print("❌ No cargaron los productos")
                    break
                # ── VERIFICA SI LA URL CAMBIÓ (DETECTA ÚLTIMA PÁGINA) ─────────────────────
                url_actual = self.driver.current_url
                if url_actual == url_anterior:
                    print(f"✅ Última página alcanzada: página {pagina_actual-1}")
                    break
                url_anterior = url_actual
                time.sleep(5)  # Espera adicional para asegurar que los productos estén completamente cargados
                contenedor = WebDriverWait(self.driver, 15).until(
                                EC.presence_of_element_located(
                                    (By.ID, "productContainer")
                                )
                            )
                html = contenedor.get_attribute("outerHTML")
                insertar_productos(self.listado_id, html, pagina_actual)
                # print(html[:500])  # Imprime los primeros 500 caracteres del HTML del contenedor para verificación
                # ── INTENTA PASAR A LA SIGUIENTE PÁGINA ───────────────────────────────────
                try:
                    boton_siguiente = self.driver.find_element(
                        By.XPATH, "//a[@data-testid='pagination_right_arrow']"
                    )
                    self.driver.execute_script("arguments[0].click();", boton_siguiente)
                    pagina_actual += 1
                    time.sleep(3)
                except:
                    print(f"✅ Última página alcanzada: página {pagina_actual}")
                    break
        except TimeoutException:
            # print(f"⏰ Error: La página tardó demasiado en cargar después de {self.wait_seconds} segundos.")
            return []
        except NoSuchElementException as e:
            print(f"❌ Error: No se encontró el elemento esperado. Detalles: {e}")
            return []
        except Exception as e:
            print(f"❌ Ocurrió un error inesperado: {e}")
            return []
        finally:
            self.driver.quit()

    def scrape_listado_sears(self):
        # Implementa la lógica de scraping para Sears aquí, siguiendo una estructura similar a los métodos anteriores
        try:
            # Inicializamos el driver al crear la instancia
            self.driver = self._configurar_driver()
            self.driver.maximize_window()
            self.driver.get(self.url_listado+'?gfeed=true')
            print(f"🔍 Cargando página: {self.url_listado+'?gfeed=true'}")
            self.driver.get(self.url_listado+'?gfeed=true')
            pagina_actual = 1
            url_anterior = ""
        
            while True:
                contenedor = None
                print(f"📄 Scrapeando página {pagina_actual}...")
                # ── ESPERA A QUE CARGUEN LOS PRODUCTOS ────────────────────────────────────
                try:
                    WebDriverWait(self.driver, 15).until(
                        EC.presence_of_element_located((By.CLASS_NAME, "boxGeneralProductosResultados"))
                    )
                except:
                    print("❌ No cargaron los productos")
                    break
                # ── VERIFICA SI LA URL CAMBIÓ (DETECTA ÚLTIMA PÁGINA) ─────────────────────
                url_actual = self.driver.current_url
                if url_actual == url_anterior:
                    print(f"✅ Última página alcanzada: página {pagina_actual-1}")
                    break
                url_anterior = url_actual
                time.sleep(5)  # Espera adicional para asegurar que los productos estén completamente cargados
                contenedor = WebDriverWait(self.driver, 15).until(
                                EC.presence_of_element_located(
                                    (By.CSS_SELECTOR, "div.boxProductosCategory.cardGrid")
                                )
                            )
                html = contenedor.get_attribute("outerHTML")
                insertar_productos(self.listado_id, html, pagina_actual)
                # print(html[:500])  # Imprime los primeros 500 caracteres del HTML del contenedor para verificación
                # ── INTENTA PASAR A LA SIGUIENTE PÁGINA ───────────────────────────────────
                try:
                    boton_siguiente = self.driver.find_element(
                        By.XPATH, "//a[.//span[text()='Siguiente']]"
                    )
                    self.driver.execute_script("arguments[0].click();", boton_siguiente)
                    pagina_actual += 1
                    time.sleep(3)
                except:
                    print(f"✅ Última página alcanzada: página {pagina_actual}")
                    break
        except TimeoutException:
            # print(f"⏰ Error: La página tardó demasiado en cargar después de {self.wait_seconds} segundos.")
            return []
        except NoSuchElementException as e:
            print(f"❌ Error: No se encontró el elemento esperado. Detalles: {e}")
            return []
        except Exception as e:
            print(f"❌ Ocurrió un error inesperado: {e}")
            return []
        finally:
            self.driver.quit()


if __name__ == "__main__":
    scraper = ListadosScraper(headless=False, listado_id=1,url_listado="https://www.liverpool.com.mx/tienda/refrigeradores/catst53841452")
    scraper.scrape_listado_liverpool()
