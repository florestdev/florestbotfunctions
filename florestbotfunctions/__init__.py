# -*- coding: utf-8 -*-
"""Привет!\nВ этой библиотеке Вы увидете некоторые функции [бота Флореста](https://t.me/postbotflorestbot).\nМои социальные сети: [тык](https://taplink.cc/florestone4185)"""

import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import os, re
import random
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
from g4f.Provider import OIVSCodeSer2

class Cripto():
    """Класс со списком криптовалют, которые доступны для функции `crypto_price`.\nBITKOIN, USDT, DOGECOIN, HAMSTERCOIN"""
    BITKOIN = 'bitcoin'
    USDT = 'tether'
    DOGE = 'dogecoin'
    HMSTR = 'hamster'

class FunctionsObject:
    def __init__(self, proxies: dict = {}, html_headers: dict = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36', 'Accept-Language': 'ru-RU'}, google_api_key: str = "", gigachat_key: str = "", gigachat_id: str = "", username_mail: str = "", mail_passwd: str = "", speech_to_text_key: str = None, vk_token: str = None, rcon_ip: str = None, rcon_port: int = None, rcon_password: str = None):
        """Привет. Именно в данном классе находятся ВСЕ функции бота. Давай я объясню смысл параметров?\nproxies: прокси, которые используются при HTTPS запросах к сайтам.\nhtml_headers: заголовки HTTPS запросов.\ngoogle_api_key: апи ключ гугла. Получить его можно [здесь](https://console.google.com/)\ngigachat_key: ключ от GigaChat (ПАО "СберБанк")\ngigachat_id: ID от GigaChat.\nusername_mail: ваша электронная почта.\nmail_passwd: ваш API-ключ от SMTP сервера.\nspeech_to_text_key: API ключ от Google Speech To Text. Необязательно.\nvk_token: токен для работы с VK API от вашего аккаунта.\nrcon_ip: IP адрес сервера, к которому нужно подключиться.\nrcon_port: порт удаленного администрирования RCON, по умолчанию, 25575.\nrcon_password: пароль для доступа к RCON. Храните его в надежном месте."""
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
        self.detector = face_analysis()
        self.client_for_gpt = Client()
        if all([rcon_ip, rcon_port, rcon_password]):
            from mcrcon import MCRcon
            self.rcon_server = MCRcon(rcon_ip, rcon_password, rcon_port)
            print(f'RCON сервер инициализирован и готов к запуску.')
        else:
            self.rcon_server = None
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

        yt_obj = YouTube(url, proxies=self.proxies)

        if yt_obj.age_restricted:
            return 'На видео наложены возрастные ограничения.'    
        else:
            import io

            buffer = io.BytesIO()

            yt_obj.streams.get_lowest_resolution().stream_to_buffer(buffer)

            return buffer.getvalue()
    def search_videos(self, query: str):
        """Функция для поиска видео по запросу и дальнейшего его закачивания.\nquery: запрос, по которому надо искать видео."""
        from pytubefix import Search

        search = Search(query, proxies=self.proxies)
        videos = search.videos

        if len(videos) == 0:
            return 'Видео по запросу не существует.'
        else:
            video = videos[0]
            if video.age_restricted:
                return 'На видео, которое мы нашли первым присутствуют возрастные ограничение. Его скачивание невозможно.'  
            else:
                import io

                buffer = io.BytesIO()

                video.streams.get_lowest_resolution().stream_to_buffer(buffer)

                return buffer.getvalue()
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
    def censor_faces_image(self, image: bytes, model: str = 'full', return_resolution: tuple[int] = None, block_size: int = 20):
        """Данная функция превращает лица на фото в пиксели, короче, цензура.\nimage: фотка в `bytes`. Пример: open('photo.jpg', 'rb').read()\nmodel: модель для распознавания лиц. `tiny` и `full`.\nreturn_resolution: выходное разрешение. По умолчанию, разрешение исходной фотографии.\nblock_size: резкость мозаики, по умолчанию 20.\nВозвращает bytes."""
        from tqdm import tqdm
        if return_resolution:
            img_pil = Image.open(io.BytesIO(image)).resize(return_resolution, Image.Resampling.LANCZOS)
            img = cv2.imdecode(numpy.frombuffer(image, numpy.uint8), cv2.IMREAD_COLOR)
            img = cv2.resize(img, return_resolution)
            _, boxes, confs = self.detector.face_detection(frame_arr=img, model=model)
            
            faces = [(x, y, w, h) for i, (x, y, w, h) in enumerate(boxes) if confs[i] > 0.5]
            if not faces:
                print(f'Лица не были найдены на фотографии.')
                return image
            else:
                for x, y, w, h in tqdm(faces, desc='Цензурим лица..', ncols=70):
                    region = (x, y, x + w, y + h)
                    region_img = img_pil.crop(region)
                    small_size = (max(int(w) // block_size, 1), h)
                    small_region = region_img.resize(small_size, Image.Resampling.NEAREST)
                    mosaic_region = small_region.resize((w, h), Image.Resampling.NEAREST)
                    img_pil.paste(mosaic_region, region)
                output = io.BytesIO()
                img_pil.save(output, format='JPEG')
                print(f'Готово!')
                return output.getvalue()
        else:
            img_pil = Image.open(io.BytesIO(image))
            img = cv2.imdecode(numpy.frombuffer(image, numpy.uint8), cv2.IMREAD_COLOR)        
            _, boxes, confs = self.detector.face_detection(frame_arr=img, model=model)
            
            faces = [(x, y, w, h) for i, (x, y, w, h) in enumerate(boxes) if confs[i] > 0.5]
            if not faces:
                print(f'Лица не были найдены на фотографии.')
                return image
            else:
                for x, y, w, h in tqdm(faces, desc='Цензурим лица..', ncols=70):
                    region = (x, y, x + w, y + h)
                    region_img = img_pil.crop(region)
                    small_size = (max(int(w) // block_size, 1), h)
                    small_region = region_img.resize(small_size, Image.Resampling.NEAREST)
                    mosaic_region = small_region.resize((w, h), Image.Resampling.NEAREST)
                    img_pil.paste(mosaic_region, region)
                output = io.BytesIO()
                img_pil.save(output, format='JPEG')
                print(f'Готово!')
                return output.getvalue()
    def minecraft_server_info(self, ip: str, port: int = None, type_: str = 'java'):
        """Информация о Minecraft-сервере.\nip: ip/host сервера, или домен. Также можно написать ip:port.\nport: порт сервера, необязателен.\ntype: java, или bedrock."""
        if type_ in ['java', 'bedrock']:
            try:
                if type_ == 'java':
                    if not port:
                        server = JavaServer(ip)
                    else:
                        server = JavaServer(ip, port)
                    latency = server.ping()
                    query = server.query()
                    status = server.status()
                    return {"latency":latency, 'query':{"query_motd":query.motd.to_ansi(), 'query_map':query.map, 'query_players_count':query.players.online, 'query_players_max':query.players.max, 'all_info':query.as_dict()}, 'status':{"query_motd":status.motd.to_ansi(), 'description':status.description, 'icon_of_server_base64':status.icon, 'query_players_count':query.players.online, 'query_players_max':query.players.max, 'version':status.version.name, 'all_info':status.as_dict()}}
                else:
                    if not port:
                        server = BedrockServer(ip)
                    else:
                        server = BedrockServer(ip, port)
                    status = server.status()
                    return {"status":status.as_dict()}
            except:
                return
        else:
            return
    def gpt_4o_req(self, prompt: str, max_tokens: int = 4096, proxy: str = None):
        """Фигня для доступа к GPT-4o-mini.\nprompt: сам запрос к нейронке.\nmax_tokens: количество символов в ответе. По умолчанию, 4096.\nproxy: прокси. По умолчанию, которые в FunctionsObject."""
        if not proxy:
            req = self.client_for_gpt.chat.completions.create([{"role":"user", "content":prompt}], 'gpt-4o-mini', OIVSCodeSer2(), proxy=self.proxies.get('http'), max_tokens=max_tokens)
        else:
            req = self.client_for_gpt.chat.completions.create([{"role":"user", "content":prompt}], 'gpt-4o-mini', OIVSCodeSer2(), proxy=proxy, max_tokens=max_tokens)
        return req.choices[0].message.content
        
class CodeEditor:
    """Редактор кода, написанный на Python с графическим интерфейсом и подсветкой ключевых слов при написании кода на Python.\nmaster: объект класса "Tk", встроенной библиотеки tkinter."""
    def __init__(self, master: tk.Tk):
        """Инициализация."""
        self.master = master
        master.title("Редактор кода")
        master.geometry("800x600")
        KEYWORD_COLOR = "#FF7F50"  # Coral
        STRING_COLOR = "#98FB98"   # PaleGreen
        COMMENT_COLOR = "#808080"  # Gray
        FUNCTION_COLOR = "#4682B4" # SteelBlue
        NUMBER_COLOR = "#BDB76B"   # DarkKhaki
        BUILTIN_COLOR = "#FFA07A"  # LightSalmon

        self.filename = None  # Current file

        # --- Widgets ---
        self.text_area = scrolledtext.ScrolledText(
            master, wrap=tk.WORD, undo=True, font=("Consolas", 12)
        )
        self.text_area.pack(fill=tk.BOTH, expand=True)

        # --- Menu ---
        self.menu_bar = tk.Menu(master)
        master.config(menu=self.menu_bar)

        # File menu
        self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.file_menu.add_command(label="новенький", command=self.new_file)
        self.file_menu.add_command(label="открыть", command=self.open_file)
        self.file_menu.add_command(label="сохранить", command=self.save_file)
        self.file_menu.add_command(label="Сохранить в директории...", command=self.save_file_as)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Назад", command=master.quit)
        self.menu_bar.add_cascade(label="Файл", menu=self.file_menu)

        # Edit menu
        self.edit_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.edit_menu.add_command(label="Отменить", command=self.text_area.edit_undo)
        self.edit_menu.add_command(label="Вперёд", command=self.text_area.edit_redo)
        self.menu_bar.add_cascade(label="Изменить", menu=self.edit_menu)

        # Help menu
        self.help_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.help_menu.add_command(label="о проге", command=self.show_about)
        self.menu_bar.add_cascade(label="помоги, плиз", menu=self.help_menu)


        self.text_area.bind("<KeyRelease>", self.highlight_syntax)  # Подсветка при вводе

        # --- Syntax Highlighting Tags ---
        self.text_area.tag_configure("keyword", foreground=KEYWORD_COLOR)
        self.text_area.tag_configure("string", foreground=STRING_COLOR)
        self.text_area.tag_configure("comment", foreground=COMMENT_COLOR)
        self.text_area.tag_configure("function", foreground=FUNCTION_COLOR)
        self.text_area.tag_configure("number", foreground=NUMBER_COLOR)
        self.text_area.tag_configure("builtin", foreground=BUILTIN_COLOR)

        # --- Keywords ---
        self.keywords = ["def", "class", "if", "else", "elif", "for", "while", "return", "import", "from", "try", "except", "finally", "with", "as", "assert", "break", "continue", "del", "global", "nonlocal", "in", "is", "lambda", "pass", "raise", "yield"]
        self.builtins = ["print", "len", "range", "str", "int", "float", "bool", "list", "tuple", "dict", "set", "open", "file", "input", "exit", "help", "dir", "type", "object"]
    def new_file(self):
        """Создает новый файл."""
        self.text_area.delete("1.0", tk.END)  # Clear the text area
        self.filename = None  # Reset filename
        self.master.title("Редактор кода - New File")

    def open_file(self):
        """Открыть файл."""
        filepath = filedialog.askopenfilename(
            filetypes=[("All Files", "*.*"), ("Text Files", "*.txt"), ("Python Files", "*.py"), ("C++ Files", "*.cpp")]
        )
        if filepath:
            try:
                with open(filepath, "r", encoding='UTF-8') as file:
                    content = file.read()
                self.text_area.delete("1.0", tk.END)
                self.text_area.insert("1.0", content)
                self.filename = filepath
                self.master.title(f"Редактор кода - {os.path.basename(filepath)}")
            except Exception as e:
                messagebox.showerror("ОШИБОЧКА", f"вот это:\n{e}")

    def save_file(self):
        """Сохранить файл."""
        if self.filename:
            try:
                content = self.text_area.get("1.0", tk.END)
                with open(self.filename, "w") as file:
                    file.write(content)
                messagebox.showinfo("успех", "файл сохранен.")
            except Exception as e:
                messagebox.showerror("ошибочка", f"лееее:\n{e}")
        else:
            self.save_file_as()

    def save_file_as(self):
        """Сохранить файл как..."""
        filepath = filedialog.asksaveasfilename(
            defaultextension=".txt", filetypes=[("All Files", "*.*"), ("Text Files", "*.txt"), ("Python Files", "*.py"), ("C++ Files", "*.cpp")]
        )
        if filepath:
            try:
                content = self.text_area.get("1.0", tk.END)
                with open(filepath, "w") as file:
                    file.write(content)
                self.filename = filepath
                self.master.title(f"Редактор кода - {os.path.basename(filepath)}")
                messagebox.showinfo("урыыы", "файл типо сохранен.")
            except Exception as e:
                messagebox.showerror("ошибОЧКА", f"посмотри сам:\n{e}")

    def show_about(self):
        """О программе."""
        messagebox.showinfo(
            "О проге", "Редактор кода от Флореста. Сделано с любовью."
        )
    def highlight_syntax(self, event=None):
        """Подсвечивает синтаксис Python."""
        # Удаляем все старые теги
        for tag in self.text_area.tag_names():
            self.text_area.tag_remove(tag, "1.0", tk.END)

        text = self.text_area.get("1.0", tk.END)

        # Подсветка комментариев
        for match in re.finditer(r"#.*", text):
            start = "1.0 + %dc" % match.start()
            end = "1.0 + %dc" % match.end()
            self.text_area.tag_add("comment", start, end)

        # Подсветка строк
        for match in re.finditer(r"(\".*\")|(\'.*\')", text):
            start = "1.0 + %dc" % match.start()
            end = "1.0 + %dc" % match.end()
            self.text_area.tag_add("string", start, end)

        # Подсветка ключевых слов
        for word in self.keywords:
            pattern = r'\b' + word + r'\b'  # Границы слова
            for match in re.finditer(pattern, text):
                start = "1.0 + %dc" % match.start()
                end = "1.0 + %dc" % match.end()
                self.text_area.tag_add("keyword", start, end)

        # Подсветка встроенных функций
        for word in self.builtins:
            pattern = r'\b' + word + r'\b'  # Границы слова
            for match in re.finditer(pattern, text):
                start = "1.0 + %dc" % match.start()
                end = "1.0 + %dc" % match.end()
                self.text_area.tag_add("builtin", start, end)

        # Подсветка чисел
        for match in re.finditer(r'\b\d+\b', text):
            start = "1.0 + %dc" % match.start()
            end = "1.0 + %dc" % match.end()
            self.text_area.tag_add("number", start, end)

        # Подсветка функций (очень упрощенно)
        for match in re.finditer(r'def\s+(\w+)\s*\(', text):
            start = "1.0 + %dc" % match.start(1) # Начало имени функции
            end = "1.0 + %dc" % match.end(1) # Конец имени функции
            self.text_area.tag_add("function", start, end)
            
import asyncio
import io
import random
import string
import re
from datetime import date
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import aiohttp
import aiofiles
import gtts
import qrcode
from PIL import Image, ImageOps, ImageDraw, ImageFont
import speech_recognition as sr
from pygame import mixer
import time
from colorama import Fore
import vk_api
from vkpymusic import Service, TokenReceiver
import faker as faker_
import subprocess
import os
from bs4 import BeautifulSoup
import aiosmtplib

class AsyncFunctionsObject:
    def __init__(self, proxies: dict = {}, html_headers: dict = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36', 'Accept-Language': 'ru-RU'}, google_api_key: str = "", gigachat_key: str = "", gigachat_id: str = "", username_mail: str = "", mail_passwd: str = "", speech_to_text_key: str = None, vk_token: str = None, rcon_ip: str = None, rcon_port: int = None, rcon_password: str = None):
        """Initialize the FunctionsObject with configuration parameters."""
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
        self.client_for_gpt = AsyncClient()
        if all([rcon_ip, rcon_password, rcon_port]):
            from aiomcrcon import Client
            self.rcon_server = Client(rcon_ip, rcon_port, rcon_password)
            print(f'RCON сервер инициализирован!')
        else:
            self.rcon_server = None
    async def generate_image(self, prompt: str) -> bytes:
        """Generate an image using GigaChat API."""
        if not self.gigachat_key or not self.client_id_gigachat:
            return "Нужно указать параметр `gigachat_key` и `gigachat_id` в настройках класса для работы с этой функцией."

        async with aiohttp.ClientSession() as session:
            # Get access token
            url = "https://ngw.devices.sberbank.ru:9443/api/v2/oauth"
            payload = {'scope': 'GIGACHAT_API_PERS'}
            headers = {
                'Content-Type': 'application/x-www-form-urlencoded',
                'Accept': 'application/json',
                'RqUID': f'{self.client_id_gigachat}',
                'Authorization': f'Basic {self.gigachat_key}'
            }
            async with session.post(url, headers=headers, data=payload, ssl=False, proxy=self.proxies.get('https')) as response:
                access_token = (await response.json())['access_token']

            # Generate image
            headers = {
                'Content-Type': 'application/json',
                'Accept': 'application/json',
                'Authorization': f'Bearer {access_token}'
            }
            data = {
                "model": "GigaChat",
                "messages": [
                    {"role": "system", "content": "Glory to Florest."},
                    {"role": "user", "content": prompt}
                ],
                "function_call": "auto"
            }
            async with session.post(
                'https://gigachat.devices.sberbank.ru/api/v1/chat/completions',
                headers=headers,
                json=data,
                ssl=False,
                proxy=self.proxies.get('https')
            ) as response:
                json_data = await response.json()
                patterns = r"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}"
                matches = re.search(patterns, json_data['choices'][0]['message']['content'])
                if not matches:
                    return f"Нельзя нарисовать что-либо по данному запросу. Причина: {json_data['choices'][0]['message']['content']}"
                else:
                    async with session.get(
                        f"https://gigachat.devices.sberbank.ru/api/v1/files/{matches.group()}/content",
                        headers={'Accept': 'application/jpg', "Authorization": f"Bearer {access_token}"},
                        ssl=False,
                        proxy=self.proxies.get('https')
                    ) as req_img:
                        return await req_img.read()

    async def ai(self, prompt: str, is_voice: bool = False):
        """Interact with GigaChat API, optionally generating voice output."""
        if not self.gigachat_key or not self.client_id_gigachat:
            return "Нужно указать параметр `gigachat_key` и `gigachat_id` в настройках класса для работы с этой функцией."

        async with aiohttp.ClientSession() as session:
            # Get access token
            url = "https://ngw.devices.sberbank.ru:9443/api/v2/oauth"
            payload = {'scope': 'GIGACHAT_API_PERS'}
            headers = {
                'Content-Type': 'application/x-www-form-urlencoded',
                'Accept': 'application/json',
                'RqUID': f'{self.client_id_gigachat}',
                'Authorization': f'Basic {self.gigachat_key}'
            }
            async with session.post(url, headers=headers, data=payload, ssl=False, proxy=self.proxies.get('https')) as response:
                access_token = (await response.json())['access_token']

            # Send prompt
            url1 = "https://gigachat.devices.sberbank.ru/api/v1/chat/completions"
            payload1 = {
                "model": "GigaChat",
                "messages": [{"role": "user", "content": prompt}],
                "stream": False,
                "repetition_penalty": 1
            }
            headers1 = {
                'Content-Type': 'application/json',
                'Accept': 'application/json',
                'Authorization': f'Bearer {access_token}'
            }
            async with session.post(url1, headers=headers1, json=payload1, ssl=False, proxy=self.proxies.get('https')) as response1:
                result = await response1.json()
                if not is_voice:
                    return result
                else:
                    buffer = io.BytesIO()
                    gtts.gTTS(result['choices'][0]['message']['content'], lang='ru', lang_check=False).write_to_fp(buffer)
                    return buffer.getvalue()

    async def deanon(self, ip: str) -> list:
        """Get geolocation information for an IP address."""
        async with aiohttp.ClientSession() as session:
            async with session.get(f'http://ip-api.com/json/{ip}?lang=ru', headers=self.headers, proxy=self.proxies.get('http')) as response:
                data = await response.json()
                return [f'{key.title()}: {value}' for key, value in data.items()]

    async def download_video(self, url: str):
        """Download a YouTube video."""
        from pytubefix import YouTube
        yt_obj = YouTube(url, proxies=self.proxies)
        if yt_obj.age_restricted:
            return 'На видео наложены возрастные ограничения.'
        buffer = io.BytesIO()
        yt_obj.streams.get_lowest_resolution().stream_to_buffer(buffer)
        return buffer.getvalue()

    async def search_videos(self, query: str):
        """Search and download a YouTube video by query."""
        from pytubefix import Search
        search = Search(query, proxies=self.proxies)
        videos = search.videos
        if not videos:
            return 'Видео по запросу не существует.'
        video = videos[0]
        if video.age_restricted:
            return 'На видео, которое мы нашли первым присутствуют возрастные ограничение. Его скачивание невозможно.'
        buffer = io.BytesIO()
        video.streams.get_lowest_resolution().stream_to_buffer(buffer)
        return buffer.getvalue()

    async def create_demotivator(self, top_text: str, bottom_text: str, photo: bytes, font: str):
        """Create a demotivator image."""
        image = io.BytesIO(photo)
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
        top_size = 80
        while text_width >= (width + 250) - 20:
            top_size -= 1
            font_1 = ImageFont.truetype(font=font, size=top_size, encoding='UTF-8')
            text_width = font_1.getlength(top_text)
        font_2 = ImageFont.truetype(font=font, size=60, encoding='UTF-8')
        text_width = font_2.getlength(bottom_text)
        bottom_size = 60
        while text_width >= (width + 250) - 20:
            bottom_size -= 1
            font_2 = ImageFont.truetype(font=font, size=bottom_size, encoding='UTF-8')
            text_width = font_2.getlength(bottom_text)
        size_1 = drawer.textlength(top_text, font=font_1)
        size_2 = drawer.textlength(bottom_text, font=font_2)
        drawer.text(((1280 - size_1) / 2, 840), top_text, fill='white', font=font_1)
        drawer.text(((1280 - size_2) / 2, 930), bottom_text, fill='white', font=font_2)
        result_here = io.BytesIO()
        img.save(result_here, 'JPEG')
        del drawer
        return result_here.getvalue()

    async def photo_make_black(self, photo: bytes):
        """Convert a photo to black and white."""
        your_photo = io.BytesIO(photo)
        image = Image.open(your_photo)
        new_image = image.convert('L')
        buffer = io.BytesIO()
        new_image.save(buffer, 'JPEG')
        return buffer.getvalue()

    async def check_weather(self, city):
        """Check weather for a city or coordinates."""
        async with aiohttp.ClientSession() as session:
            if isinstance(city, str):
                try:
                    async with session.get(f'https://geocoding-api.open-meteo.com/v1/search?name={city}', headers=self.headers, proxy=self.proxies.get('https')) as response:
                        d = await response.json()
                        lot = d["results"][0]["latitude"]
                        lat = d['results'][0]['longitude']
                    async with session.get(f'https://api.open-meteo.com/v1/forecast?latitude={lot}&longitude={lat}&current_weather=true', headers=self.headers, proxy=self.proxies.get('https')) as req:
                        if req.status != 200:
                            return None
                        data = await req.json()
                        temperature = data['current_weather']['temperature']
                        title = {0: "Ясно", 1: "Частично облачно", 3: "Облачно", 61: "Дождь"}
                        weather = title.get(data['current_weather']['weathercode'], 'Неизвестно')
                        wind_dir = 'Север' if 0 <= (d := data['current_weather']['winddirection']) < 45 or 315 <= d <= 360 else 'Восток' if 45 <= d < 135 else 'Юг' if 135 <= d < 225 else 'Запад'
                        time1 = data['current_weather']['time']
                        wind = data['current_weather']['windspeed']
                        return {'temp': temperature, 'weather': weather, 'weather_code': data['current_weather']['weathercode'], 'wind_direction': wind_dir, 'time_of_data': time1, 'wind_speed': wind}
                except:
                    return None
            elif isinstance(city, dict):
                try:
                    lat = city["lat"]
                    lon = city["lon"]
                    async with session.get(f'https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true', headers=self.headers, proxy=self.proxies.get('https')) as req:
                        data = await req.json()
                        temperature = data['current_weather']['temperature']
                        title = {0: "Ясно", 1: "Частично облачно", 3: "Облачно", 61: "Дождь"}
                        weather = title.get(data['current_weather']['weathercode'], 'Неизвестно')
                        wind_dir = 'Север' if 0 <= (d := data['current_weather']['winddirection']) < 45 or 315 <= d <= 360 else 'Восток' if 45 <= d < 135 else 'Юг' if 135 <= d < 225 else 'Запад'
                        time1 = data['current_weather']['time']
                        wind = data['current_weather']['windspeed']
                        return {'temp': temperature, 'weather': weather, 'weather_code': data['current_weather']['weathercode'], 'wind_direction': wind_dir, 'time_of_data': time1, 'wind_speed': wind}
                except KeyError:
                    return f'Нужно составить словарь, согласно образцу, указанного в описании функции.'
                except:
                    return None
            else:
                return 'Поддерживаемые типы данных: `str` для названия города и `dict` для координатов.'

    async def create_qr(self, content: str):
        """Create a QR code."""
        buffer = io.BytesIO()
        qr = qrcode.make(content)
        qr.save(buffer, scale=10)
        return buffer.getvalue()

    async def get_charts(self):
        """Get Yandex Music charts."""
        async with aiohttp.ClientSession() as session:
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
            async with session.get('https://music.yandex.ru/handlers/main.jsx', params=params, headers=headers, proxy=self.proxies.get('https')) as response:
                chart = (await response.json())['chartPositions']
                result = []
                for track in chart[:10]:
                    position = track['track']['chart']['position']
                    title = track['track']['title']
                    author = track['track']['artists'][0]['name']
                    result.append(f"№{position}: {author} - {title}")
                return f'Чарты Яндекс Музыки на данный момент🔥\n🥇{result[0]}\n🥈{result[1]}\n🥉{result[2]}\n{result[3]}\n{result[4]}\n{result[5]}\n{result[6]}\n{result[7]}\n{result[8]}\n{result[9]}'

    async def generate_password(self, symbols: int = 15):
        """Generate a random password."""
        symbols_ascii = list(string.ascii_letters + string.digits)
        random.shuffle(symbols_ascii)
        return ''.join(symbols_ascii[:symbols])

    async def text_to_speech(self, text: str, lang: str = 'ru'):
        """Convert text to speech."""
        buffer = io.BytesIO()
        engine = gtts.gTTS(text, lang=lang)
        engine.write_to_fp(buffer)
        return buffer.getvalue()

    async def information_about_yt_channel(self, url: str):
        """Узнать информацию о YouTube канале на Python.\nurl: ссылка на канал."""
        if not self.google_key:
            return 'Для использования данной функции нужно указать параметр `google_key` в конструктор класса.'
        else:
            import httpx
            
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

            # Создаем асинхронный клиент и выполняем запрос
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    'https://www.googleapis.com/youtube/v3/channels',
                    params=params,
                    headers=self.headers,
                    proxies=self.proxies
                )
                
            return response.json()

    async def crypto_price(self, crypto: str, currency: str = 'rub'):
        """Get cryptocurrency price."""
        async with aiohttp.ClientSession() as session:
            async with session.get('https://api.coingecko.com/api/v3/simple/price', params={"ids": crypto, 'vs_currencies': currency}, headers=self.headers, proxy=self.proxies.get('https')) as response:
                r = await response.json()
                if not r:
                    return "Неправильная валюта, или криптовалюта."
                try:
                    return r[crypto][currency]
                except:
                    return "Произошла ошибка. Возможно, были преодолены лимиты API."

    async def password_check(self, nickname: str) -> int:
        """Check for password leaks by nickname."""
        async with aiohttp.ClientSession() as session:
            async with session.get(f'https://api.proxynova.com/comb?query={nickname}&start=0&limit=15', headers=self.headers, proxy=self.proxies.get('https')) as req:
                if req.status == 200:
                    return (await req.json())['count']
                return 0

    async def generate_nitro(self, count: int):
        """Generate Discord Nitro codes."""
        results = []
        for _ in range(count):
            characters = string.ascii_uppercase + string.digits
            random_code = ''.join(random.choice(characters) for _ in range(15))
            formatted_code = '-'.join(random_code[i:i+4] for i in range(0, 15, 4))
            results.append(formatted_code)
        return results

    async def fake_human(self):
        """Generate fake Russian citizen data."""
        faker = faker_.Faker('ru-RU')
        today = date.today()
        year_f, month_f, day_f = map(int, str(faker.date_of_birth(minimum_age=25, maximum_age=50)).split("-"))
        age_t = today.year - year_f - ((today.month, today.day) < (month_f, day_f))
        return {
            "name": faker.name(),
            "age": age_t,
            "work_place": faker.company(),
            "work_class": faker.job().lower(),
            "address": f"Российская Федерация, {faker.address()}",
            "postal_code": faker.address()[-6:],
            'telephone_number': faker.phone_number(),
            "useragent": faker.user_agent(),
            "number_card": faker.credit_card_number(),
            "provider_of_card": faker.credit_card_provider(),
            "expire_card": faker.credit_card_expire(),
            "inn": faker.businesses_inn(),
            "orgn": faker.businesses_ogrn()
        }

    async def real_info_of_photo(self, photo: bytes):
        """Extract location data from photo metadata."""
        with Image.open(io.BytesIO(photo)) as img:
            metadata = img._getexif()
            if not metadata or not metadata.get(34853):
                return None
            gps_info = metadata[34853]
            lat = gps_info[2]
            lon = gps_info[4]
            lat_ref = gps_info[3]
            latitude = (lat[0] + lat[1] / 60.0 + lat[2] / 3600.0)
            longitude = (lon[0] + lon[1] / 60.0 + lon[2] / 3600.0)
            datetime_original = metadata.get(36867)
            async with aiohttp.ClientSession() as session:
                try:
                    if lat_ref != 'E':
                        latitude = -latitude
                    async with session.get(f"https://nominatim.openstreetmap.org/reverse?lat={latitude}&lon={longitude}&format=json", headers=self.headers, proxy=self.proxies.get('https')) as response:
                        json_data = await response.json()
                        return {
                            "country": json_data["address"]["country"],
                            "region": json_data["address"]["state"],
                            "district": json_data["address"]["district"],
                            'city': json_data["address"]["city"],
                            "full_address": json_data["display_name"],
                            'postcode': json_data["address"]["postcode"],
                            'datetime': datetime_original
                        }
                except:
                    if lat_ref != 'E':
                        latitude = -latitude
                    longitude = -longitude
                    async with session.get(f"https://nominatim.openstreetmap.org/reverse?lat={latitude}&lon={longitude}&format=json", headers=self.headers, proxy=self.proxies.get('https')) as response:
                        json_data = await response.json()
                        return {
                            "country": json_data["address"]["country"],
                            "region": json_data["address"]["state"],
                            "district": json_data["address"]["district"],
                            'city': json_data["address"]["city"],
                            "full_address": json_data["display_name"],
                            'postcode': json_data["address"]["postcode"],
                            'datetime': datetime_original
                        }

    async def bmi(self, weight: float, height: float):
        """Calculate BMI."""
        if weight <= 0 or height <= 0:
            return None
        bmi = weight / (height ** 2)
        if bmi < 18.5:
            return {"bmi": f'{bmi:.2f}', "status": "Недостаточный вес"}
        elif 18.5 <= bmi < 25:
            return {"bmi": f'{bmi:.2f}', "status": "Нормальный вес"}
        elif 25 <= bmi < 30:
            return {"bmi": f'{bmi:.2f}', "status": "Избыточный вес"}
        else:
            return {"bmi": f'{bmi:.2f}', "status": "Ожирение"}

    async def link_on_user(self, id: str):
        """Generate Telegram user link by ID."""
        if len(id) != 10:
            return {'status': f'Пользовательский ID должен быть ровно 10 символов.', 'url': None}
        try:
            return {"status": "Успех!", "url": f"tg://openmessage?user_id={int(id)}"}
        except:
            return {"status": f'Неверный формат ID.', 'url': None}

    async def send_mail(self, subject: str, body: str, recipient: str, service: str = 'smtp.mail.ru', service_port: int = 465):
        """Send an email."""
        if not self.username_mail or not self.mail_passwd:
            return "Укажите параметр username_mail и mail_passwd в настройках класса."
        message = MIMEMultipart()
        message["From"] = self.username_mail
        message["To"] = recipient
        message["Subject"] = subject
        message.attach(MIMEText(body, "plain", 'utf-8'))
        async with aiosmtplib.SMTP(hostname=service, port=service_port, use_tls=True) as server:
            await server.login(self.username_mail, self.mail_passwd)
            await server.sendmail(self.username_mail, recipient, message.as_string())

    async def parsing_site(self, url: str):
        """Parse a website's HTML."""
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(url, headers=self.headers, proxy=self.proxies.get('https')) as response:
                    if response.status == 200:
                        return await response.text()
                    return None
            except:
                return None

    async def google_photo_parsing(self, query: str):
        """Parse Google Images for photo links."""
        async with aiohttp.ClientSession() as session:
            async with session.get(f'https://www.google.com/search?q={query}&tbm=isch&imglq=1&isz=l&safe=unactive', headers=self.headers, proxy=self.proxies.get('https')) as response:
                soup = BeautifulSoup(await response.text(), 'html.parser')
                tags = soup.find_all('img', {'src': True})
                return [tag['src'] for tag in tags if 'https://' in tag['src']]

    async def speech_to_text(self, file, language: str = 'ru-RU') -> str:
        """Convert speech to text."""
        r = sr.Recognizer()
        with sr.AudioFile(file) as source:
            audio = r.record(source)
        try:
            text = await asyncio.to_thread(r.recognize_google, audio, language=language)
            return text
        except sr.UnknownValueError:
            return 'Ошибка распознавания текста.'
        except:
            return 'Неизвестная ошибка. Также могут быть проблемы с подключением.'

    async def email_mass_send(self, receivers: list, title: str, body: str, service: str = 'smtp.mail.ru', service_port: int = 465):
        """Send mass emails."""
        if not self.username_mail or not self.mail_passwd:
            return "Укажите параметр username_mail и mail_passwd в настройках класса."
        async with aiosmtplib.SMTP(hostname=service, port=service_port, use_tls=True) as server:
            await server.login(self.username_mail, self.mail_passwd)
            for email in receivers:
                message = MIMEMultipart()
                message["From"] = self.username_mail
                message["To"] = email
                message["Subject"] = title
                message.attach(MIMEText(body, "plain", 'utf-8'))
                await server.sendmail(self.username_mail, email, message.as_string())

    async def alarm_clock(self, time_to_ring: str, sound):
        """Set an alarm clock."""
        from os import environ
        environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
        mixer.init()
        alarm_time = time.strptime(time_to_ring, "%H:%M:%S")
        data = {'hour': alarm_time.tm_hour, 'minutes': alarm_time.tm_min, 'seconds': alarm_time.tm_sec}
        print(f'{Fore.GREEN}Будильник успешно запущен на {Fore.BLUE}{time_to_ring}.')
        while True:
            current_time = time.localtime()
            hour_ = current_time.tm_hour
            minutes_ = current_time.tm_min
            seconds_ = current_time.tm_sec
            if {'hour': hour_, 'minutes': minutes_, 'seconds': seconds_} == data:
                print(f'{Fore.RED}ВНИМАНИЕ!!! БУДИЛЬНИК АКТИВИРОВАН, ПРОСЫПАЙТЕСЬ!!!')
                mixer.Sound(sound).play(loops=-1)
                break
            await asyncio.sleep(1)

    async def cpp_compiler(self, filename: str, filename_output: str):
        """Compile C++ code."""
        process = await asyncio.create_subprocess_exec(
            'g++', filename, '-o', filename_output,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await process.communicate()
        return process.returncode == 0

    async def python_exe_compiler(self, path_to_py: str, path_output: str, flags: str = None):
        """Compile Python to executable."""
        os.chdir(path_output)
        cmd = f'pyinstaller --distpath "{path_output}" {flags or ""} "{path_to_py}"'
        process = await asyncio.create_subprocess_shell(
            cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await process.communicate()
        return process.returncode == 0

    async def tracking_youtube_author(self, channel_url: str, token_of_bot: str, id: int):
        """Track new YouTube content and send notifications via Telegram bot."""
        from pytubefix import Channel
        try:
            channel = Channel(channel_url, proxies=self.proxies)
        except:
            return "Данного канала не существует."
        last_video = channel.videos[0].watch_url if channel.videos else None
        last_short = channel.shorts[0].watch_url if channel.shorts else None
        last_live = channel.live[0].watch_url if channel.live else None
        async with aiohttp.ClientSession() as session:
            while True:
                channel = Channel(channel_url, proxies=self.proxies)  # Refresh channel data
                if channel.videos and channel.videos[0].watch_url != last_video:
                    last_video = channel.videos[0].watch_url
                    text = f'Вышло новое видео у автора {channel.title}.\nНазвание: {channel.videos[0].title}\nСсылка: {channel.videos[0].watch_url}'
                    async with session.post(f'https://api.telegram.org/bot{token_of_bot}/sendMessage?chat_id={id}&text={text}', proxy=self.proxies.get('https')) as response:
                        await response.read()
                elif channel.shorts and channel.shorts[0].watch_url != last_short:
                    last_short = channel.shorts[0].watch_url
                    text = f'Вышло новое видео у автора {channel.title}.\nНазвание: {channel.shorts[0].title}\nСсылка: {channel.shorts[0].watch_url}'
                    async with session.post(f'https://api.telegram.org/bot{token_of_bot}/sendMessage?chat_id={id}&text={text}', proxy=self.proxies.get('https')) as response:
                        await response.read()
                elif channel.live and channel.live[0].watch_url != last_live:
                    last_live = channel.live[0].watch_url
                    text = f'Вышло новое видео у автора {channel.title}.\nНазвание: {channel.live[0].title}\nСсылка: {channel.live[0].watch_url}'
                    async with session.post(f'https://api.telegram.org/bot{token_of_bot}/sendMessage?chat_id={id}&text={text}', proxy=self.proxies.get('https')) as response:
                        await response.read()
                await asyncio.sleep(0.5)

    async def searching_musics_vk(self, query: str, count: int = 3):
        """Search for music on VK."""
        if not self.token_of_vk:
            return "Необходимо в настройках класса указать токен от Вашего аккаунта в VK."
        service = Service('KateMobileAndroid/56 lite-460 (Android 4.4.2; SDK 19; x86; unknown Android SDK built for x86; en)', self.token_of_vk)
        songs = await asyncio.to_thread(lambda: [track.to_dict() for track in service.search_songs_by_text(query, count)])
        return songs

    async def get_last_post(self, query: str):
        """Get the latest post from a VK public."""
        vk_session = vk_api.VkApi(token=self.token_of_vk)
        vk = vk_session.get_api()
        response = await asyncio.to_thread(vk.groups.search, q=query, type='group', count=1)
        if response['count'] > 0:
            response1 = await asyncio.to_thread(vk.wall.get, owner_id=-int(response['items'][0]['id']), count=1)
            try:
                post = response1['items'][0]
                text = post.get('text', 'Текст отсутствует')
                post_id = post['id']
                owner_id = post['owner_id']
                link = f"https://vk.com/wall{owner_id}_{post_id}"
                likes = post['likes']['count']
                views = post['views']['count']
                reposts = post['reposts']['count']
                return {"text": text, "post_id": post_id, "owner_id": owner_id, "link": link, 'views': views, 'reposts': reposts, 'likes': likes}
            except:
                return None
        return None
    async def image_text_recognition(self, img: bytes, lang: str = 'ru'):
        """Разбор текста на изображении, с помощью инструментов Google Cloud.\nimg: ваше изображение в bytes.\nlang: язык текста на изображении."""
        import base64
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

            # Асинхронный запрос
            async with aiohttp.ClientSession() as session:
                async with session.post(url, json=request_body, headers=headers, proxy=self.proxies.get('https') if self.proxies else None) as response:
                    return {"code": response.status, "answer": await response.json()}
    async def minecraft_server_info(self, ip: str, port: int = None, type_: str = 'java'):
        """Информация о Minecraft-сервере.\nip: ip/host сервера, или домен. Также можно написать ip:port.\nport: порт сервера, необязателен.\ntype: java, или bedrock."""
        if type_ in ['java', 'bedrock']:
            try:
                if type_ == 'java':
                    if not port:
                        server = JavaServer(ip)
                    else:
                        server = JavaServer(ip, port)
                    latency = await asyncio.to_thread(server.ping)
                    query = await asyncio.to_thread(server.query)
                    status = await asyncio.to_thread(server.status)
                    return {"latency":latency, 'query':{"query_motd":query.motd.to_ansi(), 'query_map':query.map, 'query_players_count':query.players.online, 'query_players_max':query.players.max, 'all_info':query.as_dict()}, 'status':{"query_motd":status.motd.to_ansi(), 'description':status.description, 'icon_of_server_base64':status.icon, 'query_players_count':query.players.online, 'query_players_max':query.players.max, 'version':status.version.name, 'all_info':status.as_dict()}}
                else:
                    if not port:
                        server = BedrockServer(ip)
                    else:
                        server = BedrockServer(ip, port)
                    status = await asyncio.to_thread(server.status)
                    return {"status":status.as_dict()}
            except:
                return
        else:
            return
                
    async def rcon_send(self, command: str):
        """Команда для отправки команды на сервер через RCON.\nТребует rcon_ip, rcon_port и rcon_password в настройках AsyncFunctionsObject.\ncommand: команда с аргументами. Пример: `say Привет!`\nВозвращает ответ от сервера."""
        if not self.rcon_server:
            return 'RCON сервер не инициализирован.\nПроверьте, указали ли Вы нужные параметры в настройках класса.'
        else:
            await self.rcon_server.connect()
            return await self.rcon_server.send_cmd(command)
        
    async def gpt_4o_req(self, prompt: str, max_tokens: int = 4096, proxy: str = None):
        """Фигня для доступа к GPT-4o-mini.\nprompt: сам запрос к нейронке.\nmax_tokens: количество символов в ответе. По умолчанию, 4096.\nproxy: прокси. По умолчанию, которые в FunctionsObject."""
        if not proxy:
            req = await self.client_for_gpt.chat.completions.create([{"role":"user", "content":prompt}], 'gpt-4o-mini', OIVSCodeSer2(), proxy=self.proxies.get('http'), max_tokens=max_tokens)
        else:
            req = await self.client_for_gpt.chat.completions.create([{"role":"user", "content":prompt}], 'gpt-4o-mini', OIVSCodeSer2(), proxy=proxy, max_tokens=max_tokens)
        return req.choices[0].message.content
class AsyncYandexParser:
    """Асинхронный парсер картинок с Яндекса.\nПоддерживаются только приватные HTTP(s) прокси с именем пользователя и паролем. Также требуется установка Google Chrome на машину.\nis_headless: скрывать окно с парсером?"""

    def __init__(self, proxy_host: str = None, proxy_port: int = None, proxy_user: str = None, proxy_pass: str = None, is_headless:bool=False, arguments: list[str] = None, extensions: list[str] = None):
        """Асинхронный парсер картинок с Яндекса.\nПоддерживаются только приватные HTTP(s) прокси с именем пользователя и паролем. Также требуется установка Google Chrome на машину.\nis_headless: скрывать окно с парсером?\narguments: аргументы для запуска парсера. Пример: ['--headless', '--no-sandbox', ...]\nextensions: различные самописные расширения в формате `.crx`, директории к ним. Пример: ['C:/osu.crx', 'D:/minecraft.crx']"""
        self.proxy_host = proxy_host
        self.proxy_port = proxy_port
        self.proxy_user = proxy_user
        self.proxy_pass = proxy_pass
        self.isheadless = is_headless
        self.arguments = arguments
        self.extensions = extensions
        print(f'Парсер инициализирован, сучки!\nНачните парсить с помощью функции start_parsing.')

    def create_proxy_auth_extension(self):
        """Создаём плагин для авторизации прокси, блять."""
        if all([self.proxy_host, self.proxy_port, self.proxy_user, self.proxy_pass]):
            manifest_json = """
            {
                "version": "1.0.0",
                "manifest_version": 2,
                "name": "Chrome Proxy",
                "permissions": [
                    "proxy",
                    "tabs",
                    "unlimitedStorage",
                    "storage",
                    "<all_urls>",
                    "webRequest",
                    "webRequestBlocking"
                ],
                "background": {
                    "scripts": ["background.js"]
                }
            }
            """

            background_js = """
            var config = {
                mode: "fixed_servers",
                rules: {
                    singleProxy: {
                        scheme: "http",
                        host: "%s",
                        port: parseInt(%s)
                    },
                    bypassList: ["localhost"]
                }
            };

            chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});

            chrome.webRequest.onAuthRequired.addListener(
                function(details) {
                    return {
                        authCredentials: {
                            username: "%s",
                            password: "%s"
                        }
                    };
                },
                {urls: ["<all_urls>"]},
                ['blocking']
            );
            """ % (self.proxy_host, self.proxy_port, self.proxy_user, self.proxy_pass)

            plugin_file = 'proxy_auth_plugin.zip'
            with zipfile.ZipFile(plugin_file, 'w') as zp:
                zp.writestr("manifest.json", manifest_json)
                zp.writestr("background.js", background_js)
            
            return plugin_file
        else:
            return None

    async def download_image(self, session: aiohttp.ClientSession, img_url, directory):
        """Качаем картинку асинхронно, блять."""
        if not all([self.proxy_host, self.proxy_port, self.proxy_user, self.proxy_pass]):
            if img_url and "http" in img_url:
                try:
                    async with session.get(img_url) as response:
                        if response.status == 200:
                            _ = random.random()
                            file_path = os.path.join(directory, f'{_}.jpg')
                            with open(file_path, 'wb') as file:
                                file.write(await response.read())
                except Exception as e:
                    print(f"Картинка не скачалась, пиздец: {e}")
        else:
            if img_url and "http" in img_url:
                try:
                    proxy_auth = aiohttp.BasicAuth(login=self.proxy_user, password=self.proxy_pass)
                    async with session.get(img_url, proxy=f'http://{self.proxy_host}:{self.proxy_port}', proxy_auth=proxy_auth) as response:
                        if response.status == 200:
                            _ = random.random()
                            file_path = os.path.join(directory, f'{_}.jpg')
                            with open(file_path, 'wb') as file:
                                file.write(await response.read())
                except Exception as e:
                    print(f"Картинка не скачалась, пиздец: {e}")

    async def start_parsing(self, query: str, directory: str, max_images=10, scrolly=5, pages:int=6):
        """Начать парсить..\nquery: запрос. Пример: котики\ndirectory: директория на машине, где надо сохранять картинки.\nmax_images: максимальное количество картинок в директории.\nscrolly: скока скроллить картинки?\npages: сколько страниц с картинками парсить?"""
        # Создаём директорию, если не существует
        if not os.path.exists(directory):
            os.makedirs(directory)
        os.chdir(directory)

        # Настройка браузера
        try:
            proxy_plugin = self.create_proxy_auth_extension()
            chrome_options = Options()
            if proxy_plugin:
                chrome_options.add_extension(proxy_plugin)
            chrome_options.add_argument("--log-level=1")
            if self.isheadless:
                chrome_options.add_argument('--headless')
            if self.arguments:
                print(f'Добавление пользовательских аргументов..')
                for arg in self.arguments:
                    chrome_options.add_argument(arg)
                print(f'Готово.')
            else:
                print(f'Пользовательские аргументы не найдены.')
            if self.extensions:
                print(f'Добавление пользовательских расширений..')
                for ext in self.extensions:
                    chrome_options.add_extension(ext)
                print(f'Готово.')
            else:
                print(f'Пользовательские расширения не найдены.')
            driver = webdriver.Chrome(service=Service1(ChromeDriverManager().install()), options=chrome_options)
            print("Браузер запустился, ахуеть!")
        except Exception as e:
            print(f"Не могу запустить Chrome, пиздец: {e}")
            return

        image_urls = []
        try:
            for p in range(1, pages + 1):
                url = f"https://yandex.ru/images/search?text={query}&p={p}"
                driver.get(url)
                print(f"Зашёл на страницу ({p}), ждём, блять")
                
                # Ждём загрузку пикч
                await asyncio.sleep(10)
                
                # Скроллим
                for _ in range(scrolly):
                    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    await asyncio.sleep(2.5)
                    print("Скроллю, сука")
                
                all_images = driver.find_elements(By.TAG_NAME, "img")[:max_images]
                print(f"Всего тегов <img> на странице: {len(all_images)}")
                if all_images:
                    for img in all_images:
                        img_url = img.get_attribute("src")
                        if img_url and "http" in img_url:
                            image_urls.append(img_url)
                else:
                    print(f"Ни одного <img> не нашёл на странице {p}, пиздец полный")

        except Exception as e:
            print(f"Что-то пошло по пизде на странице {p}: {e}")

        driver.quit()
        print("Браузер закрыл, пиздец, готово")
        if proxy_plugin and os.path.exists(proxy_plugin):
            os.remove(proxy_plugin)

        # Качаем картинки
        if image_urls:
            print(f"Начинаем качать {len(image_urls)} картинок асинхронно, блять...")
            async with aiohttp.ClientSession(headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/129.0.0.0 Safari/537.36'}) as session:
                tasks = [self.download_image(session, url, directory) for url in image_urls[:max_images]]
                await tqdm.gather(*tasks, desc='Качаем картинки...', ncols=70)
        else:
            print("Нихуя не скачал, картинок нет, пиздец")
            
class TelethonThings:
    def __init__(self, app_id: int, app_hash: str, phone: str, app_version: str = '4.16.30-vxCUSTOM', system_version: str = 'Win11', device_model: str = 'FlorestTHINGS YEAH', session_name: str = 'FlorestAbobus', **attrs):
        """Короче. Класс для работы с Telegram.\nФункции: парсинг групп на аккаунте (их участники), а также массовая рассылка по никам.\nДанные берите с my.telegram.org.\napp_id: ID приложения в Telegram.\napp_hash: ключ, хэш приложения.\nphone: номер, который привязан к аккаунту.\napp_version: кастомная версия приложения.\nsystem_version: версия ОС(любая).\ndevice_model: типо имя устройства. может быть любая хрень.\nsession_name: имя сессии.\nattrs: ну короче, другие аргументы в telethon."""
        if not attrs.pop('connection', None):
            self.client = TelegramClient(session_name, app_id, app_hash, app_version=app_version, system_version=system_version, device_model=device_model, proxy=attrs.pop('proxy', None), use_ipv6=attrs.pop('use_ipv6', None), local_addr=attrs.pop('local_addr', None), timeout=attrs.pop('timeout', 10), request_retries=attrs.pop('request_retries', 5), connection_retries=attrs.pop('connection_retries', 5), retry_delay=attrs.pop('retry_delay', 1), auto_reconnect=attrs.pop('auto_reconnect', True), sequential_updates=attrs.pop('sequential_updates', False), flood_sleep_threshold=attrs.pop('flood_sleep_threshold', 60), raise_last_call_error=attrs.pop('raise_last_call_error', False), lang_code=attrs.pop('lang_code', 'en'), system_lang_code=attrs.pop('system_lang_code', 'en'), base_logger=attrs.pop('base_logger', None), receive_updates=attrs.pop('receive_updates', None), catch_up=attrs.pop('catch_up', False), entity_cache_limit=attrs.pop('entity_cache_limit', 5000))
            self.client.start(phone=phone)
        else:
            self.client = TelegramClient(session_name, app_id, app_hash, app_version=app_version, system_version=system_version, device_model=device_model, proxy=attrs.pop('proxy', None), use_ipv6=attrs.pop('use_ipv6', None), local_addr=attrs.pop('local_addr', None), timeout=attrs.pop('timeout', 10), request_retries=attrs.pop('request_retries', 5), connection_retries=attrs.pop('connection_retries', 5), retry_delay=attrs.pop('retry_delay', 1), auto_reconnect=attrs.pop('auto_reconnect', True), sequential_updates=attrs.pop('sequential_updates', False), flood_sleep_threshold=attrs.pop('flood_sleep_threshold', 60), raise_last_call_error=attrs.pop('raise_last_call_error', False), lang_code=attrs.pop('lang_code', 'en'), system_lang_code=attrs.pop('system_lang_code', 'en'), base_logger=attrs.pop('base_logger', None), receive_updates=attrs.pop('receive_updates', None), catch_up=attrs.pop('catch_up', False), entity_cache_limit=attrs.pop('entity_cache_limit', 5000), connection=attrs.pop('connection'))
            self.client.start(phone=phone)
    def parse_groups(self) -> list[dict]:
        """Парсит группу с вашего аккаунта, которую Вы выберете.\nВозвращает `list[dict]`."""
        from colorama import Fore
 
        from telethon.tl.functions.messages import GetDialogsRequest
        from telethon.tl.types import InputPeerEmpty
        import asyncio
        
        banner = f"""{Fore.GREEN}
        _____  _                          _    ____
        |  ___|| |  ___   _ __   ___  ___ | |_ |  _ \   __ _  _ __  ___   ___  _ __
        | |_   | | / _ \ | '__| / _ \/ __|| __|| |_) | / _` || '__|/ __| / _ \| '__|
        |  _|  | || (_) || |   |  __/\__ \| |_ |  __/ | (_| || |   \__ \|  __/| |
        |_|    |_| \___/ |_|    \___||___/ \__||_|     \__,_||_|   |___/ \___||_|
        """

        print(f'{banner}\n\nПарсер, созданный для людей.')
        chats = []
        last_date = None
        size_chats = 200
        groups=[]

        result = self.client(GetDialogsRequest(
            offset_date=last_date,
            offset_id=0,
            offset_peer=InputPeerEmpty(),
            limit=size_chats,
            hash = 0
            )
        )
        chats.extend(result.chats)
        for chat in chats:
            try:
                if chat.megagroup== True:
                    groups.append(chat)
            except:
                continue
            
        print(f'{Fore.YELLOW}Выберите номер группы из перечня:')
        i=0
        for g in groups:
            print(F'{Fore.GREEN}{str(i)} - {g.title}')
            i+=1
        g_index = input("Введите нужную цифру: ")
        target_group=groups[int(g_index)]

        print(f'{Fore.YELLOW}Узнаём пользователей...')
        all_participants = self.client.get_participants(target_group)

        print(f'{Fore.YELLOW}Начинаем парсить {all_participants.total} участников.')

        users = []
        
        for user in all_participants:
            users.append({"id":user.id, 'username':f'@{user.username}', 'name':user.first_name, 'surname':user.last_name, 'phone':user.phone, 'is_scam':user.scam, 'is_premium':user.premium, 'last_activity':user.status})
        print(f'{Fore.GREEN}Парсинг был проведен успешно.')
        return users
    def send_mass_messages(self, nicknames_and_ids: list[str], messages: list[str], delay: float = random.uniform(1, 7)) -> None:
        """Рассылка пользователям.\nnicknames_and_ids: ники пользователей, а также их цифровые ID.\nmessages: сообщения для отправки.\ndelay: задержки в рассылке сообщений.\nФункция возвращает `None`."""
        import time, asyncio
        import random
        from tqdm import tqdm
        
        for user in tqdm(nicknames_and_ids, desc='Рассылаем пользователям...', ncols=70):
            for message in messages:
                try:
                    time.sleep(delay)
                    self.client.send_message(user, message)
                except Exception as e:
                    print(f'Ошибка при написании {user}: {e}')
        return None
