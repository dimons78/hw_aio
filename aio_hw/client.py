import asyncio

import aiohttp
import requests


async def main():
    async with aiohttp.ClientSession() as session:

        # СОЗДАНИЕ
        response = await session.post(
            "http://127.0.0.1:8080/ann/",
            json={"title": "title_6",
                  "description": "Для загрузки начальных данных модели Book необходимо выполнить команду",
                  "owner": "owner_1",}
        )

        data = await response.json()
        print(data)


        # ПОЛУЧЕНИЕ
        response = await session.get("http://127.0.0.1:8080/ann/9/")
        data = await response.json()
        print(data)



        # УДАЛЕНИЕ
        response = await session.delete(
            "http://127.0.0.1:8080/ann/9/",

        )
        data = await response.json()
        print(data)


        # ПОЛУЧЕНИЕ
        response = await session.get("http://127.0.0.1:8080/ann/9/")
        data = await response.json()
        print(data)


asyncio.run(main())
