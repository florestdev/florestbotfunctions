# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import os, re
import random, requests
import aiohttp
import asyncio
import zipfile
from .dataclasses import *
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


class AsyncYandexParser:
    """
    Асинхронный парсер изображений с Яндекс.Картинок.
    Поддерживаются приватные HTTP(S)-прокси с авторизацией.
    Требуется установленный Google Chrome.

    Параметры:
        proxy_host, proxy_port, proxy_user, proxy_pass — прокси.
        is_headless — запуск браузера без окна.
        arguments — дополнительные аргументы Chrome.
        extensions — дополнительные расширения Chrome (.crx).
    """

    def __init__(
        self,
        proxy_host: str = None,
        proxy_port: int = None,
        proxy_user: str = None,
        proxy_pass: str = None,
        is_headless: bool = False,
        arguments: list[str] = None,
        extensions: list[str] = None
    ):
        self.proxy_host = proxy_host
        self.proxy_port = proxy_port
        self.proxy_user = proxy_user
        self.proxy_pass = proxy_pass
        self.isheadless = is_headless
        self.arguments = arguments
        self.extensions = extensions

        print("Парсер успешно инициализирован. "
              "Используйте функцию start_parsing для начала работы.")

    def create_proxy_auth_extension(self):
        """
        Создаёт временное расширение Chrome для авторизации прокси.
        """

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
            """ % (
                self.proxy_host,
                self.proxy_port,
                self.proxy_user,
                self.proxy_pass
            )

            plugin_file = "proxy_auth_plugin.zip"
            with zipfile.ZipFile(plugin_file, "w") as zp:
                zp.writestr("manifest.json", manifest_json)
                zp.writestr("background.js", background_js)

            return plugin_file

        return None

    async def download_image(self, session: aiohttp.ClientSession, img_url: list[str]):
        """
        Асинхронная загрузка изображений.
        Возвращает list[YandexImage].
        """

        images: list[YandexImage] = []

        if not all([self.proxy_host, self.proxy_port, self.proxy_user, self.proxy_pass]):
            # Без прокси
            for url in tqdm(img_url, desc="Скачиваем изображения...", ncols=70):
                if url.startswith(("http://", "https://")):
                    try:
                        async with session.get(url) as response:
                            if response.status == 200:
                                images.append(
                                    YandexImage({"data": await response.read(), "url": url})
                                )
                    except:
                        pass
        else:
            # С прокси
            proxy_auth = aiohttp.BasicAuth(
                login=self.proxy_user,
                password=self.proxy_pass
            )
            proxy_url = f"http://{self.proxy_host}:{self.proxy_port}"

            for url in tqdm(img_url, desc="Скачиваем изображения...", ncols=70):
                try:
                    if url.startswith(("http://", "https://")):
                        async with session.get(
                            url,
                            proxy=proxy_url,
                            proxy_auth=proxy_auth
                        ) as response:
                            if response.status == 200:
                                images.append(
                                    YandexImage({"data": await response.read(), "url": url})
                                )
                except:
                    pass

        return images

    async def start_parsing(self, query: str, max_images=10, scrolly=5, pages: int = 6):
        """
        Запуск парсинга изображений.

        Параметры:
            query — поисковый запрос.
            max_images — максимальное количество изображений на странице.
            scrolly — количество прокруток.
            pages — количество страниц для парсинга.
        """

        try:
            proxy_plugin = self.create_proxy_auth_extension()

            chrome_options = Options()
            chrome_options.add_argument("--log-level=1")

            if proxy_plugin:
                chrome_options.add_extension(proxy_plugin)

            if self.isheadless:
                chrome_options.add_argument("--headless")

            if self.arguments:
                print("Добавление пользовательских аргументов...")
                for arg in self.arguments:
                    chrome_options.add_argument(arg)
                print("Пользовательские аргументы добавлены.")
            else:
                print("Пользовательские аргументы отсутствуют.")

            if self.extensions:
                print("Добавление пользовательских расширений...")
                for ext in self.extensions:
                    chrome_options.add_extension(ext)
                print("Расширения добавлены.")
            else:
                print("Пользовательские расширения отсутствуют.")

            driver = webdriver.Chrome(
                service=Service1(ChromeDriverManager().install()),
                options=chrome_options
            )
            print("Браузер успешно запущен.")

        except Exception as e:
            print(f"Ошибка запуска браузера: {e}")
            return

        image_urls = []

        try:
            for p in range(1, pages + 1):
                url = f"https://yandex.ru/images/search?text={query}&p={p}"
                driver.get(url)
                print(f"Открыта страница №{p}. Ожидание загрузки...")

                await asyncio.sleep(10)

                for _ in range(scrolly):
                    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    await asyncio.sleep(2.5)
                    print("Прокрутка страницы...")

                all_images = driver.find_elements(By.TAG_NAME, "img")
                print(f"Найдено тегов <img>: {len(all_images)}")

                if all_images:
                    for img in all_images[:max_images]:
                        img_url = img.get_attribute("src")
                        if img_url and "http" in img_url:
                            image_urls.append(img_url)
                else:
                    print(f"На странице {p} изображения не найдены.")

        except Exception as e:
            print(f"Ошибка обработки страницы {p}: {e}")

        finally:
            driver.quit()
            print("Браузер закрыт.")

            if proxy_plugin and os.path.exists(proxy_plugin):
                os.remove(proxy_plugin)

        if image_urls:
            print(f"Начинается загрузка {len(image_urls)} изображений...")

            async with aiohttp.ClientSession(
                headers={
                    "User-Agent":
                        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                        "AppleWebKit/537.36 (KHTML, like Gecko) "
                        "Chrome/129.0.0.0 Safari/537.36"
                }
            ) as client:
                return await self.download_image(client, image_urls)
        else:
            print("Изображения для загрузки не найдены.")
            return None

    def filter_by_resolution(self, images: list[YandexImage], resolutions: list[Resolution]):
        """
        Фильтрация изображений по разрешению.

        Возвращает список изображений, подходящих под заданные параметры.
        """

        from tqdm import tqdm as sync_tqdm

        resolutions_dict = [res.data for res in resolutions]
        new_images: list[YandexImage] = []

        for image in sync_tqdm(images, 'Фильтрация изображений...', ncols=70):
            if image.get_resolution().data in resolutions_dict:
                new_images.append(image)

        return new_images

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
