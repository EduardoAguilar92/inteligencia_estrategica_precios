import argparse

from database.reset_db import resetear_base_de_datos
from database.init_db import inicializar_base_de_datos
from scrapers.listados import obtener_listados
from scrapers.contenidos import ListadosScraper


def parsear_argumentos() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Scraper de listados de productos")
    parser.add_argument(
        "-r",
        "--reset",
        required=False,
        help="Indica si se debe resetear la base de datos antes de iniciar el proceso (elimina todas las tablas y datos)",
    )
    args = parser.parse_args()


    return args


if __name__ == "__main__":
    args = parsear_argumentos()
    print("Ejecutando el script principal")
    if args.reset:
        print("Se ha solicitado resetear la base de datos")
        resetear_base_de_datos()
        inicializar_base_de_datos()
    listado = obtener_listados()
    print("Listados obtenidos:")
    for listado in listado:
        print(listado)
        if listado[1] == 'Liverpool':  # Verifica que la URL no esté vacía
            scraper = ListadosScraper(listado_id=listado[0], url_listado=listado[2], headless=False)
            scraper.scrape_listado_liverpool()
        if listado[1] == 'Coppel':  # Verifica que la URL no esté vacía
            scraper = ListadosScraper(listado_id=listado[0], url_listado=listado[2], headless=False)
            scraper.scrape_listado_coppel()
        if listado[1] == 'Sears':  # Verifica que la URL no esté vacía
            scraper = ListadosScraper(listado_id=listado[0], url_listado=listado[2], headless=False)
            scraper.scrape_listado_sears()