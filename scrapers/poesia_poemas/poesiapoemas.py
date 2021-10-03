import re
from loggs.log import logger
from lxml.html import document_fromstring, HtmlElement, tostring
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec

driver = webdriver.Chrome('/Users/usuarioman/WebDrivers/chromedriver')

from cliente import get_http_client
from bs4 import BeautifulSoup
import asyncio

from db.utils import get_motor_client


def get_html_element(text_response):
    try:
        h_element = document_fromstring(text_response)
        assert isinstance(h_element, HtmlElement)
        return h_element

    except AssertionError:
        print('Nop, no es un HtmlElement')
        pass


async def extract_links():
    motor = get_motor_client()
    collection = motor.get_collection('perrito_poeta', 'poesiapoemas')
    cliente = get_http_client()

    letras = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u",
              "v", "w", "x", "y", "z"]

    links_to_scrap = [f"http://www.poesiaspoemas.com/poetas-{link}" for link in letras]

    for link in links_to_scrap:
        async with cliente.request(method='GET',
                                   url=link,
                                   ) as response:
            text = await response.text()
            sopa = BeautifulSoup(text, features='html.parser')

            for element in sopa.select('.poetbox a'):
                author = element.get_text()
                link = "http://www.poesiaspoemas.com" + element.attrs['href']
                await collection.insert_one({'autor': author, 'link_autor_page': link})


async def extract_poemas():
    motor = get_motor_client()
    collection = motor.get_collection('perrito_poeta', 'poesiapoemas')
    wait = WebDriverWait(driver, 10)

    async for doc in collection.find({"lista_poemas": {"$exists": False}}):
        if len(doc['lista_link_poemas']) <= 0:
            logger.info('No tiene poemas, ignorando.')
            pass

        else:
            poemas = list()
            link_autor = doc['link_author_page']
            link_lista_poemas = doc['lista_link_poemas']
            logger.info(f'{len(link_lista_poemas)} poemas a descargar . . .')
            try:
                for poem_link in link_lista_poemas:
                    try:
                        driver.get(poem_link)
                        wait.until(ec.visibility_of_element_located((By.ID, 'poematext')))

                        poema_raw = driver.find_element_by_id('poematext').text

                        titulo = driver.find_element_by_tag_name('span').text

                        votos_texto = driver.find_element_by_css_selector('.vt').text

                        votos_integer = int(re.search(r'\d*', votos_texto).group(0))

                        sep = '¿ Te gustó este poema?'
                        second_sep = 'publicado el '
                        stripped = poema_raw.split(sep, 1)[0]
                        poema = stripped.split(second_sep, 1)[1]

                        data = {"texto_poema": poema,
                                'titulo_poema': titulo,
                                'votos_texto': votos_texto,
                                'votos_integer': votos_integer,
                                'url_poema': poem_link,
                                }

                        poemas.append(data)

                    except Exception as e:
                        logger.error(f'ERROR SACANDO INFORMACIÓN DE LA PÁGINA.{e}')
                        continue

                logger.info(f'LA SIGUIENTE LISTA DE POEMAS SE HA CREADO: {poemas}')

                await collection.update_one({'link_author_page': link_autor}, {'$set': {"lista_poemas": poemas}})

            except Exception as e:
                logger.error(e)
                continue


loop = asyncio.get_event_loop()

task = extract_poemas()
loop.run_until_complete(task)
