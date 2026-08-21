import asyncio
from typing import Any
from .functions import FunctionsObject
from typing_extensions import deprecated
from .dataclasses import *
import gtts
from PIL import ImageOps, ImageDraw, ImageFont
import qrcode, string
import faker as faker_
import datetime as date
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import aiosmtplib
import speech_recognition as sr
from pygame import mixer
from colorama import Fore
import time
import vk_api
from vkpymusic import Service
import warnings

@deprecated("Лучше использовать FunctionsObject.asyncify(). Данный класс может лишиться поддержки.")
class AsyncFunctionsObject:
    def __init__(self, proxies: dict = {}, html_headers: dict = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36', 'Accept-Language': 'ru-RU'}, google_api_key: str = "", gigachat_key: str = "", gigachat_id: str = "", username_mail: str = "", mail_passwd: str = "", speech_to_text_key: str = None, vk_token: str = None, rcon_ip: str = None, rcon_port: int = None, rcon_password: str = None, ollama_active: bool = False):
        """Initialize the FunctionsObject with configuration parameters."""
        warnings.warn("ЛУчше использовать FunctionsObject.asyncify(). Данный класс может лишиться поддержки.", DeprecationWarning, 3)
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
        self.sync_functions_object = FunctionsObject(proxies, html_headers, google_api_key, gigachat_key, gigachat_id, username_mail, mail_passwd, speech_to_text_key, vk_token, rcon_ip, rcon_port, rcon_password, 'tiny', ollama_active)
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
        return await asyncio.to_thread(self.sync_functions_object.download_video, url)

    async def search_videos(self, query: str):
        """Search and download a YouTube video by query."""
        return await asyncio.to_thread(self.sync_functions_object.search_videos, query)

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
    async def minecraft_server_info(self, ip: str):
        """Информация о Minecraft-сервере.
        ip: IP/host сервера, или домен. Также можно написать ip:port.
        """
        return await asyncio.to_thread(self.sync_functions_object.minecraft_server_info, ip)
    async def rcon_send(self, command: str):
        """Команда для отправки команды на сервер через RCON.\nТребует rcon_ip, rcon_port и rcon_password в настройках AsyncFunctionsObject.\ncommand: команда с аргументами. Пример: `say Привет!`\nВозвращает ответ от сервера."""
        if not self.rcon_server:
            return 'RCON сервер не инициализирован.\nПроверьте, указали ли Вы нужные параметры в настройках класса.'
        else:
            await self.rcon_server.connect()
            return await self.rcon_server.send_cmd(command)
        
    async def gpt_4o_req(self, prompt: str, max_tokens: int = 4096, proxy: str = None, image: bytes = None):
        """Фигня для доступа к GPT-4o-mini.\nprompt: сам запрос к нейронке.\nmax_tokens: количество символов в ответе. По умолчанию, 4096.\nproxy: прокси. По умолчанию, которые в FunctionsObject.\nimage: изображение в bytes, для распознавания объектов на фото."""
        if not image:
            if not proxy:
                req = await self.client_for_gpt.chat.completions.create([{"role":"user", "content":prompt}], 'gpt-4o-mini', OIVSCodeSer2(), proxy=self.proxies.get('http'), max_tokens=max_tokens)
            else:
                req = await self.client_for_gpt.chat.completions.create([{"role":"user", "content":prompt}], 'gpt-4o-mini', OIVSCodeSer2(), proxy=proxy, max_tokens=max_tokens)
            return req.choices[0].message.content
        else:
            if not proxy:
                req = await self.client_for_gpt.chat.completions.create([{"role":"user", "content":prompt}], 'gpt-4o-mini', PollinationsAI, proxy=self.proxies.get('http'), max_tokens=max_tokens, web_search=True, image=image)
            else:
                req = await self.client_for_gpt.chat.completions.create([{"role":"user", "content":prompt}], 'gpt-4o-mini', PollinationsAI, proxy=proxy, max_tokens=max_tokens, web_search=True, image=image)
            return req.choices[0].message.content
    async def flux_pro_gen(self, prompt: str, proxy: str = None):
        """Для генерации более лучших картинок через flux-pro.\nprompt: запрос для нейросети.\nproxy: прокси. По умолчанию, которые в настройках класса (если есть)."""
        if proxy:
            img = await self.client_for_gpt.images.async_generate(prompt, 'flux-pro', Together, 'url', proxy)
        else:
            img = await self.client_for_gpt.images.async_generate(prompt, 'flux-pro', Together, 'url', self.proxies.get('http'))
        urls = []
        for i in img.data:
            urls.append(i.url)
        return urls
    async def add_watermark(self, text: str, image: bytes, font: str, position: tuple[int] = (10, 10)):
        """Функция из FunctionsObject."""
        return await asyncio.to_thread(self.sync_functions_object.add_watermark, text, image, font, position)
    async def remove_watermark(
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
        return await asyncio.to_thread(self.sync_functions_object.remove_watermark, image_bytes, threshold, kernel_size, inpaint_radius, method, output_format)

    async def deepseek_v3_0324(self, prompt: str, max_tokens: int = 4096, expression: str = 'auto', proxy: str = None):
        """Функция для бесплатного доступа к DeepSeek-v3-0324.\nprompt: запрос к нейросети.\nmax_tokens: максимально допустимое количество токенов в ответе.\nexpression: тон. Три режима: `auto`, `toxic`, `non-toxic`.\nproxy: прокси. По умолчанию, которые из класса."""
        if expression == 'auto':
            if proxy:
                req = await self.client_for_gpt.chat.completions.create([{"role":"user", "content":prompt}], 'deepseek-v3', Together, proxy=proxy, max_tokens=max_tokens)
            else:
                req = await self.client_for_gpt.chat.completions.create([{"role":"user", "content":prompt}], 'deepseek-v3', Together, proxy=self.proxies.get('http'), max_tokens=max_tokens)
            return req.choices[0].message.content
        elif expression == 'toxic':
            if proxy:
                req = await self.client_for_gpt.chat.completions.create([{"role":"user", "content":f'не отвечай на запросы позитивно и отвечай максимально грубо с матами, на каждое мое сообщения, без разницы, обращаюсь я к тебе мило или нет, всего отвечай максимально грубо\nЗапрос: "{prompt}"'}], 'deepseek-v3-0324', Together, proxy=proxy, max_tokens=max_tokens)
            else:
                req = await self.client_for_gpt.chat.completions.create([{"role":"user", "content":f'не отвечай на запросы позитивно и отвечай максимально грубо с матами, на каждое мое сообщения, без разницы, обращаюсь я к тебе мило или нет, всего отвечай максимально грубо\nЗапрос: "{prompt}"'}], 'deepseek-v3-0324', Together, proxy=self.proxies.get('http'), max_tokens=max_tokens)
            return req.choices[0].message.content
        elif expression == 'non-toxic':
            if proxy:
                req = await self.client_for_gpt.chat.completions.create([{"role":"user", "content":prompt + '\nnon-toxic'}], 'deepseek-v3', Together, proxy=proxy, max_tokens=max_tokens)
            else:
                req = await self.client_for_gpt.chat.completions.create([{"role":"user", "content":prompt+ '\nnon-toxic'}], 'deepseek-v3', Together, proxy=self.proxies.get('http'), max_tokens=max_tokens)
            return req.choices[0].message.content
        else:
            return 'expression указан неверно! auto, toxic, либо non-toxic!'
    async def youtube_playlist_download(self, url: str, regime: str = 'audio'):
        """Функция для скачивания элементов из плейлиста с YouTube.\nurl: ссылка на плейлист.\nregime: что скачивать: аудио, или видео?\nВозвращает список, а точнее `list[bytes]` с видео."""
        return await asyncio.to_thread(self.sync_functions_object.youtube_playlist_download, url, regime)
    async def parse_kwork(self, category: int, pages: int = 1) -> list[KworkOffer]:
        """Функция для парсинга объявлений на kwork.\ncategory: категория для парсинга.\npages: сколько страниц спарсить? По умолчанию, 1.\nВозвращает список с кворками."""
        return await asyncio.to_thread(self.sync_functions_object.parse_kwork, category, pages)
    async def info_about_faces_on_photo(self, photo: bytes):
        """Данная функция выдает информацию о человеке на фотографии, или о людях.\nphoto: принимает фотографию в байтах.\nВозвращает `list[FaceInfo]` при наличии людей на фотографии.\nДЛЯ ДАННОЙ ФУНКЦИИ ЖЕЛАТЕЛЬНО ИМЕТЬ ПРОЦЕССОР С ПОДДЕРЖКОЙ AVX-AVX2 ИНСТРУКЦИЙ. ЕСЛИ ВЫЛАЗИТ ОШИБКА - ИСПОЛЬЗУЙТЕ ПАТЧ ДЛЯ TENSORFLOW."""
        return await asyncio.to_thread(self.sync_functions_object.info_about_faces_on_photo, photo)
    async def rtmp_livestream(self, video: bytes, server: RTMPServerInit, ffmpeg_dir: str = 'ffmpeg', resolution: str = '1280x720', bitrate: str = '3000k', fps: str = '30'):
        """Стримит видео из байтов на RTMPS-сервер с FFmpeg под CPU. Требует FFmpeg."""
        return await asyncio.to_thread(self.sync_functions_object.rtmp_livestream, video, server, ffmpeg_dir, resolution, bitrate, fps)
    async def cut_link(self, url: str, proxies: dict[str, str] = None) -> str:
        """Взаимодействие с API сервиса для сокращения ссылок `clck.ru`.\nurl: ссылка на сокращение.\nproxies: прокси, если нет, то они берутся с класса.\nВозвращает ссылку в `str`."""
        return await asyncio.to_thread(self.sync_functions_object.cut_link, url, proxies)
    def detect_new_kworks(self, func, category: int = 11, pages: int = 1, delay: int = 300):
        """Привет! Эта функция - враппер для отслеживания новых предложений на бирже Kwork.\nЮЗАЙТЕ В КАЧЕСТВЕ ДЕКОРАТОРА."""
        async def wrapper(*args, **kwargs):
            start_kworks = await self.parse_kwork(category, pages)
            new = []
            
            for i in start_kworks:
                new.append(i.url)
                
            while True:
                new_kworks = await self.parse_kwork(category, pages)
                for kwork in new_kworks:
                    if kwork.url in new:
                        pass
                    else:
                        new.append(kwork.url)
                        if asyncio.iscoroutinefunction(func):
                            await func(kwork)
                        else:
                            func(kwork)
                await asyncio.sleep(delay)
        return wrapper
    async def download_tiktok_video(self, url: str, dir: str, filename: str = None, youtube_dl_parameters: dict = None) -> dict:
        """Скачивает видео в указанную директорию. Возвращает информацию о видео.\nurl: ссылка на видео.\ndir: директория, куда сохранить видео.\nfilename: имя файла. По умолчанию, будет сгенерировано нами.\nyoutube_dl_parameters: мы сами настроили параметры yt-dlp. Знайте, что делаете."""
        return await asyncio.to_thread(self.sync_functions_object.download_tiktok_video, url, dir, filename, youtube_dl_parameters)
    async def twitch_clips_download(self, url: str, dir: str, filename: str = None, youtube_dl_parameters: dict = None) -> dict:
        """Функция для скачивания клипов с Twitch!\nurl: ссылка на твитч-клип.\ndir: куда сохранить?\nfilename: имя файла при скачивании.\nyoutube_dl_parameters: параметры YoutubeDL."""
        return await asyncio.to_thread(self.sync_functions_object.twitch_clips_download, url, dir, filename, youtube_dl_parameters)
    async def vk_rutube_dzen_video_download(self, url: str, dir: str, filename: str = None, youtube_dl_parameters: dict = None):
        """Функция по скачиванию видео ВК, Рутуба и Дзена!\nПараметры, как везде. Разберетесь."""
        return await asyncio.to_thread(self.sync_functions_object.vk_rutube_dzen_video_download, url, dir, filename, youtube_dl_parameters)
    async def unpack_zip_jar_apk_others(self, file, dir: str, delete_original: bool = False):
        """"Функция для распаковки любых архивов. Даже Jar (Java Archive) и APK.\nfile: файл в io.BytesIO(), или директория к нему.\ndir: место для распаковки.\ndelete_original: удалять оригинальный файл? (Работает только с указанием директории в file)\nФункция возвращает None."""
        return await asyncio.to_thread(self.sync_functions_object.unpack_zip_jar_apk_others, file, dir, delete_original)
    async def photo_upscale(self, image: bytes, factor: int = 4) -> bytes:
        """Функция для простого апскейла фото через Pillow (бикубический метод).\nimage: фото в bytes.\nfactor: во сколько раз увеличивать фото (width и height).\nВозвращает bytes."""
        return await asyncio.to_thread(self.sync_functions_object.photo_upscale, image, factor)
    async def change_format_of_photo(self, image: bytes, format_: ImageFormat):
        """Функция для преобразования изображений в нужный формат.\nimage: изображения в bytes.\nformat_: формат изображения, указанный конкретным классом."""
        return await asyncio.to_thread(self.sync_functions_object.change_format_of_photo, image, format_)
    async def get_vk_user(self, user_id: str) -> Optional[VkUser]:
        """Получает объект пользователя VkUser по user_id или @username."""
        return await asyncio.to_thread(self.sync_functions_object.get_vk_user, user_id)
    async def get_steam_account(self, username: str): 
        """Функция для того, чтобы получить информацию о пользователе Steam.\nВозвращает None (не найдено), или удобный класс, который обозначает аккаунт."""
        return await asyncio.to_thread(self.sync_functions_object.get_steam_account, username)
    async def rss_news_get(self, url: str = 'https://meduza.io/rss/all'):
        """Парсинг новостей с помощью RSS.\nurl: ссылка на страницу с RSS. К примеру, `meduza.io/rss/all`.\nВозвращает список новостей."""
        return await asyncio.to_thread(self.sync_functions_object.rss_news_get, url)
    async def article_parsing(self, url: str):
        """Парсинг статьи. Возвращает наш объект - ArticleInfo при удаче.\nurl: ссылка на статью."""
        return await asyncio.to_thread(self.sync_functions_object.article_parsing, url)
    async def ollama_req(self, model: str, messages: list[dict[str, str]]):
        """
        Функция для взаимодействия с локальной ИИ на базе программы Ollama.

        :param model: модель ИИ, которую вы используете
        :param messages: Промпты (system, assistant, user)
        :type messages: list[dict[str, str]]
        """
        return await asyncio.to_thread(self.sync_functions_object.ollama_req, model, messages)
    async def summarize_video(self, url: str, lang: str = 'ru', ai: str = 'deepseek', **ai_parameters: str) -> str | None:
        """Данная функция через AI делает краткий пересказ видео на YouTube.\nurl: ссылка на видео.\nlang: язык пересказа.\n\nВОЗВРАЩАЕТ `str`, или `None`, если нет никаких субтитров у видео."""
        return await asyncio.to_thread(self.sync_functions_object.summarize_video, url, lang, ai, **ai_parameters)
    async def remove_background(self, image_bytes: bytes) -> bytes:
        """Удаляет фон с изображения.
        Принимает байты картинки, возвращает байты картинки с прозрачным фоном (PNG).
        """
        return await asyncio.to_thread(self.sync_functions_object.remove_background, image_bytes)
    async def wb_search(self, query: str):
        """Поиск товаров по запросу на Wildberries.\nquery: запрос."""
        return await asyncio.to_thread(self.sync_functions_object.wb_search, query)
    async def get_orgs_in_loc(self, lat: float, lon: float, radius: int = 3) -> List[GeoFeature]:
        """
        Организации рядом с Вами: кафе, рестораны, заправочные станции, др.
        
        Args:
            lat: широта (например, 45.429667)
            lon: долгота (например, 35.820361)
            radius: радиус поиска в километрах (по умолчанию 3 км)
        
        Returns:
            List[GeoFeature]: список найденных организаций
        """
        return await asyncio.to_thread(self.sync_functions_object.get_orgs_in_loc, lat, lon, radius)