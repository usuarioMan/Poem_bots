import asyncio
from aiohttp import ClientSession
from bs4 import BeautifulSoup

from db.utils import get_motor_client


# ------------------------------------------------------------- AUTHOR PAGE
async def fetch_first_stage(url, session):
    motor = get_motor_client()
    collection = motor.get_collection('perrito_poeta', 'poesiapoemas')
    async with session.get(url) as response:
        text = await response.text()
        sopa = BeautifulSoup(text, features='html.parser')
        for element in sopa.select('.poetbox a'):
            author = element.get_text()
            link = "http://www.poesiaspoemas.com" + element.attrs['href']
            await collection.insert_one({'autor': author, 'link_author_page': link})


async def first_stage():
    letras = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u",
              "v", "w", "x", "y", "z"]
    links_to_scrap = [f"http://www.poesiaspoemas.com/poetas-{link}" for link in letras]
    tasks = []
    async with ClientSession() as session:
        for link in links_to_scrap:
            task = asyncio.ensure_future(fetch_first_stage(link, session))
            tasks.append(task)

        await asyncio.gather(*tasks)


# ------------------------------------------------------------- LIST OF POEMS.
async def fetch_second_stage(url, session, collection):
    async with session.get(url[1]) as response:
        text = await response.text()
        status = response.status
        lista_link_poemas = list()

        if status == 200:
            sopa = BeautifulSoup(text, features='html.parser')

            try:
                tags = sopa.select('.leer')
                assert len(tags) > 0
                for tag in tags:
                    link = "http://www.poesiaspoemas.com" + tag.attrs['href']
                    lista_link_poemas.append(link)

            except AssertionError:
                try:
                    tags = sopa.select('.tpoem')
                    assert len(tags) > 0

                    for tag in tags:
                        link = "http://www.poesiaspoemas.com" + tag.attrs['href']
                        lista_link_poemas.append(link)

                except Exception as error:
                    pass

            await collection.update_one({'_id': url[0]}, {'$set': {"lista_link_poemas": lista_link_poemas}})

        elif status == 503:
            try:
                await asyncio.sleep(15)
                sopa = BeautifulSoup(text, features='html.parser')
                tags = sopa.select('.leer')
                assert len(tags) > 0
                for tag in tags:
                    link = "http://www.poesiaspoemas.com" + tag.attrs['href']
                    lista_link_poemas.append(link)

                await collection.update_one({'_id': url[0]}, {'$set': {"lista_link_poemas": lista_link_poemas}})

            except AssertionError:
                try:
                    tags = sopa.select('.tpoem')
                    assert len(tags) > 0

                    for tag in tags:
                        link = "http://www.poesiaspoemas.com" + tag.attrs['href']
                        lista_link_poemas.append(link)

                    await collection.update_one({'_id': url[0]}, {'$set': {"lista_link_poemas": lista_link_poemas}})

                except Exception as error:
                    await collection.update_one({'_id': url[0]}, {'$set': {"lista_link_poemas": []}})


async def second_stage():
    motor = get_motor_client()
    collection = motor.get_collection('perrito_poeta', 'poesiapoemas')
    links_to_scrap = list()
    tasks = []
    async for document in collection.find({}):
        links_to_scrap.append((document['_id'], document['link_author_page']))

    async with ClientSession() as session:
        for link in links_to_scrap:
            task = asyncio.ensure_future(fetch_second_stage(link, session, collection))
            tasks.append(task)

        await asyncio.gather(*tasks)


# ------------------------------------------------------------- RETRY MF.
async def fetch_third_stage(url, session, collection):
    async with session.get(url[1]) as response:
        text = await response.text()
        status = response.status
        lista_link_poemas = list()

        if status == 200:
            sopa = BeautifulSoup(text, features='html.parser')

            try:
                tags = sopa.select('.leer')
                assert len(tags) > 0
                for tag in tags:
                    link = "http://www.poesiaspoemas.com" + tag.attrs['href']
                    lista_link_poemas.append(link)

            except AssertionError:
                try:
                    tags = sopa.select('.tpoem')
                    assert len(tags) > 0

                    for tag in tags:
                        link = "http://www.poesiaspoemas.com" + tag.attrs['href']
                        lista_link_poemas.append(link)

                except Exception as error:
                    pass

            await collection.update_one({'_id': url[0]}, {'$set': {"lista_link_poemas": lista_link_poemas}})

        elif status == 503:
            try:
                await asyncio.sleep(15)
                sopa = BeautifulSoup(text, features='html.parser')
                tags = sopa.select('.leer')
                assert len(tags) > 0
                for tag in tags:
                    link = "http://www.poesiaspoemas.com" + tag.attrs['href']
                    lista_link_poemas.append(link)

                await collection.update_one({'_id': url[0]}, {'$set': {"lista_link_poemas": lista_link_poemas}})

            except AssertionError:
                try:
                    tags = sopa.select('.tpoem')
                    assert len(tags) > 0

                    for tag in tags:
                        link = "http://www.poesiaspoemas.com" + tag.attrs['href']
                        lista_link_poemas.append(link)

                    await collection.update_one({'_id': url[0]}, {'$set': {"lista_link_poemas": lista_link_poemas}})

                except Exception:
                    pass


async def third_stage():
    motor = get_motor_client()
    collection = motor.get_collection('perrito_poeta', 'poesiapoemas')
    links_to_scrap = list()
    tasks = []
    async for document in collection.find({"lista_link_poemas": {"$size": 0}}):
        links_to_scrap.append((document['_id'], document['link_author_page']))

    async with ClientSession() as session:
        for link in links_to_scrap:
            task = asyncio.ensure_future(fetch_third_stage(link, session, collection))
            tasks.append(task)

        await asyncio.gather(*tasks)
    await asyncio.sleep(60)


# async def fetch_fourth_stage(urls, session, collection):
#     _id = urls[0]
#     for url in urls[1]:
#         async with session.get(url) as response:
#             if response.status == 200:
#                 text = await response.text()
#                 html = document_fromstring(text)
#                 text = html.get_element_by_id('poematext')
#                 print(text.text)
#                 print('')


# async def fourth_stage():
#    motor = get_motor_client()
#    collection = motor.get_collection('perrito_poeta', 'poesiapoemas')
#    links_to_scrap = list()
#    tasks = []
#    async for document in collection.find({}):
#        try:
#            if len(document['lista_link_poemas']) > 0:
#                links_to_scrap.append((document['_id'], document['lista_link_poemas'], collection))
#        except KeyError:
#            print(document)
#            exit(1)
#
#    async with ClientSession() as session:
#        for link in links_to_scrap:
#            task = asyncio.ensure_future(fetch_fourth_stage(link, session, collection))
#            tasks.append(task)
#
#        await asyncio.gather(*tasks)
#    # await asyncio.sleep(60)


loop = asyncio.get_event_loop()
# future = asyncio.ensure_future(first_stage())
# loop.run_until_complete(future)
#
# future = asyncio.ensure_future(second_stage())
# loop.run_until_complete(future)
# future = asyncio.ensure_future(third_stage())
# loop.run_until_complete(future)
# future = asyncio.ensure_future(third_stage())
# loop.run_until_complete(future)
future = asyncio.ensure_future(third_stage())
loop.run_until_complete(future)
future = asyncio.ensure_future(third_stage())
loop.run_until_complete(future)
