import argparse
from datetime import datetime, timedelta
import time

from concurrent.futures import ThreadPoolExecutor, as_completed

from database.reset_db import resetear_base_de_datos
from database.init_db import inicializar_base_de_datos
from scrapers.listados import obtener_listados
from scrapers.contenidos import ListadosScraper
from processing.procesar_contenido import procesar_catalogo
from processing.procesar_productos import procesar_productos


def parsear_argumentos() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Scraper de listados de productos")
    parser.add_argument(
        "-r",
        "--reset",
        required=False,
        help="Indica si se debe resetear la base de datos antes de iniciar el proceso (elimina todas las tablas y datos)",
    )
    parser.add_argument(
        "-w",
        "--workers",
        type=int,
        default=2,
        help="Número de scrapers en paralelo (recomendado: 2 a 4)",
    )
    parser.add_argument(
        "-l",
        "--nlistados",
        type=int,
        default=None,
        help="Número de listados específicos a procesar (si no se especifica, se procesan todos los listados activos)",
    )
    args = parser.parse_args()


    return args


def ejecutar_scraper(listado_item: tuple) -> str:
    listado_id, competencia, url_listado = listado_item
    scraper = ListadosScraper(listado_id=listado_id, url_listado=url_listado, headless=False)

    if competencia == "Liverpool":
        scraper.scrape_listado_liverpool()
        return f"✅ Liverpool completado: {listado_id}"
    if competencia == "Coppel":
        scraper.scrape_listado_coppel()
        return f"✅ Coppel completado: {listado_id}"
    if competencia == "Sears":
        scraper.scrape_listado_sears()
        return f"✅ Sears completado: {listado_id}"

    return f"ℹ️ Competencia no soportada: {competencia} ({listado_id})"


def esperar_hasta_hora_objetivo() -> None:
    ahora = datetime.now()
    objetivo = ahora.replace(hour=0, minute=0, second=1, microsecond=0)

    if ahora >= objetivo:
        objetivo = objetivo + timedelta(days=1)

    segundos_espera = (objetivo - ahora).total_seconds()
    print(f"⏳ Esperando hasta {objetivo.strftime('%Y-%m-%d %H:%M:%S')} para ejecutar scraping...")
    time.sleep(segundos_espera)


if __name__ == "__main__":
    args = parsear_argumentos()
    esperar_hasta_hora_objetivo()
    print("Ejecutando el script principal")
    if args.reset:
        print("Se ha solicitado resetear la base de datos")
        resetear_base_de_datos()
        inicializar_base_de_datos()

    listados = obtener_listados()
    if args.nlistados:
        listados = listados[:args.nlistados]
        print(f"Procesando solo los listados especificados: {args.nlistados}")

    with ThreadPoolExecutor(max_workers=max(1, args.workers)) as executor:
        futures = [executor.submit(ejecutar_scraper, listado) for listado in listados]
        for future in as_completed(futures):
            try:
                print(future.result())
            except Exception as e:
                print(f"❌ Error en tarea de scraping: {e}")

    print("Procesamiento de listados completado")
    print(f"El scraping ha finalizado {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}.")

    procesar_catalogo()
    print("Procesamiento de contenidos completado")
    print(f"El procesamiento de contenido ha finalizado {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}.")

    procesar_productos()
    print("Procesamiento de productos completado")
    print(f"El procesamiento de productos ha finalizado {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}.")

