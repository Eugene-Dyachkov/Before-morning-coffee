import asyncio
import websockets
import json
import requests
import datetime
import psycopg
from aiohttp import ClientSession


class Get_data():
    async def get_weather(self):
        async with ClientSession() as session:
            async with session.get(
                "https://api.openweathermap.org/data/2.5/weather?lat=53.19&lon=45.01&appid=e4be4831d7607ab68d261546d157d614&units=metric"
            ) as response:
                content = await response.json()
                self.weather = [content['name'], content['main']['temp']]
                print(self.weather)


    async def get_valutes(self):
        async with ClientSession() as session:
            async with session.get("https://www.cbr-xml-daily.ru/daily_json.js") as res:
                content = await res.text()
                valutes = json.loads(content)
                self.valutes_content = [
                valutes['Valute']['USD']['Value'],
                valutes['Valute']['EUR']['Value']
                ]
            print(self.valutes_content)

    async def get_tg(self):
        create_json = await asyncio.create_subprocess_shell(
            'snscrape --max-result 1 --jsonl telegram-channel breakingmash > telegram.json'
            )
        await create_json.wait()
        with open('telegram.json') as tg_json:
            self.tg_content = []
            for item in tg_json:
                item = json.loads(item)
                self.tg_content.append(item['content'])
            print(self.tg_content)


class Get_Db:
    async def connect(self):
        try:
            async with await psycopg.AsyncConnection.connect(
                host = "192.168.88.225",
                user = "eugene",
                password = "123",
                dbname = "site_db") as self.conn:

                async with self.conn.cursor()  as cur:
                    await cur.execute(
                        "SELECT version();"
                    )
                    print(await cur.fetchone())
        except Exception as ex:
            print(ex)

    async def create_table(self):
        try:
            async with self.conn.cursor() as cur:
                await cur.execute(
                    "CREATE TABLE IF NOT EXISTS notes(notes_id int AUTO_INCREMENT,"\
                        "header varchar(32) NOT NULL,"\
                        "text varchar(32) NOT NULL,"\
                        "data data NOT NULL,"\
                        "PRIMARY KEY(notes_id));"
                )
                print(await cur.fetchone())
        except Exception as ex:
            print(ex)


async def new_client(client_socket, path):
    print("New client")
    data = Get_data()
    db = Get_Db()
    event_loop.create_task(data.get_tg())
    event_loop.create_task(data.get_weather())
    event_loop.create_task(data.get_valutes())
    event_loop.create_task(db.connect())
    while True:
        try:
            comand = await client_socket.recv()
            print(comand)
        except:
            pass

async def start_server():
    db = Get_Db()
    await websockets.serve(new_client, "192.168.88.228", 8855)

if __name__ == "__main__":
    event_loop = asyncio.new_event_loop()
    event_loop.run_until_complete(start_server())
    event_loop.run_forever()
