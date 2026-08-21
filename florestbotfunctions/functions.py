from .dataclasses import *
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import os, re
import numpy as np
import random, requests
import aiohttp
import asyncio
import zipfile
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as Service1
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from tqdm.asyncio import tqdm
import numpy
import cv2
from yoloface import face_analysis
from telethon.sync import TelegramClient
from mcstatus import JavaServer, BedrockServer
from g4f.client import Client, AsyncClient
from g4f.Provider import OIVSCodeSer2, Blackbox, Chatai, LegacyLMArena, PollinationsAI, RetryProvider, ARTA, PollinationsImage
from g4f.Provider import Together
from yt_dlp import YoutubeDL
import torch
from whisper import load_model
from moviepy import VideoFileClip, TextClip, CompositeVideoClip
import librosa
from typing import Dict, Any, Optional, List
import xml.etree.ElementTree as ET
import feedparser
from newspaper import Article
import datetime
from donationalerts.asyncio_api import Alert, Event
from functools import wraps

from dataclasses import dataclass
from typing import Any, Dict, Callable
from duckduckgo_search import DDGS
import subprocess
from PIL import ImageDraw, Image, ImageFont
import time
import vk_api

from math import radians, sin, cos, asin, sqrt

from ollama import Client

class FunctionsObject:
    def __init__(self, proxies: dict = {}, html_headers: dict = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36', 'Accept-Language': 'ru-RU'}, google_api_key: str = "", gigachat_key: str = "", gigachat_id: str = "", username_mail: str = "", mail_passwd: str = "", speech_to_text_key: str = None, vk_token: str = None, rcon_ip: str = None, rcon_port: int = None, rcon_password: str = None, whisper_model: str = None, ollama_active: bool = False):
        """Привет. Именно в данном классе находятся ВСЕ функции бота. Давай я объясню смысл параметров?\nproxies: прокси, которые используются при HTTPS запросах к сайтам.\nhtml_headers: заголовки HTTPS запросов.\ngoogle_api_key: апи ключ гугла. Получить его можно [здесь](https://console.google.com/)\ngigachat_key: ключ от GigaChat (ПАО "СберБанк")\ngigachat_id: ID от GigaChat.\nusername_mail: ваша электронная почта.\nmail_passwd: ваш API-ключ от SMTP сервера.\nspeech_to_text_key: API ключ от Google Speech To Text. Необязательно.\nvk_token: токен для работы с VK API от вашего аккаунта.\nrcon_ip: IP адрес сервера, к которому нужно подключиться.\nrcon_port: порт удаленного администрирования RCON, по умолчанию, 25575.\nrcon_password: пароль для доступа к RCON. Храните его в надежном месте.\nwhisper_model: модель для распознаватора речи и создания субтитров. К примеру, tiny."""
        print(f'Объект класса был успешно запущен.')
        self.proxies = proxies
        self.headers = html_headers
        self.google_key = google_api_key
        self.gigachat_key = gigachat_key
        self.client_id_gigachat = gigachat_id
        self.username_mail = username_mail
        self.mail_passwd = mail_passwd
        self.speech_to_text_key = speech_to_text_key
        self.token_of_vk = vk_token
        self.client_for_gpt = Client()
        if all([rcon_ip, rcon_port, rcon_password]):
            from mcrcon import MCRcon
            self.rcon_server = MCRcon(rcon_ip, rcon_password, rcon_port)
            print(f'RCON сервер инициализирован и готов к запуску.')
        else:
            self.rcon_server = None
        self.duckduckgo = DDGS(proxies=proxies)
        self.ollama_client = Client() if ollama_active else None
    def generate_image(self, prompt: str) -> bytes:
        """Данная функция генерирует картинки с помощью GigaChat.\nprompt: запрос, по которому надо сгенерировать изображение."""
        import requests, re, urllib3
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        if self.gigachat_key and self.client_id_gigachat:
            url = "https://ngw.devices.sberbank.ru:9443/api/v2/oauth"

            payload={
                'scope': 'GIGACHAT_API_PERS'
            }
            headers = {
                'Content-Type': 'application/x-www-form-urlencoded',
                'Accept': 'application/json',
                'RqUID': f'{self.client_id_gigachat}',
                'Authorization': f'Basic {self.gigachat_key}'
            }

            response = requests.request("POST", url, headers=headers, data=payload, verify=False, proxies=self.proxies)

            access_token = response.json()['access_token']

            headers = {
                'Content-Type': 'application/json',
                'Accept': 'application/json',
                'Authorization': f'Bearer {access_token}'
            }

            data = {
                "model": "GigaChat",
                "messages": [
                    {
                        "role": "system",
                        "content": "Glory to Florest."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                "function_call": "auto"
            }

            patterns = r"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}"

            response = requests.post(
                'https://gigachat.devices.sberbank.ru/api/v1/chat/completions',
                headers=headers,
                json=data,
                verify=False,
                proxies=self.proxies
            )
            json = response.json()
            matches = re.search(patterns, json['choices'][0]['message']['content'])
            if not matches:
                return f"Нельзя нарисовать что-либо по данному запросу. Причина: {json['choices'][0]['message']['content']}"
            else:
                req_img = requests.get(f"https://gigachat.devices.sberbank.ru/api/v1/files/{matches}/content", headers={'Accept': 'application/jpg', "Authorization":f"Bearer {access_token}"}, verify=False, stream=True, proxies=self.proxies)
                return req_img.content
        else:
            return "Нужно указать параметр `gigachat_key` и `gigachat_id` в настройках класса для работы с этой функцией."
    def ai(self, prompt: str, is_voice: bool = False):
        """Используем GigaChat.\nprompt: что тебе нужно от нейросетки.\nis_voice: записать-ли нам голосовуху?"""
        import requests, json, gtts, io
        import urllib3
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        if self.gigachat_key and self.client_id_gigachat:
            if not is_voice:
                url = "https://ngw.devices.sberbank.ru:9443/api/v2/oauth"

                payload={
                    'scope': 'GIGACHAT_API_PERS'
                }
                headers = {
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'Accept': 'application/json',
                    'RqUID': f'{self.client_id_gigachat}',
                    'Authorization': f'Basic {self.gigachat_key}'
                }

                response = requests.request("POST", url, headers=headers, data=payload, verify=False, proxies=self.proxies)

                access_token = response.json()['access_token']

                url1 = "https://gigachat.devices.sberbank.ru/api/v1/chat/completions"

                payload1 = json.dumps({
                    "model": "GigaChat",
                    "messages": [
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],
                    "stream": False,
                    "repetition_penalty": 1
                })
                headers1 = {
                    'Content-Type': 'application/json',
                    'Accept': 'application/json',
                    'Authorization': f'Bearer {access_token}'
                }

                response1 = requests.request("POST", url1, headers=headers1, data=payload1, verify=False, proxies=self.proxies)
                return response1.json()
            else:
                url = "https://ngw.devices.sberbank.ru:9443/api/v2/oauth"

                payload={
                    'scope': 'GIGACHAT_API_PERS'
                }
                headers = {
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'Accept': 'application/json',
                    'RqUID': f'{self.client_id_gigachat}',
                    'Authorization': f'Basic {self.gigachat_key}'
                }

                response = requests.request("POST", url, headers=headers, data=payload, verify=False, proxies=self.proxies)

                access_token = response.json()['access_token']

                url1 = "https://gigachat.devices.sberbank.ru/api/v1/chat/completions"

                payload1 = json.dumps({
                    "model": "GigaChat",
                    "messages": [
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],
                    "stream": False,
                    "repetition_penalty": 1
                })
                headers1 = {
                    'Content-Type': 'application/json',
                    'Accept': 'application/json',
                    'Authorization': f'Bearer {access_token}'
                }

                response1 = requests.request("POST", url1, headers=headers1, data=payload1, verify=False, proxies=self.proxies)
                buffer = io.BytesIO()
                gtts.gTTS(response1.json()['choices'][0]['message']['content'], lang='ru', lang_check=False).write_to_fp(buffer)
                return buffer.getvalue()
        else:
            return "Нужно указать параметр `gigachat_key` и `gigachat_id` в настройках класса для работы с этой функцией."
        
    def deanon(self, ip: str) -> list:
        """Деанончик по IP.\nВы сами принимаете на себя ответственность за использование данной функции.\nip: дай айпи, тварюка."""
        import requests
        r = requests.get(f'http://ip-api.com/json/{ip}?lang=ru', proxies=self.proxies, headers=self.headers).json()
        results = []
        for key, value in r.items():
            results.append(f'{key.title()}: {value}')
        return results
    def download_video(self, url: str):
        """Данная функция качает видео с YouTube с помощью URL.\nurl: ссылка на видео."""
        from pytubefix import YouTube
        from tqdm import tqdm as sync_tqdm

        yt_obj = YouTube(url, proxies=self.proxies)

        if yt_obj.age_restricted:
            return 'На видео наложены возрастные ограничения.'    
        else:
            return yt_obj
    def search_videos(self, query: str):
        """Функция для поиска видео по запросу и дальнейшего его закачивания.\nquery: запрос, по которому надо искать видео."""
        from pytubefix import Search
        from tqdm import tqdm as sync_tqdm

        search = Search(query, proxies=self.proxies)
        return [search.videos if search.videos else "Not Founded!"]
    def create_demotivator(self, top_text: str, bottom_text: str, photo: bytes, font: str):
        """Создайте демотиватор с помощью данной фичи!\ntop_text: верхний текст.\nbottom_text: нижний текст.\nphoto: ваша фотография в bytes.\nfont: ваш шрифт. Пример: `times.ttf`."""
        import io
        image = io.BytesIO(photo)
        from PIL import Image, ImageOps, ImageDraw, ImageFont
        img = Image.new('RGB', (1280, 1024), color='black')
        img_border = Image.new('RGB', (1060, 720), color='#000000')
        border = ImageOps.expand(img_border, border=2, fill='#ffffff')
        user_img = Image.open(image).convert("RGBA").resize((1050, 710))
        (width, height) = user_img.size
        img.paste(border, (111, 96))
        img.paste(user_img, (118, 103))
        drawer = ImageDraw.Draw(img)
        font_1 = ImageFont.truetype(font=font, size=80, encoding='UTF-8')
        text_width = font_1.getlength(top_text)

        while text_width >= (width + 250) - 20:
            font_1 = ImageFont.truetype(font=font, size=80, encoding='UTF-8')
            text_width = font_1.getlength(top_text)
            top_size -= 1

        font_2 = ImageFont.truetype(font=font, size=60, encoding='UTF-8')
        text_width = font_2.getlength(bottom_text)

        while text_width >= (width + 250) - 20:
            font_2 = ImageFont.truetype(font=font, size=60, encoding='UTF-8')
            text_width = font_2.getlength(bottom_text)
            bottom_size -= 1

        size_1 = drawer.textlength(top_text, font=font_1)
        size_2 = drawer.textlength(bottom_text, font=font_2)

        drawer.text(((1280 - size_1) / 2, 840), top_text, fill='white', font=font_1)
        drawer.text(((1280 - size_2) / 2, 930), bottom_text, fill='white', font=font_2)

        result_here = io.BytesIO()

        img.save(result_here, 'JPEG')
    
        del drawer

        return result_here.getvalue()
    def photo_make_black(self, photo: bytes):
        """Сделать фото черно-белым.\nphoto: фото в `bytes`."""
        import io
        from PIL import Image
        your_photo = io.BytesIO(photo)

        image = Image.open(your_photo)
        new_image = image.convert('L')
        buffer = io.BytesIO()
        new_image.save(buffer, 'JPEG')
        return buffer.getvalue()
    def check_weather(self, city):
        """Проверить погоду в каком-либо городе.\ncity: город, или его координаты в виде словаря `{"lat":..., "lon":...}`.\nИспользуется бесплатный OpenMeteo API."""
        import requests
        if isinstance(city, str):
            try:
                d = requests.get(f'https://geocoding-api.open-meteo.com/v1/search?name={city}', proxies=self.proxies, headers=self.headers).json()
                lot = d["results"][0]["latitude"]
                lat = d['results'][0]['longitude']
                req = requests.get(f'https://api.open-meteo.com/v1/forecast?latitude={lot}&longitude={lat}&current_weather=true', headers=self.headers, proxies=self.proxies)
                if req.status_code != 200:
                    return None
                else:
                    data = req.json()
                    temperature = data['current_weather']['temperature']
                    title = {0: "Ясно", 1: "Частично облачно", 3: "Облачно", 61: "Дождь"}
                    weather = title.get(data['current_weather']['weathercode'], 'Неизвестно')
                    wind_dir = 'Север' if 0 <= (d := data['current_weather']['winddirection']) < 45 or 315 <= d <= 360 else 'Восток' if 45 <= d < 135 else 'Юг' if 135 <= d < 225 else 'Запад'
                    time1 = data['current_weather']['time']
                    wind = data['current_weather']['windspeed']
                    return {'temp':temperature, 'weather':weather, 'weather_code':data['current_weather']['weathercode'], 'wind_direction':wind_dir, 'time_of_data':time1, 'wind_speed':wind}
            except:
                return None
        elif isinstance(city, dict):
            try:
                try:
                    lat = city["lat"]
                    lon = city["lon"]
                    req = requests.get(f'https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true', headers=self.headers, proxies=self.proxies)
                except KeyError:
                    return f'Нужно составить словарь, согласно образцу, указанного в описании функции.'
                
                data = req.json()
                temperature = data['current_weather']['temperature']
                title = {0: "Ясно", 1: "Частично облачно", 3: "Облачно", 61: "Дождь"}
                weather = title.get(data['current_weather']['weathercode'], 'Неизвестно')
                wind_dir = 'Север' if 0 <= (d := data['current_weather']['winddirection']) < 45 or 315 <= d <= 360 else 'Восток' if 45 <= d < 135 else 'Юг' if 135 <= d < 225 else 'Запад'
                time1 = data['current_weather']['time']
                wind = data['current_weather']['windspeed']
                return {'temp':temperature, 'weather':weather, 'weather_code':data['current_weather']['weathercode'], 'wind_direction':wind_dir, 'time_of_data':time1, 'wind_speed':wind}
            except:
                return None
        else:
            return 'Поддерживаемые типы данных: `str` для названия города и `dict` для координатов.'
    def create_qr(self, content: str):
        """Создать QR код.\ncontent: что будет нести в себе qr. ссылка, текст..."""
        import qrcode
        import io
        
        buffer = io.BytesIO()
        qr = qrcode.make(content)
        qr.save(buffer, scale=10)
        return buffer.getvalue()
    def get_charts(self):
        """Узнать чарты Я.Музыки."""
        import requests
        headers = {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7,fi;q=0.6,nb;q=0.5,is;q=0.4,pt;q=0.3,ro;q=0.2,it;q=0.1,de;q=0.1',
            'Connection': 'keep-alive',
            'Referer': 'https://music.yandex.ru/chart',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
            'X-Current-UID': '403036463',
            'X-Requested-With': 'XMLHttpRequest',
            'X-Retpath-Y': 'https://music.yandex.ru/chart',
            'sec-ch-ua': '"Not?A_Brand";v="8", "Chromium";v="108", "Google Chrome";v="108"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Linux"',
        }

        params = {
            'what': 'chart',
            'lang': 'ru',
            'external-domain': 'music.yandex.ru',
            'overembed': 'false',
            'ncrnd': '0.23800355071570123',
        }
        result = []
        response = requests.get('https://music.yandex.ru/handlers/main.jsx', params=params, headers=headers, proxies=self.proxies)
        chart = response.json()['chartPositions']
        for track in chart[:10]:
            position = track['track']['chart']['position']
            title = track['track']['title']
            author = track['track']['artists'][0]['name']
            result.append(f"№{position}: {author} - {title}")
        return f'Чарты Яндекс Музыки на данный момент🔥\n🥇{result[0]}\n🥈{result[1]}\n🥉{result[2]}\n{result[3]}\n{result[4]}\n{result[5]}\n{result[6]}\n{result[7]}\n{result[8]}\n{result[9]}'
    def generate_password(self, symbols: int = 15):
        """Сгенерировать пароль.\nsymbols: количество символов в пароле."""
        import string
        import random

        symbols_ascii = list(string.ascii_letters + string.digits)

        random.shuffle(symbols_ascii)

        return ''.join(symbols_ascii[:symbols])
    def text_to_speech(self, text: str, lang: str = 'ru'):
        """Из текста в речь на Python.\ntext: текст для озвучки.\nlang: язык для озвучки. По умолчанию, **русский**."""
        import gtts
        import io

        buffer = io.BytesIO()
        engine = gtts.gTTS(text, lang=lang)
        engine.write_to_fp(buffer)
        return buffer.getvalue()
    def information_about_yt_channel(self, url: str):
        """Узнать информацию о YouTube канале на Python.\nurl: ссылка на канал."""
        if not self.google_key:
            return 'Для использования данной функции нужно указать параметр `google_key` в конструктор класса.'
        else:
            import requests
            if '/channel/' in url:
                channel_id = url.split('/channel/')[-1].split('?')[0]
                params = {
                    "part": "snippet,statistics",
                    "id": channel_id,
                    "key": self.google_key
                }
            else:
                username = url.split('/@')[-1].split('?')[0]
                params = {
                    "part": "snippet,statistics",
                    "forHandle": f"@{username}",
                    "key": self.google_key
                }
            request = requests.get('https://www.googleapis.com/youtube/v3/channels', proxies=self.proxies, headers=self.headers, params=params)
            response = request.json()
            return response
    def crypto_price(self, crypto: str, currency: str = 'rub'):
        """Цена криптовалют.\ncrypto: крипта, которую нужно узнать. Для этого воспользуйтесь константами из класса `Cripto`.\ncurrency: валюта, в которой нужно получить результат. Доступно: `rub`, `usd` и `eur`."""
        import requests
        r = requests.get('https://api.coingecko.com/api/v3/simple/price', params={"ids":crypto, 'vs_currencies':currency}, proxies=self.proxies, headers=self.headers).json()
        if r == {}:
            return "Неправильная валюта, или криптовалюта."
        else:
            try:
                return r[crypto][currency]
            except:
                return "Произошла ошибка. Возможно, были преодолены лимиты API."
    def password_check(self, nickname: str) -> int:
        """Поиск сливов паролей по нику.\nnickname: ник для поиска.\nВозвращает `int`."""
        import requests
        req = requests.get(f'https://api.proxynova.com/comb?query={nickname}&start=0&limit=15', headers=self.headers, proxies=self.proxies)
        if req.status_code == 200:
            return req.json()['count']
    def generate_nitro(self, count: int):
        """Генерация нитро.\n(Ключи могут не работать, может потребоваться некоторое количество попыток)\ncount: количество ключей."""
        import random, string
        a = 0
        results = []
        while a < count:
            characters = string.ascii_uppercase + string.digits
            random_code = ''.join(random.choice(characters) for _ in range(15))
            formatted_code = '-'.join(random_code[i:i+4] for i in range(0, 15, 4))
            results.append(formatted_code)
        del a
        return results
    def fake_human(self):
        """Фейковый гражданин Российской Федерации. Без вопросов.\nАргументы отсутствуют.\nВозвращает словарь `dict`."""
        import faker as faker_
        from datetime import date

        faker = faker_.Faker('ru-RU')
        today = date.today()
        year_f = int(str(faker.date_of_birth(minimum_age=25, maximum_age=50)).split("-")[0])
        month_f = int(str(faker.date_of_birth(minimum_age=25, maximum_age=50)).split("-")[1])
        day_f = int(str(faker.date_of_birth(minimum_age=25, maximum_age=50)).split("-")[2])
        age_t = today.year - year_f - ((today.month, today.day) < (month_f, day_f))

        return {"name":faker.name(), "age":age_t, "work_place":faker.company(), "work_class":faker.job().lower(), "address":f"Российская Федерация, {faker.address()}", "postal_code":faker.address()[-6:], 'telephone_number':faker.phone_number(), "useragent":faker.user_agent(), "number_card":faker.credit_card_number(), "provider_of_card":faker.credit_card_provider(), "expire_card":faker.credit_card_expire(), "inn":faker.businesses_inn(), "orgn":faker.businesses_ogrn()}
    def real_info_of_photo(self, photo: bytes):
        """С помощью данной функции можно узнать адрес, город, почтовый индекс по фотографии.\nphoto: фотография в `bytes`."""
        import io
        from PIL import Image
        import requests
        with Image.open(io.BytesIO(photo)) as img:
            metadata = img._getexif()
            if not metadata:
                return None
            gps_info = metadata.get(34853)
            if not gps_info:
                return None
            lat = gps_info[2]
            lon = gps_info[4]
            lat_ref = gps_info[3]
            latitude = (lat[0] + lat[1] / 60.0 + lat[2] / 3600.0)
            longitude = (lon[0] + lon[1] / 60.0 + lon[2] / 3600.0)
            datetime_original = metadata.get(36867)
            try:
                if lat_ref != 'E':
                    latitude = -latitude
                r = requests.get(f"https://nominatim.openstreetmap.org/reverse?lat={latitude}&lon={longitude}&format=json", headers=self.headers, proxies=self.proxies)
                json = r.json()
                return {"country":json["address"]["country"], "region":json["address"]["state"], "district":json["address"]["district"], 'city':json["address"]["city"], "full_address":json["display_name"], 'postcode':json["address"]["postcode"], 'datetime':datetime_original}
            except:
                if lat_ref != 'E':
                    latitude = -latitude
                longitude = -longitude
                r = requests.get(f"https://nominatim.openstreetmap.org/reverse?lat={latitude}&lon={longitude}&format=json", headers=self.headers, proxies=self.proxies)
                json = r.json()
                return {"country":json["address"]["country"], "region":json["address"]["state"], "district":json["address"]["district"], 'city':json["address"]["city"], "full_address":json["display_name"], 'postcode':json["address"]["postcode"], 'datetime':datetime_original}
    def bmi(self, weight: float, height: float):
        """Узнать ИМТ по весу и росту.\nweight: дай вес в кг.\nheight: дай рост в метрах. Пример: 1.76 (176 см)\nВозвращает `dict` при удаче. `None` при невозможности узнать ИМТ. Не указывайте 0, либо отрицательные числа в параметры.\nИсходный код на канале моего друга: [тык](https://t.me/pie_rise_channel_s_8395/1009)"""
        if weight == 0 or weight < 0:
            return None
        else:
            if height == 0 or height < 0:
                return None
            else:
                bmi = weight / (height ** 2)
                if bmi < 18.5:
                    return {"bmi":f'{bmi:.2f}', "status":"Недостаточный вес"}
                elif 18.5 <= bmi < 25:
                    return {"bmi":f'{bmi:.2f}', "status":"Нормальный вес"}
                elif 25 <= bmi < 30:
                    return {"bmi":f'{bmi:.2f}', "status":"Избыточный вес"}
                else:
                    return {"bmi":f'{bmi:.2f}', "status":"Ожирение"}
    def link_on_user(self, id: str):
        """Введи ID юзера.\nГде его можно узнать?\nСкачайте Ayugram с официального сайта разработчика, а затем зайдите в профиль к человеку. Внизу будет его ID.\nЛибо зайдите в @username_to_id_bot и нажмите на кнопку \"User\". Если пользователь не отображается, добавьте его в контакты и повторите попытку.\nid: ID пользователя в кавычках."""
        if len(id) > 10:
            return {'status':f'Пользовательский ID не может привышать 10 символов.', 'url':None}
        elif len(id) < 10:
            return {"status":f'Пользовательский ID не может быть меньше, чем 10 символов.', 'url':None}
        else:
            try:
                return {"status":"Успех!", "url":F"tg://openmessage?user_id={int(id)}"}
            except:
                return {"status":f'Пользовательский ID не может привышать 10 символов.', 'url':None}
    def send_mail(self, subject: str, body: str, recipient: str, service: str = 'smtp.mail.ru', service_port: int = 465):
        """Отправить письмо по почте, используя Python.\nТребуется указать username_mail и mail_passwd в настройках класса для работы.\nsubject: тема письма.\nbody: остальная часть письма.\nrecipient: получатель.\nservice: сервис-провайдер вашего SMTP сервера.\nservice_port: порт SMTP сервера."""
        if self.username_mail and self.mail_passwd:
            from email.mime.multipart import MIMEMultipart
            from email.mime.text import MIMEText
            import smtplib
            message = MIMEMultipart()
            message["From"] = self.username_mail
            message["To"] = recipient
            message["Subject"] = subject
 
            message.attach(MIMEText(body, "plain", 'utf-8'))
 
            with smtplib.SMTP_SSL(service, service_port) as server:
                server.login(self.username_mail, password=self.mail_passwd)
                server.sendmail(self.username_mail, recipient, message.as_string())
        else:
            return "Укажите параметр username_mail и mail_passwd в настройках класса."
    def parsing_site(self, url: str):
        """Парсинг сайта)))\nЧисто скинем HTML код.\nurl: ссылка на сайт.\nПри удаче возвращает `str`."""
        import requests
        try:
            req = requests.get(url, proxies=self.proxies, headers=self.headers)
            if req.status_code == 200:
                return req.text
            else:
                return None
        except:
            return None
    def google_photo_parsing(self, query: str):
        """Парсинг гугл фото.\nВозвращает список с ссылками на фотографии, если есть.\nquery: запрос."""
        import requests
        from bs4 import BeautifulSoup
        req = requests.get(f'https://www.google.com/search?q={query}&tbm=isch&imglq=1&isz=l&safe=unactive', proxies=self.proxies)
        soup = BeautifulSoup(req.text, 'html.parser')
        tags = soup.find_all('img', {'src':True})
        imgs_links = []
        for tag in tags:
            if 'https://' in tag['src']:
                imgs_links.append(tag['src'])
        return imgs_links
    def speech_to_text(self, file, language: str = 'ru-RU') -> str:
        """Из речи в текст. Поддерживаются аудиофайлы формата: `wav`, `flac`.\nfile: директория к файлу. Либо open(), или io.BytesIO().\nlanguage: код языка. К примеру, `en-US`.\nВозвращает `str`!"""
        import speech_recognition as sr
        r = sr.Recognizer()
        with sr.AudioFile(file) as source:
            audio = r.record(source)
        try:
            text = r.recognize_google(audio, language=language)
            return text
        except sr.UnknownValueError:
            return 'Ошибка распознавания текста.'
        except:
            return 'Неизвестная ошибка. Также могут быть проблемы с подключением.'
    def email_mass_send(self, recievers: list, title: str, body: str, service: str = 'smtp.mail.ru', service_port: int = 465):
        """Функция для массовой отправки сообщений.\nrecievers: список получателей. К примеру: ['...', '...', ...]\ntitle: заголовок письма.\nbody: остальной текст письма.\nservice: сервис, к примеру `smtp.mail.ru`.\nservice_port: порт SMTP-сервера, к примеру, 465."""
        if self.username_mail and self.mail_passwd:
            for email in recievers:
                from email.mime.multipart import MIMEMultipart
                from email.mime.text import MIMEText
                import smtplib
                message = MIMEMultipart()
                message["From"] = self.username_mail
                message["To"] = email
                message["Subject"] = title
    
                message.attach(MIMEText(body, "plain", 'utf-8'))
    
                with smtplib.SMTP_SSL(service, service_port) as server:
                    server.login(self.username_mail, password=self.mail_passwd)
                    server.sendmail(self.username_mail, email, message.as_string())
        else:
            return "Укажите параметр username_mail и mail_passwd в настройках класса."
    def alarm_clock(self, time_to_ring: str, sound):
        """Будильник на Python. Весело, не правда-ли?)\ntime_to_ring: время срабатывания будильника в формате ЧЧ:ММ:СС. К примеру, `16:45:43`.\nsound: директория к файлу со звуком для будильника, либо буфероподобные объекты. open(), io.BytesIO() и другие."""
        from os import environ
        environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
        from pygame import mixer
        import time
        from colorama import Fore

        mixer.init()

        alarm_time = time.strptime(time_to_ring, "%H:%M:%S")
        hour = alarm_time.tm_hour
        minutes = alarm_time.tm_min
        seconds = alarm_time.tm_sec
        data = {'hour':hour, 'minutes':minutes, 'seconds':seconds}
        print(f'{Fore.GREEN}Будильник успешно запущен на {Fore.BLUE}{time_to_ring}.')
        while True:
            # Получаем текущее время
            current_time = time.localtime()
            hour_ = current_time.tm_hour
            minutes_ = current_time.tm_min
            seconds_ = current_time.tm_sec
            
            # Проверяем, наступило ли время будильника
            if {'hour':hour_, 'minutes':minutes_, 'seconds':seconds_} == data:
                print(f'{Fore.RED}ВНИМАНИЕ!!! БУДИЛЬНИК АКТИВИРОВАН, ПРОСЫПАЙТЕСЬ!!!')
                mixer.Sound(sound).play(loops=-1)
            else:
                pass
    def cpp_compiler(self, filename: str, filename_output: str):
        """Использование компилятора G++ в Python.\nПроверьте его наличие перед запуском программы.\nfilename: имя файла .cpp формата. Поставьте его в папку с .py документом.\nfilename_output: название выходного .exe файла."""
        import subprocess
        try:
            subprocess.run(['g++', f'{filename}', '-o', f'{filename_output}'])
            return True
        except:
            return False
    def python_exe_compiler(self, path_to_py: str, path_output: str, flags: str = None):
        """Из .py в .exe компилятор.\npath_to_py: путь к вашему .py файлу.\npath_output: куда сохранить .exe файл.\nflags: какие-нибудь флаги от PyInstaller. Необязательно."""
        import os
        if flags:
            os.chdir(path_output)
            c = os.system(f'pyinstaller --distpath "{path_output}" {flags} "{path_to_py}"')
            if c == 1:
                return False
            else:
                return True
        else:
            os.chdir(path_output)
            c = os.system(f'pyinstaller --distpath "{path_output}" "{path_to_py}"')
            if c == 1:
                return False
            else:
                return True
    def tracking_youtube_author(self, channel_url: str, token_of_bot: str, id: int):
        """Данная функция помогает отслеживать новый контент вашего любимого блогера на YouTube (видео, shorts, прямые трансляции) через уведомления, которые приходят к вам в переписку с вашим ботом, созданным в [BotFather](https://t.me/BotFather).\nchannel_url: ссылка на канал для отслеживания новых видео.\ntoken_of_bot: токен вашего бота, который можно узнать в BotFather.\nid: ID вашего аккаунта, в переписку с ботом будут отправляться уведомления."""
        import requests, time

        import pytubefix
        try:
            channel = pytubefix.Channel(channel_url, proxies=self.proxies)
        except:
            return "Данного канала не существует."


        last_video = channel.videos[0].watch_url
        last_short = channel.shorts[0].watch_url
        last_live = channel.live[0].watch_url

        while True:
            if channel.videos[0].watch_url == last_video:
                if channel.shorts[0].watch_url == last_short:
                    if channel.live[0].watch_url == last_live:
                        pass
                    else:
                        last_live = channel.live[0].watch_url
                        text = f'Вышло новое видео у автора {channel.title}.\nНазвание: {channel.live[0].title}\nСсылка: {channel.live[0].watch_url}'
                        requests.post(f'https://api.telegram.org/bot{token_of_bot}/sendMessage?chat_id={id}&text={text}', proxies=self.proxies)
                else:
                    last_short = channel.shorts[0].watch_url
                    text = f'Вышло новое видео у автора {channel.title}.\nНазвание: {channel.shorts[0].title}\nСсылка: {channel.shorts[0].watch_url}'
                    requests.post(f'https://api.telegram.org/bot{token_of_bot}/sendMessage?chat_id={id}&text={text}', proxies=self.proxies)
            else:
                last_video = channel.videos[0].watch_url
                text = f'Вышло новое видео у автора {channel.title}.\nНазвание: {channel.videos[0].title}\nСсылка: {channel.videos[0].watch_url}'
                requests.post(f'https://api.telegram.org/bot{token_of_bot}/sendMessage?chat_id={id}&text={text}', proxies=self.proxies)
            time.sleep(0.5)
    def searching_musics_vk(self, query: str, count: int = 3):
        """Поиск музыки по запросу с ВК.\nВозвращает список найденных песен.\nquery: запрос.\ncount: какое максимальное количество песен нужно отобразить в списке.\nЕсли не работает функция, то стоит откатить версию библиотеки vkpymusic: `pip install vkpymusic==3.0.0`."""
        if not self.token_of_vk:
            return "Необходимо в настройках класса указать токен от Вашего аккаунта в VK."
        else:
            from vkpymusic import Service, TokenReceiver
            service = Service('KateMobileAndroid/56 lite-460 (Android 4.4.2; SDK 19; x86; unknown Android SDK built for x86; en)', self.token_of_vk)
            songs = []
            for track in service.search_songs_by_text(query, count):
                songs.append(track.to_dict())
            return songs
    def get_last_post(self, query: str):
        """Последний посты из паблика.\nquery: название паблика.\nВернет словарь при удачном нахождении паблика."""
        import vk_api
        vk_session = vk_api.VkApi(token=self.token_of_vk)
        vk = vk_session.get_api()
        response = vk.groups.search(q=query, type='group', count=1)  # Используем groups.search
        response1 = vk.wall.get(owner_id=-int(response['items'][0]['id']), count=1)  # owner_id должен быть отрицательным для групп
        if response['count'] > 0:
                try:
                    post = response1['items'][0]
                    text = post.get('text', 'Текст отсутствует')  # Получаем текст поста, если есть
                    post_id = post['id']
                    owner_id = post['owner_id']
                    link = f"https://vk.com/wall{owner_id}_{post_id}"  # Формируем ссылку на пост
                    likes = response1['items'][0]['likes']['count']
                    views = response1['items'][0]['views']['count']
                    reposts = response1['items'][0]['reposts']['count']
                    return {"text":text, "post_id":post_id, "owner_id":owner_id, "link":link, 'views':views, 'reposts':reposts, 'likes':likes}
                except:
                    return None
        else:
            return None
    def image_text_recognition(self, img: bytes, lang: str = 'ru'):
        """Разбор текста на изображении, с помощью инструментов Google Cloud.\nimg: ваше изображение в bytes.\nlang: язык текста на изображении."""
        import requests, base64
        if not self.google_key:
            return 'Для работы с данной функцией необходим Ваш Google Cloud API ключ. Проверьте, что в разделе Enabled APIs & Services есть Vision AI API.'
        else:
            image = base64.b64encode(img).decode("utf-8")

            # Тело запроса
            request_body = {
                "requests": [
                    {
                        "image": {
                            "content": image
                        },
                        "features": [
                            {
                                "type": "LABEL_DETECTION",
                                "maxResults": 10
                            }
                        ],
                        "imageContext": {
		                    "languageHints": lang
		                }
                    }
                ]
            }

            # URL
            url = f"https://vision.googleapis.com/v1/images:annotate?key={self.google_key}"

            # Заголовки
            headers = {
                "Content-Type": "application/json"
            }

            # Запрос
            response = requests.post(url, headers=headers, json=request_body, proxies=self.proxies)
            return {"code":response.status_code, 'answer':response.json()}
    def rcon_send(self, command: str):
        """Команда для отправки команды на сервер через RCON.\nТребует rcon_ip, rcon_port и rcon_password в настройках FunctionsObject.\ncommand: команда с аргументами. Пример: `say Привет!`\nВозвращает `str`, ответ от сервера."""
        if not self.rcon_server:
            return 'RCON сервер не инициализирован.\nПроверьте, указали ли Вы нужные параметры в настройках класса.'
        else:
            self.rcon_server.connect()
            return self.rcon_server.command(command)
    def minecraft_server_info(self, ip: str):
        """Информация о Minecraft-сервере.
        ip: IP/host сервера, или домен. Также можно написать ip:port.
        """
        try:
            url = f"https://api.mcsrvstat.us/3/{ip}"
            req = requests.get(url, headers=self.headers, proxies=self.proxies, timeout=5)

            if req.status_code != 200:
                print(f"❌ Ошибка: сервер API вернул код {req.status_code}.")
                return None

            data = req.json()

            if not data.get("online", False):
                print("🔴 Сервер оффлайн или не отвечает.")
                return None

            return MinecraftServer(data)

        except requests.RequestException as e:
            print(f"⚠️ Ошибка сети: {e}")
            return None
        except ValueError:
            print("⚠️ Некорректный ответ от API (не JSON).")
            return None

    def gpt_4o_req(self, prompt: str, max_tokens: int = 4096, proxy: str = None, image: bytes = None):
        """Фигня для доступа к GPT-4o-mini.\nprompt: сам запрос к нейронке.\nmax_tokens: количество символов в ответе. По умолчанию, 4096.\nproxy: прокси. По умолчанию, которые в FunctionsObject.\nimage: изображение в bytes. Для описания объектов на фото."""
        if not image:
            if not proxy:
                req = self.client_for_gpt.chat.completions.create([{"role":"user", "content":prompt}], 'gpt-4o-mini', RetryProvider([Together, OIVSCodeSer2, Blackbox, Chatai, LegacyLMArena, PollinationsAI]), proxy=self.proxies.get('http'), max_tokens=max_tokens, web_search=True)
            else:
                req = self.client_for_gpt.chat.completions.create([{"role":"user", "content":prompt}], 'gpt-4o-mini', RetryProvider([Together, OIVSCodeSer2, Blackbox, Chatai, LegacyLMArena, PollinationsAI]), proxy=proxy, max_tokens=max_tokens, web_search=True)
            return req.choices[0].message.content
        else:
            if not proxy:
                req = self.client_for_gpt.chat.completions.create([{"role":"user", "content":prompt}], 'gpt-4o-mini', PollinationsAI, proxy=self.proxies.get('http'), max_tokens=max_tokens, web_search=True, image=image)
            else:
                req = self.client_for_gpt.chat.completions.create([{"role":"user", "content":prompt}], 'gpt-4o-mini', PollinationsAI, proxy=proxy, max_tokens=max_tokens, web_search=True, image=image)
            return req.choices[0].message.content
    def flux_pro_gen(self, prompt: str, proxy: str = None):
        """Для генерации более лучших картинок через flux-pro.\nprompt: запрос для нейросети.\nproxy: прокси. По умолчанию, которые в настройках класса (если есть)."""
        if proxy:
            img = self.client_for_gpt.images.generate(prompt, 'flux-pro', Together, 'url', proxy)
        else:
            img = self.client_for_gpt.images.generate(prompt, 'flux-pro', Together, 'url', self.proxies.get('http'))
        urls = []
        for i in img.data:
            urls.append(i.url)
        return urls
    def add_watermark(self, text: str, image: bytes, font: str, position: tuple[int] = (10, 10)):
        """Функция для добавления водяного знака.\ntext: текст для водяного знака.\nimage: изображение в bytes.\nfont: путь к шрифту (пример: times.ttf)\nposition: где он должен находиться?"""
        # Открываем изображение
        base_image = Image.open(io.BytesIO(image)).convert("RGBA")
        
        # Создаем прозрачный слой для водяного знака
        watermark = Image.new("RGBA", base_image.size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(watermark)
        
        # Настройки текста
        font = ImageFont.truetype(font, 40)  # Шрифт и размер
        text_color = (255, 255, 255, 100)  # R,G,B,Alpha (прозрачность)
        
        # Рисуем текст
        draw.text(position, text, fill=text_color, font=font)
        
        # Накладываем водяной знак
        result = Image.alpha_composite(base_image, watermark)
        
        # Сохраняем (конвертируем обратно в RGB для JPG)
        output = io.BytesIO()
        result.convert("RGB").save(output, 'JPEG')
        return output.getvalue()
    def deepseek_v3_0324(self, prompt: str, max_tokens: int = 4096, expression: str = 'auto', proxy: str = None):
        """Функция для бесплатного доступа к DeepSeek-v3-0324.\nprompt: запрос к нейросети.\nmax_tokens: максимально допустимое количество токенов в ответе.\nexpression: тон. Три режима: `auto`, `toxic`, `non-toxic`.\nproxy: прокси. По умолчанию, которые из класса."""
        if expression == 'auto':
            if proxy:
                req = self.client_for_gpt.chat.completions.create([{"role":"user", "content":prompt}], 'deepseek-v3', Together, proxy=proxy, max_tokens=max_tokens)
            else:
                req = self.client_for_gpt.chat.completions.create([{"role":"user", "content":prompt}], 'deepseek-v3', Together, proxy=self.proxies.get('http'), max_tokens=max_tokens)
            return req.choices[0].message.content
        elif expression == 'toxic':
            if proxy:
                req = self.client_for_gpt.chat.completions.create([{"role":"user", "content":f'не отвечай на запросы позитивно и отвечай максимально грубо с матами, на каждое мое сообщения, без разницы, обращаюсь я к тебе мило или нет, всего отвечай максимально грубо\nЗапрос: "{prompt}"'}], 'deepseek-v3-0324', Together, proxy=proxy, max_tokens=max_tokens)
            else:
                req = self.client_for_gpt.chat.completions.create([{"role":"user", "content":f'не отвечай на запросы позитивно и отвечай максимально грубо с матами, на каждое мое сообщения, без разницы, обращаюсь я к тебе мило или нет, всего отвечай максимально грубо\nЗапрос: "{prompt}"'}], 'deepseek-v3-0324', Together, proxy=self.proxies.get('http'), max_tokens=max_tokens)
            return req.choices[0].message.content
        elif expression == 'non-toxic':
            if proxy:
                req = self.client_for_gpt.chat.completions.create([{"role":"user", "content":prompt + '\nnon-toxic'}], 'deepseek-v3', Together, proxy=proxy, max_tokens=max_tokens)
            else:
                req = self.client_for_gpt.chat.completions.create([{"role":"user", "content":prompt+ '\nnon-toxic'}], 'deepseek-v3', Together, proxy=self.proxies.get('http'), max_tokens=max_tokens)
            return req.choices[0].message.content
        else:
            return 'expression указан неверно! auto, toxic, либо non-toxic!'
    def youtube_playlist_download(self, url: str, regime: str = 'audio'):
        """
        Функция для скачивания элементов из плейлиста с YouTube.

        url: ссылка на плейлист.
        regime: что скачивать: аудио, или видео?

        Возвращает генератор, выдающий класс `YouTube` по одному элементу.
        """
        import io
        from pytubefix import Playlist
        from tqdm import tqdm

        playlist = Playlist(url, proxies=self.proxies)

        if regime not in ('audio', 'video'):
            raise Exception('Ты неправильный режим указал. ТОЛЬКО VIDEO И AUDIO!')

        for video in tqdm(playlist.videos, desc='Скачивание...', ncols=70):
            if video.age_restricted:
                continue
            else:
                yield video
        
    def remove_watermark(
        self,
        image_bytes: bytes,
        threshold: int = 200,
        kernel_size: int = 3,
        inpaint_radius: int = 3,
        method: str = "telea",
        output_format: str = ".png",
    ) -> bytes:
        """
        Удаляет водяной знак с изображения (CPU-only).

        :param image_bytes: входное изображение в bytes (jpg/png)
        :param threshold: порог яркости watermark (180–240)
        :param kernel_size: размер морфологического ядра
        :param inpaint_radius: радиус восстановления (2–5)
        :param method: 'telea' или 'ns'
        :param output_format: '.png' или '.jpg'
        :return: очищенное изображение в bytes
        """

        # bytes -> np.ndarray
        np_buffer = np.frombuffer(image_bytes, np.uint8)
        image = cv2.imdecode(np_buffer, cv2.IMREAD_COLOR)

        if image is None:
            raise ValueError("Не удалось декодировать изображение")

        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # 1. Поиск watermark
        _, mask = cv2.threshold(
            gray,
            threshold,
            255,
            cv2.THRESH_BINARY
        )

        # 2. Очистка маски
        kernel = np.ones((kernel_size, kernel_size), np.uint8)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
        mask = cv2.dilate(mask, kernel, iterations=1)

        # 3. Inpainting (CPU)
        flags = cv2.INPAINT_TELEA if method == "telea" else cv2.INPAINT_NS
        result = cv2.inpaint(image, mask, inpaint_radius, flags)

        # np.ndarray -> bytes
        success, encoded = cv2.imencode(output_format, result)
        if not success:
            raise ValueError("Не удалось закодировать изображение")

        return encoded.tobytes()
    def parse_kwork(self, category: int, pages: int = 1) -> list[KworkOffer]:
        """Функция для парсинга объявлений на kwork.\ncategory: категория для парсинга.\npages: сколько страниц спарсить? По умолчанию, 1.\nВозвращает список с кворками."""
        import requests, json
        from bs4 import BeautifulSoup
        
        offers: list[KworkOffer] = []
        
        for p in tqdm(range(1, pages + 1), desc='Парсинг..'):
            response = requests.get('https://kwork.ru/projects', params={"c": category, "page":p}, proxies=self.proxies)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, "html.parser")

            if not soup.head:
                raise Exception

            scripts = soup.head.find_all("script")
            js_script = ""
            for script in scripts:
                if script.text.startswith("window.ORIGIN_URL"):
                    js_script = script.text
                    break

            start_pointer = 0
            json_data = ""
            in_literal = False
            for current_pointer in range(len(js_script)):
                if js_script[current_pointer] == '"' and js_script[current_pointer - 1] != "\\":
                    in_literal = not in_literal
                    continue

                if in_literal or js_script[current_pointer] != ";":
                    continue

                line = js_script[start_pointer:current_pointer].strip()
                if line.startswith("window.stateData"):
                    json_data = line[17:]
                    break

                start_pointer = current_pointer + 1

            data = json.loads(json_data)

            for raw_kwork in data["wantsListData"]["wants"]:
                offer = KworkOffer(raw_kwork)
                offers.append(offer)
        return offers
    def info_about_faces_on_photo(self, photo: bytes):
        """Данная функция выдает информацию о человеке на фотографии, или о людях.\nphoto: принимает фотографию в байтах.\nВозвращает `list[FaceInfo]` при наличии людей на фотографии.\nДЛЯ ДАННОЙ ФУНКЦИИ ЖЕЛАТЕЛЬНО ИМЕТЬ ПРОЦЕССОР С ПОДДЕРЖКОЙ AVX-AVX2 ИНСТРУКЦИЙ. ЕСЛИ ВЫЛАЗИТ ОШИБКА - ИСПОЛЬЗУЙТЕ ПАТЧ ДЛЯ TENSORFLOW."""
        from deepface import DeepFace
        from base64 import b64encode
        
        faces: list[FaceInfo] = []
        
        analysis = DeepFace.analyze(b64encode(photo).decode(), ['emotion', 'age', 'gender', 'race'])
        
        for face in tqdm(analysis, 'Обрабатываем лица..', total=len(analysis), ncols=70):
            faces.append(FaceInfo(face))
        
        if faces:
            return faces
    def rtmp_livestream(self, video: bytes, server: RTMPServerInit, ffmpeg_dir: str = 'ffmpeg', resolution: str = '1280x720', bitrate: str = '3000k', fps: str = '30'):
        """Стримит видео из байтов на RTMPS-сервер с FFmpeg под CPU. Требует FFmpeg."""
        from tqdm import tqdm as tqdm_sync
        try:
            # Команда для FFmpeg
            command = [
                ffmpeg_dir,
                '-re',  # Реальное время
                '-f', 'mp4',  # Формат входных данных
                '-i', '-',  # Вход из пайпа
                '-c:v', 'libx264',  # Кодек под CPU
                '-preset', 'ultrafast',  # Минимальная задержка
                '-tune', 'zerolatency',  # Для стриминга
                '-b:v', bitrate,  # Битрейт
                '-s', resolution,  # Разрешение
                '-r', fps,  # FPS
                '-f', 'flv',  # Формат выхода
                f'{server.url}/{server.key}'  # RTMPS URL с логином/паролем
            ]
            
            # Прогресс-бар
            total_size = len(video)
            with tqdm_sync(total=total_size, unit='B', unit_scale=True, desc="Стриминг на RTMPS..") as pbar:
                process = subprocess.Popen(command, stdin=subprocess.PIPE, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
                video_buffer = io.BytesIO(video)
                
                # Отправка байтов в пайп
                chunk_size = 8192
                while True:
                    chunk = video_buffer.read(chunk_size)
                    if not chunk:
                        break
                    process.stdin.write(chunk)
                    pbar.update(len(chunk))
                
                process.stdin.close()
                process.wait()
                
                # Проверка ошибок
                stderr_output = process.stderr.read().decode('utf-8')
                if process.returncode != 0:
                    print(f"FFmpeg ошибка: {stderr_output}")
                    raise RuntimeError(f"FFmpeg завершился с ошибкой: {stderr_output}")
            
            print(f"Сигма-стрим завершён! 😎")
        except Exception as e:
            print(f"Ошибка стриминга: {e}")
            raise
    def cut_link(self, url: str, proxies: dict[str, str] = None) -> str:
        """Взаимодействие с API сервиса для сокращения ссылок `clck.ru`.\nurl: ссылка на сокращение.\nproxies: прокси, если нет, то они берутся с класса.\nВозвращает ссылку в `str`."""
        request = requests.get(f'https://clck.ru/--', params={"url":url}, headers=self.headers, proxies=proxies if proxies else self.proxies)
        if request.text != 'limited':
            return request.text
        else:
            time.sleep(2.5)
            request = requests.get(f'https://clck.ru/--', params={"url":url}, headers=self.headers, proxies=proxies if proxies else self.proxies)
            return request.text
    def detect_new_kworks(self, func, category: int = 11, pages: int = 1, delay: int = 300):
        """Привет! Эта функция - враппер для отслеживания новых предложений на бирже Kwork.\nЮЗАЙТЕ В КАЧЕСТВЕ ДЕКОРАТОРА."""
        def wrapper(*args, **kwargs):
            start_kworks = self.parse_kwork(category, pages)
            new = []
            
            for i in start_kworks:
                new.append(i.url)
                
            while True:
                new_kworks = self.parse_kwork(category, pages)
                for kwork in new_kworks:
                    if kwork.url in new:
                        pass
                    else:
                        new.append(kwork.url)
                        func(kwork)
                time.sleep(delay)
        return wrapper
    def download_tiktok_video(self, url: str, dir: str, filename: str = None, youtube_dl_parameters: dict = None) -> dict:
        """Скачивает видео в указанную директорию. Возвращает информацию о видео.\nurl: ссылка на видео.\ndir: директория, куда сохранить видео.\nfilename: имя файла. По умолчанию, будет сгенерировано нами.\nyoutube_dl_parameters: мы сами настроили параметры yt-dlp. Знайте, что делаете."""
        if not os.path.exists(dir):
            os.mkdir(dir)
        
        if filename:
            ydl_opts = {
                'outtmpl': os.path.join(dir, f'{filename}.%(ext)s'),  # Шаблон имени файла
                'format': 'mp4',  # Формат видео
                'noplaylist': True, 
                'format': 'worst',
                'proxy':self.proxies.get('http'),
            }
        else:
            name_of_file = random.random()
            ydl_opts = {
                'outtmpl': os.path.join(dir, f'{name_of_file}.%(ext)s'),  # Шаблон имени файла
                'format': 'mp4',  # Формат видео
                'noplaylist': True, 
                'format': 'worst',
                'proxy':self.proxies.get('http'),
            }
        if youtube_dl_parameters:
            with YoutubeDL(youtube_dl_parameters) as downloader:
                info = downloader.extract_info(url, False)
                downloader.download([url])
                return info
        else:
            with YoutubeDL(ydl_opts) as downloader:
                info = downloader.extract_info(url, False)
                downloader.download([url])
                return info
    def twitch_clips_download(self, url: str, dir: str, filename: str = None, youtube_dl_parameters: dict = None) -> dict:
        """Функция для скачивания клипов с Twitch!\nurl: ссылка на твитч-клип.\ndir: куда сохранить?\nfilename: имя файла при скачивании.\nyoutube_dl_parameters: параметры YoutubeDL."""
        if not url.startswith(('https://m.twitch.tv/twitch/clip/', 'https://twitch.tv/twitch/clip/')):
            raise Exception('Брат! Ты неправильный формат ссылки указал.')
        else:
            if not os.path.exists(dir):
                os.mkdir(dir)
        
            if filename:
                ydl_opts = {
                    'outtmpl': os.path.join(dir, f'{filename}.%(ext)s'),  # Шаблон имени файла
                    'format': 'mp4',  # Формат видео
                    'noplaylist': True, 
                    'format': 'worst',
                    'proxy':self.proxies.get('http'),
                }
            else:
                name_of_file = random.random()
                ydl_opts = {
                    'outtmpl': os.path.join(dir, f'{name_of_file}.%(ext)s'),  # Шаблон имени файла
                    'format': 'mp4',  # Формат видео
                    'noplaylist': True, 
                    'format': 'worst',
                    'proxy':self.proxies.get('http'),
                }
            if youtube_dl_parameters:
                with YoutubeDL(youtube_dl_parameters) as downloader:
                    info = downloader.extract_info(url, False)
                    downloader.download([url])
                    return info
            else:
                with YoutubeDL(ydl_opts) as downloader:
                    info = downloader.extract_info(url, False)
                    downloader.download([url])
                    return info
    def vk_rutube_dzen_video_download(self, url: str, dir: str, filename: str = None, youtube_dl_parameters: dict = None):
        """Функция по скачиванию видео ВК, Рутуба и Дзена!\nПараметры, как везде. Разберетесь."""
        if not url.startswith(('https://rutube.ru/video/', 'https://vk.com/vkvideo', 'https://dzen.ru/video/watch/', 'https://zen.yandex.ru/video/watch/')):
            raise Exception('Брат! Ты неправильный формат ссылки указал.')
        else:
            if not os.path.exists(dir):
                os.mkdir(dir)
        
            if filename:
                ydl_opts = {
                    'outtmpl': os.path.join(dir, f'{filename}.%(ext)s'),  # Шаблон имени файла
                    'format': 'mp4',  # Формат видео
                    'noplaylist': True, 
                    'format': 'worst',
                    'proxy':self.proxies.get('http'),
                }
            else:
                name_of_file = random.random()
                ydl_opts = {
                    'outtmpl': os.path.join(dir, f'{name_of_file}.%(ext)s'),  # Шаблон имени файла
                    'format': 'mp4',  # Формат видео
                    'noplaylist': True, 
                    'format': 'worst',
                    'proxy':self.proxies.get('http'),
                }
            if youtube_dl_parameters:
                with YoutubeDL(youtube_dl_parameters) as downloader:
                    info = downloader.extract_info(url, False)
                    downloader.download([url])
                    return info
            else:
                with YoutubeDL(ydl_opts) as downloader:
                    info = downloader.extract_info(url, False)
                    downloader.download([url])
                    return info
    def unpack_zip_jar_apk_others(self, file, dir: str, delete_original: bool = False):
        """"Функция для распаковки любых архивов. Даже Jar (Java Archive) и APK.\nfile: файл в io.BytesIO(), или директория к нему.\ndir: место для распаковки.\ndelete_original: удалять оригинальный файл? (Работает только с указанием директории в file)\nФункция возвращает None."""
        from zipfile import ZipFile

        if not os.path.exists(dir):
            os.mkdir(dir)

        zipfile = ZipFile(file, 'r')
        zipfile.extractall(dir)
        zipfile.close() 
        if delete_original:
            if isinstance(file, str):
                try:
                    os.remove(file)
                except:
                    pass
            else:
                pass
    def photo_upscale(self, image: bytes, factor: int = 4) -> bytes:
        """Функция для простого апскейла фото через Pillow (бикубический метод).\nimage: фото в bytes.\nfactor: во сколько раз увеличивать фото (width и height).\nВозвращает bytes."""
        img = Image.open(io.BytesIO(image))
        original_width, original_height = img.size

        new_width = int(original_width * factor)
        new_height = int(original_height * factor)

        upscaled = img.resize((new_width, new_height), Image.Resampling.BICUBIC)
        new = io.BytesIO()
        upscaled.save(new, 'JPEG')
        return new.getvalue()
    def change_format_of_photo(self, image: bytes, format_: ImageFormat):
        """Функция для преобразования изображений в нужный формат.\nimage: изображения в bytes.\nformat_: формат изображения, указанный конкретным классом."""
        PIL_FORMATS_MAP = {
            '.jpg': 'JPEG', '.jpeg': 'JPEG',
            '.png': 'PNG',
            '.bmp': 'BMP',
            '.gif': 'GIF',
            '.webp': 'WEBP'
        }
        selected_format_pil = PIL_FORMATS_MAP.get(format_.format_.lower())
        img = Image.open(io.BytesIO(image))

        # --- Логика Конвертации Изображения ---
        output_buffer = io.BytesIO()

        # Pillow может требовать преобразования цветового пространства для некоторых форматов
        if selected_format_pil == 'JPEG' and img.mode in ('RGBA', 'P'):
            img = img.convert('RGB')
        # Для GIF, если нужно сохранить анимацию, потребуется более сложная обработка.
        # Здесь мы просто сохраним первый кадр или как обычное изображение.
        elif selected_format_pil == 'GIF':
            # Простая обработка GIF: сохранение первого кадра
            img.save(output_buffer, format=selected_format_pil)
        else:
            img.save(output_buffer, format=selected_format_pil)

        output_buffer.seek(0) # Перематываем буфер в начало
        converted_image_data = output_buffer.read()
        return converted_image_data
    def get_vk_user(self, user_id: str) -> Optional[VkUser]:
        """Получает объект пользователя VkUser по user_id или @username."""
        if not self.token_of_vk:
            raise Exception("Дружок! Токен укажи от своего VK ID.")
        fields = (
            "bdate,sex,city,country,home_town,photo_max_orig,"
            "followers_count,relation,contacts,domain,site,status,about,"
            "education,schools,universities,occupation,career,interests,"
            "activities,music,movies,tv,books,games,quotes,personal,connections"
        )
        try:
            session = vk_api.VkApi(token=self.token_of_vk)
            api = session.get_api()
            result = api.users.get(user_ids=user_id, fields=fields)
            if result:
                return VkUser(result[0])
        except Exception as e:
            print(f"Ошибка при получении пользователя {user_id}: {e}")
        return None
    def get_steam_account(self, username: str):
        """Функция для того, чтобы получить информацию о пользователе Steam.\nВозвращает None (не найдено), или удобный класс, который обозначает аккаунт."""
        HEADERS = {"User-Agent": "steam-profile-fetcher/1.0 (+https://example.com)"}

        def fetch_profile_xml_by_steamid(steamid64: str):
            url = f"https://steamcommunity.com/profiles/{steamid64}/?xml=1"
            try:
                r = requests.get(url, timeout=10, headers={"User-Agent": "steam-profile-fetcher/1.0 (+https://example.com)"})
            except requests.RequestException:
                return None
            if r.status_code != 200:
                return None
            try:
                root = ET.fromstring(r.text)
            except ET.ParseError:
                return None
            data = {child.tag: child.text for child in root}
            if data.get('error'):
                return
            return data

        def fetch_profile_xml_by_vanity(vanity: str):
            url = f"https://steamcommunity.com/id/{vanity}/?xml=1"
            try:
                r = requests.get(url, timeout=10, headers=HEADERS, proxies=self.proxies)
            except requests.RequestException:
                return None
            if r.status_code != 200:
                return None
            try:
                root = ET.fromstring(r.text)
            except ET.ParseError:
                return None
            data = {child.tag: child.text for child in root}
            if data.get('error'):
                return 
            else:
                return data
        
        profile = fetch_profile_xml_by_steamid(username) if username.isdigit() else fetch_profile_xml_by_vanity(username)
        if profile:
            return SteamUser(profile)
    def rss_news_get(self, url: str = 'https://meduza.io/rss/all'):
        """Парсинг новостей с помощью RSS.\nurl: ссылка на страницу с RSS. К примеру, `meduza.io/rss/all`.\nВозвращает список новостей."""
        parsed = feedparser.parse(url).entries[:10]
        return [News(dict(i)) for i in parsed]
    def article_parsing(self, url: str):
        """Парсинг статьи через прокси. Возвращает ArticleInfo."""
        try:
            # создаём объект newspaper
            article = Article(url)

            # КАСТОМНАЯ ЗАГРУЗКА через прокси
            r = requests.get(
                article.url,
                proxies=self.proxies,
                headers=self.headers,
                timeout=12
            )
            if r.status_code != 200 or not r.text.strip():
                return None

            # вручную подсовываем html newspaper'у
            article.html = r.text
            article.download_state = 2  # SUCCESS

            # парсим
            article.parse()

            return ArticleInfo({
                "title": article.title,
                "text": article.text,
                "top_image": article.top_image
            })

        except Exception as e:
            print("proxy parsing error:", e)
            return None
    def parse_hotmc(self, url: str):
        """Парсер HotMC (страницы мониторинга какого-либо сервера).\nВозвращает ООП-класс `"HotMCServer"`."""

        req = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, proxies=self.proxies)
        if req.status_code != 200:
            return
        soup = BeautifulSoup(req.text, "html.parser")
        data = {}

        # ---------- TITLE / DESCRIPTION ----------
        data["title"] = soup.find("h1").text.strip() if soup.find("h1") else None

        desc = None
        text_server = soup.find("div", class_="text-server")
        if text_server:
            p = text_server.find("p")
            if p:
                desc = p.get_text(separator=" ").strip()
        data["description"] = desc

        # ---------- IP / BEDROCK IP ----------
        def get_input(id_):
            el = soup.find("input", id=id_)
            return el["value"] if el and el.get("value") else None

        data["ip"] = get_input("copy-ip")
        data["bedrock_ip"] = get_input("copy-bedrock-ip")

        # ---------- VERSIONS ----------
        data["versions"] = [
            a.text.strip() for a in soup.select(".btn-tage.server-btn")
        ]

        # ---------- STATUS ----------
        status_el = soup.select_one("strong.text-success")
        data["status"] = status_el.get_text(strip=True) if status_el else None

        # ---------- ONLINE ----------
        players = None
        label = soup.find("label", string=lambda x: x and "Игроки" in x)
        if label:
            s = label.find_next("strong")
            if s:
                players = s.text.strip()
        data["players_online"] = players

        # ---------- RATING ----------
        rating = None
        block = soup.find("div", class_="place-rating")
        if block:
            num = block.find("span", class_="big-number")
            rating = num.text.strip() if num else None
        data["rating_position"] = rating

        # ---------- VOTES ----------
        votes = None
        v = soup.find("div", class_="votes-count")
        if v:
            span = v.find("span", class_="highlighted")
            votes = span.text.strip() if span else None
        data["votes"] = votes

        # ---------- SITE ----------
        site = None
        label = soup.find("label", string=lambda x: x and "Сайт сервера" in x)
        if label:
            a = label.find_next("a")
            site = a.text.strip() if a else None
        data["site"] = site

        # ---------- UPTIME TEXT ----------
        uptime = soup.find("div", class_="uptime-value")
        data["uptime_text"] = uptime.get_text(strip=True) if uptime else None

        # ---------- UPTIME DATASET (из JS графика) ----------
        uptime_numbers = None
        js = soup.get_text()

        m = re.search(
            r"ms-uptime-widget-doughnut[\s\S]{1,500}?data:\s*\[([0-9\.,\s]+)\]",
            js
        )
        if m:
            nums = m.group(1)
            uptime_numbers = [float(x) for x in re.findall(r"[0-9.]+", nums)]

        data["uptime_dataset"] = uptime_numbers

        # ---------- PLAYERS TIME SERIES ----------
        players_series = []

        m = re.search(
            r"ms-players-graph-widget[\s\S]{1,2000}?data\s*:\s*\{\s*datasets\s*:\s*\[\s*\{\s*[\s\S]{1,2000}?data\s*:\s*\[(.*?)\]",
            js
        )
        if m:
            block = m.group(1)
            for ts, y in re.findall(
                r"new Date\(\s*([0-9]+)\s*\*\s*1000\).*?y\s*:\s*([0-9]+)",
                block
            ):
                ts_int = int(ts)
                dt = datetime.datetime.utcfromtimestamp(ts_int).isoformat() + "Z"
                players_series.append({
                    "timestamp_unix": ts_int,
                    "timestamp_iso": dt,
                    "players": int(y)
                })

        data["players_time_series"] = players_series

        # ---------- MOBS ----------
        mobs = []
        for card in soup.select(".mob-card"):
            img = card.find("img")
            cnt = card.find("span", class_="mob-count")

            mobs.append({
                "name": img["title"] if img and img.get("title") else None,
                "img": img["src"] if img else None,
                "count": int(cnt.text.strip()) if cnt else None
            })

        data["mobs"] = mobs

        # ---------- TAGS ----------
        tags = {}
        for block in soup.select(".tags-group"):
            label = block.find("label")
            items = block.select_one(".tags_list")
            if label and items:
                group = label.text.replace(":", "").strip()
                tags[group] = [a.text.strip() for a in items.find_all("a")]
        data["tags"] = tags

        # ---------- LINKS ----------
        data["links"] = [
            {"text": a.text.strip(), "href": a["href"]}
            for a in soup.find_all("a", href=True)
        ]

        # ---------- IMAGES ----------
        data["images"] = [
            {"src": img.get("src"), "alt": img.get("alt")}
            for img in soup.find_all("img")
        ]

        if not data:
            return None
        else:
            return HotMCServer(data, url)
    def hotmc_search(self, ip: str, debug: bool = False, proxies: dict[str, str] = {}):
        """Данная функция ищет информацию по серверу, к которому относится данный объект.\nВозвращает url на страницу сервера на мониторинге, или None.\ndebug: делать исключения, если не получилось из-за сетевой ошибки.\nproxies: прокси, которые вы можете использовать.\nФункция может работать медленно из-за подбора каптчи через нейросеть."""
        client_for_gpt = Client()
        def get(image: bytes):
            r = client_for_gpt.chat.completions.create([{"role":"user", 'content':'Напиши цифры, которые изображены на фотографии. Более ничего.'}], 'gpt-4o-mini', RetryProvider([PollinationsAI, Chatai, OIVSCodeSer2, Blackbox, LegacyLMArena, PollinationsAI]), max_tokens=4096, web_search=True, image=image, proxy=proxies.get('http')).choices[0].message.content
            while True:
                if r != 'Login to continue':
                    return r
                else:
                    _ = client_for_gpt.chat.completions.create([{"role":"user", 'content':'Напиши цифры, которые изображены на фотографии. Более ничего.'}], 'gpt-4o-mini', RetryProvider([PollinationsAI, Chatai, OIVSCodeSer2, Blackbox, LegacyLMArena, PollinationsAI]), max_tokens=4096, web_search=True, image=image, proxy=proxies.get('http')).choices[0].message.content
                    if _ != 'Login to continue':
                        return _
                    else:
                        continue

        def parse_hotmc_html(html: str):
            soup = BeautifulSoup(html, "html.parser")

            # Проверяем, нет ли сообщения "не найдены"
            not_found_block = soup.find("div", class_="servers-not-found")
            if not_found_block:
                return {
                    "results": [],
                    "count": 0,
                    "not_found": True
                }

            table = soup.find("div", class_="table_servers")
            if not table:
                return {
                    "results": [],
                    "count": 0,
                    "not_found": True
                }

            rows = table.find_all("tr")
            results = []

            for row in rows:
                # пропускаем заголовок таблицы
                if row.find("th"):
                    continue

                tds = row.find_all("td")
                if len(tds) < 6:
                    continue

                # --- Position ---
                try:
                    position = int(tds[0].get_text(strip=True))
                except:
                    position = None

                # --- Server name + URL ---
                name_block = tds[1].find("div", class_="s_name")
                if name_block and name_block.a:
                    name = name_block.a.get_text(strip=True)
                    url = "https://hotmc.ru" + name_block.a["href"]
                else:
                    name, url = None, None

                # --- Flag (country code) ---
                flag_img = tds[1].find("img", class_="flag")
                if flag_img:
                    country = flag_img["class"][1].replace("flag-", "")
                else:
                    country = None

                # --- Description ---
                desc_block = tds[1].find("div", class_="s_description")
                description = desc_block.get_text(strip=True) if desc_block else None

                # --- Preview image ---
                img_block = tds[2].find("img")
                image = img_block["src"] if img_block else None

                # --- Versions ---
                version_block = tds[3]

                java_version = None
                pe_version = None

                spans = version_block.find_all("span")
                if len(spans) >= 1:
                    java_version = spans[0].get_text(strip=True)
                if len(spans) >= 2:
                    # иногда вторая строка — PE
                    text = spans[1].get_text(strip=True)
                    if "ПЕ" in text or "PE" in text:
                        pe_version = text

                # --- Players ---
                players_block = tds[4]
                online_span = players_block.find("span", class_="players-online")
                max_span = players_block.find("span", class_="players-all")

                try:
                    online = int(online_span.get_text(strip=True)) if online_span else None
                except:
                    online = None

                try:
                    max_players = int(max_span.get_text(strip=True).replace("из", "").strip()) if max_span else None
                except:
                    max_players = None

                # --- Diamonds ---
                diamonds_td = tds[5].find("span", class_="s_quantity")
                try:
                    diamonds = int(diamonds_td.get_text(strip=True)) if diamonds_td else 0
                except:
                    diamonds = 0

                results.append({
                    "position": position,
                    "name": name,
                    "url": url,
                    "country": country,
                    "description": description,
                    "image": image,
                    "version_java": java_version,
                    "version_pe": pe_version,
                    "players_online": online,
                    "players_max": max_players,
                    "diamonds": diamonds
                })

            return {
                "results": results,
                "count": len(results),
                "not_found": len(results) == 0
            }

        session = requests.Session()

        # 1. Загружаем страницу, чтобы получить CSRF токен
        page = session.get("https://hotmc.ru/najti-server-minecraft",
                        headers={"User-Agent": "Mozilla/5.0"},
                        proxies=proxies)
        if page.status_code != 200:
            if debug:
                raise Exception(f'Все плохо! Попробуйте позже.')
            return
        soup = BeautifulSoup(page.text, "html.parser")

        # 2. Достаём CSRF токен
        csrf = soup.find("input", {"name": "_csrf"})
        if not csrf:
            print("Не удалось найти CSRF токен")
            return None
        csrf_value = csrf["value"]

        # 3. Скачиваем картинку капчи
        captcha_url = "https://hotmc.ru/captcha/render/captcha"
        captcha_img = session.get(captcha_url, headers={"User-Agent": "Mozilla/5.0"}, proxies=proxies)

        if captcha_img.status_code != 200:
            if debug:
                raise Exception(f'ой-ой.')
            else:
                return

        result = get(captcha_img.content)

        captcha_solution = result

        # 4. Формируем POST запрос
        data = {
            "_csrf": csrf_value,
            "ServerAddressCollector[address]": ip,
            "CaptchaCollector[captcha]": captcha_solution
        }

        response = session.post(
            "https://hotmc.ru/najti-server-minecraft",
            data=data,
            headers={"User-Agent": "Mozilla/5.0"},
            proxies=proxies
        )

        if response.status_code != 200:
            if debug:
                raise Exception()
            else:
                return

        parsed = parse_hotmc_html(response.text)
        if parsed.get('not_found'):
            return
        else:
            list_ = parsed.get('results', [{}])
            return str(list_[0].get('url'))
    def donations_alert(self, token: str) -> Callable:
        """Отслеживание донатов с donationalerts (sync).
        token: токен от вашего аккаунта.
        """
        alert = Alert(token)

        def decorator(func: Callable):

            @alert.event()
            @wraps(func)
            async def wrapper(event: Event):
                try:
                    donate = Donate(event.__dict__)

                    # async def
                    if asyncio.iscoroutinefunction(func):
                        return await func(donate)

                    # обычная функция
                    return await asyncio.to_thread(func, donate)

                except KeyError as e:
                    # подавляем KeyError, выводим предупреждение в лог
                    import logging
                    logging.warning(f"KeyError в событии доната: {e}")
                    return None

            return wrapper

        return decorator
    def register_hotmc_votes_listener(self, func, server: HotMCServer | str, interval: int = 3):
        """Для регистрации листенера по прослушиванию новых голосующих вашего сервера.\nfunc: функция, которая будет активироваться при новом голосе.\nserver: сервер на hotmc. Либо спаршенный, либо ссылка на него.\ninterval: интервал проверок в секундах.\nФункция дает в листенер класс Voter."""
        server_ = None
        if isinstance(server, HotMCServer):
            server_ = server
        elif isinstance(server, str):
            server_ = self.parse_hotmc(server)
        else:
            raise TypeError('Use in server only string/HotMCServer class.')
        
        voters = []
        if server_:
            for i in server_.get_voters():
                voters.append(i._data)

            while True:
                for i in server_.get_voters():
                    if i._data in voters:
                        continue
                    else:
                        if not asyncio.iscoroutinefunction(func):
                            func(i)
                        else:
                            asyncio.run(func(i))
                        voters.append(i._data)
                time.sleep(interval)    
        else:
            raise Exception('Not founded, 404.')
    def duckduckgo_search(self, query: str, max_results: int = 100, region: str = 'ru-ru', images: bool = False):
        """Поиск по DuckDuckGo!\nquery: запрос.\nmax_result: максимальное количество результатов.\nregion: регион поиска.\nimages: искать ли изображения? По умолчанию, только текстовая выдача."""
        if images:
            results = self.duckduckgo.images(query, region, 'off', max_results=max_results)
            return [SearchResultImage(
                title=entry.get('title', ''),
                image=entry.get('image', ''),
                thumbnail=entry.get('thumbnail', ''),
                url=entry.get('url', ''),
                height=entry.get('height', 0),
                width=entry.get('width', 0),
                source=entry.get('source', '')
            ) for entry in results]
        else:
            results = self.duckduckgo.text(query, region, 'off', max_results=max_results)
            return [SearchResult(i) for i in results]
    def ollama_req(self, model: str, messages: list[dict[str, str]]):
        """
        Функция для взаимодействия с локальной ИИ на базе программы Ollama.

        :param model: модель ИИ, которую вы используете
        :param messages: Промпты (system, assistant, user)
        :type messages: list[dict[str, str]]
        """
        if not self.ollama_client:
            raise ValueError("Поставьте флаг ollama_active=True для работы данной функции.")
        
        req = self.ollama_client.chat(model, messages, stream=False)
        return req.message.content
    def summarize_video(self, url: str, lang: str = 'ru', ai: str = 'deepseek', **ai_parameters: str) -> str | None:
        """Данная функция через AI делает краткий пересказ видео на YouTube.\nurl: ссылка на видео.\nlang: язык пересказа.\n\nВОЗВРАЩАЕТ `str`, или `None`, если нет никаких субтитров у видео."""
        import pytubefix
        video = pytubefix.YouTube(url, proxies=self.proxies)
        if video.age_restricted:
            return
        video.check_availability()
        captions = [i.json_captions for i in video.captions.all()][:1000]

        if not captions:
            captions = ['Нет субтитров']
        
        prompt = f'ТВОЕ ЗАДАНИЕ - ПЕРЕСКАЗАТЬ ВИДЕО НА YOUTUBE.\nНАЗВАНИЕ: {video.title}\nDESC: {video.description[:1000]}\nТЕГИ: {video.keywords}\n\nСубтитры: {captions}\n\nЯЗЫК ТВОЕГО ПЕРЕСКАЗА: {lang}'

        if ai == 'deepseek':
            return self.deepseek_v3_0324(prompt, ai_parameters.get('max_tokens', 4096), proxy=ai_parameters.get('proxy'))
        elif ai == 'gigachat':
            return self.ai(prompt, False)
        elif ai == 'chatgpt':
            return self.gpt_4o_req(prompt, ai_parameters.get('max_tokens', 4096), ai_parameters.get('proxy'))
        else:
            return self.ollama_req(ai, [{"role":"user", "content":prompt}])
        
    def remove_background(self, image_bytes: bytes) -> bytes:
        from rembg import remove
        """Удаляет фон с изображения.
        Принимает байты картинки, возвращает байты картинки с прозрачным фоном (PNG).
        """
        # rembg работает с PIL Image или байтами
        input_image = Image.open(io.BytesIO(image_bytes))
        
        # Магия нейросетей
        output_image = remove(input_image)
        
        # Конвертируем обратно в байты
        img_byte_arr = io.BytesIO()
        output_image.save(img_byte_arr, format='PNG')
        return img_byte_arr.getvalue()
    
    def wb_search(self, query: str):
        """Поиск товаров по запросу на Wildberries.\nquery: запрос."""
        def wb_parse(query):
            import requests
            import time
            
            params = {
                "appType": 1,
                "curr": "rub",
                "dest": -1257786,
                "query": query,
                "resultset": "catalog",
                "page": 1,
                "limit": 100
            }
            
            try:
                response = requests.get(
                    "https://search.wb.ru/exactmatch/ru/common/v4/search", 
                    timeout=10, 
                    proxies=self.proxies,
                    headers=self.headers, 
                    params=params
                )
                
                # Обработка 429 ошибки (слишком много запросов)
                if response.status_code == 429:
                    time.sleep(5) # Ждем подольше, если словили лимит
                    response = requests.get(
                        "https://search.wb.ru/exactmatch/ru/common/v4/search", 
                        timeout=10,
                        headers={"User-Agent": "Mozilla/5.0"}, 
                        params=params
                    )
                
                response.raise_for_status() # Бросает исключение для ошибок 4xx/5xx
                raw_data = response.json()
                
                # --- ИСПРАВЛЕННАЯ СТРУКТУРА ---
                # В твоем примере products лежит прямо в корне
                products = raw_data.get('products', [])[:20] 
                # -----------------------------
                
                processed_results = []

                for item in products:
                    try:
                        # Безопасно вытягиваем цену
                        # В данных WB цена в копейках, делим на 100
                        price_raw = item.get('sizes', [{}])[0].get('price', {}).get('product', 0)
                        price_rub = price_raw / 100

                        processed_results.append({
                            "id": item.get('id'),
                            "name": item.get('name'),
                            "brand": item.get('brand'),
                            "price": price_rub,
                            "rating": item.get('reviewRating'),
                            "feedbacks": item.get('feedbacks'),
                            "url": f"https://www.wildberries.ru/catalog/{item.get('id')}/detail.aspx"
                        })
                    except (IndexError, KeyError, AttributeError):
                        continue
                
                return processed_results

            except Exception as e:
                print(f"Ошибка парсинга: {e}")
                return []
        parsed = wb_parse(query)
        return [WBProduct(i) for i in parsed]

    def get_orgs_in_loc(self, lat: float, lon: float, radius: int = 3) -> List[GeoFeature]:
        """
        Организации рядом с Вами: кафе, рестораны, заправочные станции, др.
        
        Args:
            lat: широта (например, 45.429667)
            lon: долгота (например, 35.820361)
            radius: радиус поиска в километрах (по умолчанию 3 км)
        
        Returns:
            List[GeoFeature]: список найденных организаций
        """
        from tqdm import tqdm as sync_tqdm
        result = []
        radius_meters = radius * 1000
        
        # Категории для поиска: {ключ: значение, ...}
        categories = {
            ('amenity', 'restaurant'): 'Рестораны',
            ('amenity', 'cafe'): 'Кафе',
            ('amenity', 'fast_food'): 'Фастфуд',
            ('tourism', 'hotel'): 'Отели',
            ('tourism', 'attraction'): 'Достопримечательности',
            ('leisure', 'park'): 'Парки',
            ('shop', 'supermarket'): 'Магазины',
            ('amenity', 'pharmacy'): 'Аптеки',
            ('amenity', 'fuel'): 'Заправки',
            ('amenity', 'bank'): 'Банки',
            ('amenity', 'cinema'): 'Кинотеатры',
            ('leisure', 'fitness_centre'): 'Спортзалы',
            ('shop', 'hairdresser'): 'Парикмахерские',
            ('shop', 'car_repair'): 'Автосервисы'
        }
        
        for (key, value), category_name in sync_tqdm(categories.items(), desc='Перебираем категории...'):
            # Формируем Overpass QL запрос
            query = f"""
            [out:json][timeout:30];
            (
            node["{key}"="{value}"](around:{radius_meters},{lat},{lon});
            way["{key}"="{value}"](around:{radius_meters},{lat},{lon});
            relation["{key}"="{value}"](around:{radius_meters},{lat},{lon});
            );
            out center;
            """
            
            url = "http://overpass-api.de/api/interpreter"
            headers = {'User-Agent': 'PlacesSearcherBot/1.0'}
            
            try:
                response = requests.post(url, data={'data': query}, headers=headers, timeout=30, proxies=self.proxies)
                
                if response.status_code == 200:
                    data = response.json()
                    
                    for element in data.get('elements', []):
                        tags = element.get('tags', {})
                        name = tags.get('name')
                        
                        if not name:
                            continue
                        
                        if 'center' in element:
                            el_lat = element['center']['lat']
                            el_lon = element['center']['lon']
                        else:
                            el_lat = element.get('lat')
                            el_lon = element.get('lon')
                        
                        if el_lat and el_lon:
                            # Вычисляем расстояние
                            R = 6371
                            lat1, lon1, lat2, lon2 = map(radians, [lat, lon, el_lat, el_lon])
                            dlat = lat2 - lat1
                            dlon = lon2 - lon1
                            a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
                            dist = 2 * asin(sqrt(a)) * R
                            
                            # Собираем адрес
                            addr_parts = []
                            if 'addr:street' in tags:
                                addr_parts.append(tags['addr:street'])
                            if 'addr:housenumber' in tags:
                                addr_parts.append(tags['addr:housenumber'])
                            if 'addr:city' in tags:
                                addr_parts.append(tags['addr:city'])
                            if 'addr:village' in tags:
                                addr_parts.append(tags['addr:village'])
                            address = ', '.join(addr_parts) if addr_parts else 'Адрес неизвестен'
                            
                            # Создаём объект GeoFeature
                            feature = GeoFeature(
                                name=name,
                                lat=el_lat,
                                lon=el_lon,
                                address=address,
                                distance=dist,
                                category=category_name
                            )
                            result.append(feature)
                            
            except Exception as e:
                print(f"Ошибка при поиске ({key}={value}): {e}")
                continue
        
        # Сортируем по расстоянию
        result.sort(key=lambda x: x.distance)
        return result


    async def asyncify(self, func, *args, **kwargs) -> Any:
        """
        Асинхронный запуск любой функции из библиотеки.
        Не рекомендуется с листенерами и декораторами.
        
        :param func: Функция из FunctionsObject
        :param args: Позиционные аргументы функции
        :param kwargs: Именновые аргументы функции
        :return: Возвращает исходное значение функции.
        :rtype: Any
        """
        if not callable(func):
            raise RuntimeError('func is not callable!')
        return await asyncio.to_thread(func, *args, **kwargs)