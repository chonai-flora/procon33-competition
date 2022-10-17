from __future__ import annotations
import aiohttp
import requests
import wave
import json

HOST = ''
TOKEN = ''
HEADER = {
    "Content-Type": "application/json", 
    'procon-token': TOKEN
}


async def get_match():
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(HOST + '/match', headers=HEADER, ssl=True) as res:
                if res.status == requests.codes.ok:
                    return await res.json()
                return await res.text()
            
        except Exception as err:
            print(err)
            return err


async def get_problem():
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(HOST + '/problem', headers=HEADER, ssl=True) as res:
                if res.status == requests.codes.ok:
                    return await res.json()
                return await res.text()
            
        except Exception as err:
            print(err)
            return err


async def get_chunks(div):
    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(HOST + '/problem/chunks?n=' + str(div), headers=HEADER, ssl=True) as res:
                if res.status == requests.codes.ok:
                    return await res.json()
                return await res.text()

        except Exception as err:
            print(err)
            return err


async def get_file(file_name, save_path):
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(HOST + '/problem/chunks/' + file_name, headers=HEADER, ssl=True) as res:
                if res.status == requests.codes.ok:
                    data = await res.read()
                    with wave.open(save_path + file_name, mode='wb') as f:
                        f.setnchannels(1)
                        f.setsampwidth(2)
                        f.setframerate(48000)
                        f.writeframes(bytes(data))
                else:
                    data = await res.text()
                return data
        except Exception as err:
            print(err)
            return err


async def answer(problem_id, answers):
    body = json.dumps({"problem_id": problem_id, "answers": answers})

    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(HOST + '/problem', data=body, headers=HEADER, ssl=True) as res:
                if res.status == requests.codes.ok:
                    return await res.json()
                return await res.text()
            
        except Exception as err:
            print(err)
            return err