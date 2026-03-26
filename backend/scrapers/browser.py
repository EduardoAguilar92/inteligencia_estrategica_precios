from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def crear_navegador(headless: bool = True) -> webdriver.Chrome:
    """
    Configura y retorna una instancia del navegador Chrome lista para usar.

    Args:
        headless: Si True corre sin ventana visual (producción).
                  Si False abre el navegador (desarrollo/debug).
    """
    opciones = Options()

    if headless:
        opciones.add_argument("--headless=new")

    # ── ANTI-DETECCIÓN ─────────────────────────────────────────────────────────
    opciones.add_argument("--disable-blink-features=AutomationControlled")
    opciones.add_experimental_option("excludeSwitches", ["enable-automation"])
    opciones.add_experimental_option("useAutomationExtension", False)

    # ── ESTABILIDAD Y RENDIMIENTO ──────────────────────────────────────────────
    opciones.add_argument("--disable-gpu")
    opciones.add_argument("--no-sandbox")
    opciones.add_argument("--disable-dev-shm-usage")

    return webdriver.Chrome(options=opciones)