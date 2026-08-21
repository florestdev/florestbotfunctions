"""Dataclasses of florestbotfunctions."""
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import os, re
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
from bs4 import BeautifulSoup
from PIL import Image
import io

class SearchResultImage:
    def __init__(self, title: str, image: str, thumbnail: str, url: str,
                 height: int, width: int, source: str):
        self._title = title
        self._image = image
        self._thumbnail = thumbnail
        self._url = url
        self._height = height
        self._width = width
        self._source = source

    @property
    def title(self) -> str:
        return self._title

    @property
    def image(self) -> str:
        return self._image

    @property
    def thumbnail(self) -> str:
        return self._thumbnail

    @property
    def url(self) -> str:
        return self._url

    @property
    def height(self) -> int:
        return self._height

    @property
    def width(self) -> int:
        return self._width

    @property
    def source(self) -> str:
        return self._source

    @property
    def aspect_ratio(self) -> float:
        """Вычисляет соотношение сторон изображения"""
        return self._width / self._height if self._height else 0

    def __repr__(self):
        return f"SearchResultImage(title={self._title!r}, url={self._url!r})"

class SearchResult:
    def __init__(self, data: dict):
        self.data = data
    @property
    def title(self):
        """Название сайта из выдачи."""
        return self.data.get('title')
    @property
    def body(self):
        """Описание сайта."""
        return self.data.get('body')
    @property
    def href(self):
        """Ссылка на сайт."""
        return self.data.get('href')
    def __str__(self):
        return f'Название: {self.title}\nОписание: {self.body}\nСсылка на сайт: {self.href}'

class Donate:
    """
    Класс-обёртка над словарём события DonationAlerts.
    Позволяет получать данные события через свойства (property).
    """

    def __init__(self, data: Dict[str, Any]):
        if not isinstance(data, dict):
            raise TypeError("Donate data must be a dict")
        self._data = data

    # ---- Основные свойства ---- #

    @property
    def id(self) -> int:
        """Уникальный ID доната."""
        return int(self._data.get("id", 0))

    @property
    def alert_type(self) -> str:
        """Тип алерта (donation, subscription, etc)."""
        return self._data.get("alert_type", "")

    @property
    def is_shown(self) -> str:
        """Показывать ли оповещение на экране."""
        return self._data.get("is_shown", "")

    @property
    def additional_data(self) -> dict:
        """Дополнительная информация о донате."""
        return self._data.get("additional_data", {})

    @property
    def billing_system(self) -> str:
        """Название платёжной системы."""
        return self._data.get("billing_system", "")

    @property
    def billing_system_type(self) -> str:
        """Тип платёжной системы."""
        return self._data.get("billing_system_type", "")

    @property
    def username(self) -> str:
        """Имя донатера."""
        return self._data.get("username", "")

    @property
    def amount(self) -> float:
        """Сумма доната (как float)."""
        try:
            return float(self._data.get("amount", 0))
        except ValueError:
            return 0.0

    @property
    def amount_str(self) -> str:
        """Сумма как строка."""
        return self._data.get("amount", "0")

    @property
    def amount_formatted(self) -> str:
        """Красиво форматированная сумма (например: 100 ₽)."""
        return self._data.get("amount_formatted", "")

    @property
    def amount_main(self) -> int:
        """Округлённая сумма (целое число)."""
        return int(self._data.get("amount_main", 0))

    @property
    def currency(self) -> str:
        """Валюта доната (RUB, USD, EUR...)."""
        return self._data.get("currency", "")

    @property
    def message(self) -> str:
        """Сообщение донатера."""
        return self._data.get("message", "")

    @property
    def header(self) -> str:
        """Заголовок доната."""
        return self._data.get("header", "")

    @property
    def date_created(self) -> Any:
        """Дата создания доната."""
        return self._data.get("date_created")

    @property
    def emotes(self) -> str:
        """Эмодзи, прикреплённые к сообщению."""
        return self._data.get("emotes", "")

    @property
    def ap_id(self) -> str:
        """Application ID."""
        return self._data.get("ap_id", "")

    @property
    def is_test_alert(self) -> bool:
        """Проверочный ли это донат."""
        return bool(self._data.get("_is_test_alert", False))

    @property
    def message_type(self) -> str:
        """Тип сообщения (text, tts?)."""
        return self._data.get("message_type", "")

    @property
    def preset_id(self) -> int:
        """ID пресета алерта."""
        return int(self._data.get("preset_id", 0))

    @property
    def objects(self) -> dict:
        """Вложенные объекты DonationAlerts."""
        return self._data.get("objects", {})

    # ---- Утилиты ---- #

    def to_dict(self) -> Dict[str, Any]:
        """Получить исходный словарь полностью."""
        return self._data
    
class Voter:
    def __init__(self, _data: dict):
        self._data = _data
    @property
    def username(self):
        """Ник голосующего."""
        return self._data.get('username')
    @property
    def votes(self):
        """Количество голосов."""
        return self._data.get('votes')

class HotMCServer:

    def __init__(self, data: dict, url: str):
        self._data = data or {}
        self.url = url or 'none'

    # ----------------------- Базовая информация -----------------------

    @property
    def title(self):
        return self._data.get("title")

    @property
    def description(self):
        return self._data.get("description")

    @property
    def ip(self):
        return self._data.get("ip")

    @property
    def bedrock_ip(self):
        return self._data.get("bedrock_ip")

    @property
    def versions(self):
        return self._data.get("versions", [])

    @property
    def status(self):
        return self._data.get("status")

    @property
    def players_online(self):
        return self._data.get("players_online")

    @property
    def rating_position(self):
        return self._data.get("rating_position")

    @property
    def votes(self):
        return self._data.get("votes")

    @property
    def site(self):
        return self._data.get("site")

    # ----------------------- Uptime / графики -----------------------

    @property
    def uptime_text(self):
        return self._data.get("uptime_text")

    @property
    def uptime_dataset(self):
        return self._data.get("uptime_dataset")

    @property
    def players_time_series(self):
        return self._data.get("players_time_series", [])

    # ----------------------- Мобы -----------------------

    @property
    def mobs(self):
        """Возвращает список мобов: [{'name':..., 'count':...}, ...]"""
        return self._data.get("mobs", [])

    # ----------------------- Теги -----------------------

    @property
    def tags(self):
        """Возвращает словарь: { 'Особенности': [...], ... }"""
        return self._data.get("tags", {})

    # ----------------------- Ссылки / изображения -----------------------

    @property
    def links(self):
        return self._data.get("links", [])

    @property
    def images(self):
        return self._data.get("images", [])

    # ----------------------- Удобные методы форматирования -----------------------

    @property
    def mobs_text(self):
        if not self.mobs:
            return "Нет данных"
        return "\n".join(f"• {m.get('name')} × {m.get('count')}" for m in self.mobs)

    @property
    def tags_text(self):
        if not self.tags:
            return "Нет тегов"
        txt = []
        for group, items in self.tags.items():
            txt.append(f"<b>{group}:</b> {', '.join(items)}")
        return "\n".join(txt)

    @property
    def players_graph_info(self):
        if not self.players_time_series:
            return "Нет данных"
        return f"{len(self.players_time_series)} точек графика"
    
    def get_voters(self):
        """Дает подробный список тех, кто голосовал за сервер."""
        m = re.search(r"-(\d+)$", self.url)
        if m:
            id__ = m.group(1)
        else:
            id__ = None

        votes_list = []

        if id__:
            headers2 = {"User-Agent":"Mozilla/5.0"}
            start_html = requests.get(
                f'https://hotmc.ru/vote-{id__}',
                headers=headers2
            ).text

            soup = BeautifulSoup(start_html, "html.parser")
            table = soup.find("table", class_="table table-hover table-condensed table-striped")

            if table:
                tbody = table.find("tbody")
                if tbody:
                    rows = tbody.find_all("tr")
                    for row in rows:
                        cols = row.find_all("td")
                        if len(cols) >= 2:
                            nick = cols[0].text.strip()
                            count = int(cols[1].text.strip())
                            votes_list.append((nick, count))
            return [Voter({"username":i[0], "votes":i[1]}) for i in votes_list]

    # ----------------------- Готовый форматированный вывод -----------------------

    def format(self) -> str:
        return f"""
<b>{self.title}</b>

{self.description}

<b>Адрес:</b>
• Java: <code>{self.ip}</code>
• Bedrock: <code>{self.bedrock_ip}</code>

<b>Версии:</b> {", ".join(self.versions)}

<b>Статус:</b> {self.status}
<b>Онлайн:</b> {self.players_online}
<b>Рейтинг HotMC:</b> {self.rating_position}
<b>Голоса:</b> {self.votes}

<b>Сайт:</b> {self.site}

<b>Uptime:</b> {self.uptime_text}

<b>График онлайна:</b>
{self.players_graph_info}

<b>Коллекция мобов:</b>
{self.mobs_text}

<b>Теги:</b>
{self.tags_text}
""".strip()
    def __str__(self):
        return self.format()

class ArticleInfo:
    def __init__(self, data: dict):
        self.data = data
    @property
    def title(self):
        """Заголовок статьи."""
        return self.data.get('title')
    @property
    def text(self):
        """Содержание статьи."""
        return self.data.get('text')
    @property
    def top_image(self):
        """Главное изображение на странице (ссылка)."""
        return self.data.get('top_image')
    def download_top_image(self):
        """Скачивает изображение и возвращает в bytes."""
        try:
            r = requests.get(self.top_image, headers={"User-Agent":"Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:15.0) Gecko/20100101 Firefox/15.0.1"})
            if r.status_code != 200:
                return
            else:
                return r.content
        except:
            return

class MinecraftServer:
    """Информация о Minecraft-сервере."""

    def __init__(self, data: dict):
        self._data = data  # защищённый атрибут

    # ====== Свойства ======

    @property
    def online(self) -> bool:
        return self._data.get("online", False)

    @property
    def ip(self) -> str:
        return self._data.get("ip", "—")

    @property
    def motd(self) -> str:
        motd_data = self._data.get("motd", {}).get("clean", [])
        return "\n".join(motd_data) if motd_data else "—"

    @property
    def version(self) -> str:
        return self._data.get("version", "—")

    @property
    def software(self) -> str:
        return self._data.get("software", "—")

    @property
    def map(self) -> str:
        return self._data.get("map", "—")

    @property
    def players_online(self) -> int:
        return self._data.get("players", {}).get("online", 0)

    @property
    def players_max(self) -> int:
        return self._data.get("players", {}).get("max", 0)

    @property
    def players_list(self) -> list[str]:
        return self._data.get("players", {}).get("list", [])

    @property
    def icon(self) -> str | None:
        return self._data.get("icon")
    
    def hotmc_search(self, debug: bool = False, proxies: dict[str, str] = {}):
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
            "ServerAddressCollector[address]": self.ip,
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

    # ====== Строковое представление ======

    def __str__(self):
        status = "🟢 Онлайн" if self.online else "🔴 Оффлайн"
        return (
            f"{status} — {self.ip}\n"
            f"Версия: {self.version}\n"
            f"Игроки: {self.players_online}/{self.players_max}\n"
            f"MOTD: {self.motd}"
        )


class News:
    def __init__(self, data: dict[str, str]):
        self._data = data  # защищённый атрибут

    # Название новости
    @property
    def title(self) -> str:
        return self._data.get("title", "—")

    # Ссылка на новость
    @property
    def link(self) -> str:
        return self._data.get("link", "—")

    # Дата публикации
    @property
    def published(self) -> str:
        return self._data.get("published", "—")

    # Краткое описание
    @property
    def description(self) -> str:
        return self._data.get("description", "—")

    # Строковое представление для печати
    def __str__(self):
        return f"{self.title} - {self.published}\n{self.link}"

class SteamUser:
    """
    Класс для представления пользователя Steam на основе данных JSON, полученных, например, из Steam API.
    
    Attributes
    ----------
    data : dict
        Исходные данные пользователя Steam в формате словаря.
    """

    def __init__(self, data: dict):
        """
        Инициализация объекта SteamUser.

        Parameters
        ----------
        data : dict
            Словарь с информацией о пользователе Steam.
        """
        self.data = data

    @property
    def steam_id64(self) -> str:
        """64-битный SteamID пользователя."""
        return self.data.get('steamID64')

    @property
    def steam_id(self) -> str:
        """Псевдоним пользователя (логин в Steam)."""
        return self.data.get('steamID')

    @property
    def online_state(self) -> str:
        """Текущее состояние пользователя (online, offline, in-game и т.д.)."""
        return self.data.get('onlineState')

    @property
    def state_message(self) -> str:
        """Сообщение, связанное с состоянием пользователя (например, 'Offline', 'In-Game')."""
        return self.data.get('stateMessage')

    @property
    def privacy_state(self) -> str:
        """Статус приватности профиля (public, private и т.п.)."""
        return self.data.get('privacyState')

    @property
    def visibility_state(self) -> int:
        """Цифровое значение уровня видимости профиля."""
        val = self.data.get('visibilityState')
        return int(val) if val is not None and val.isdigit() else None

    @property
    def avatar_icon(self) -> str:
        """URL иконки аватара (малый размер)."""
        return self.data.get('avatarIcon')

    @property
    def avatar_medium(self) -> str:
        """URL среднего размера аватара."""
        return self.data.get('avatarMedium')

    @property
    def avatar_full(self) -> str:
        """URL аватара полного размера."""
        return self.data.get('avatarFull')

    @property
    def vac_banned(self) -> bool:
        """True, если пользователь VAC-забанен."""
        return self.data.get('vacBanned') == '1'

    @property
    def trade_ban_state(self) -> str:
        """Состояние торгового бана (например, 'None', 'Probation' и т.д.)."""
        return self.data.get('tradeBanState')

    @property
    def is_limited_account(self) -> bool:
        """True, если аккаунт ограничен (например, из-за отсутствия покупок)."""
        return self.data.get('isLimitedAccount') == '1'

    @property
    def custom_url(self) -> str:
        """Пользовательский URL профиля (steamcommunity.com/id/...)."""
        return self.data.get('customURL')

    @property
    def member_since(self) -> str:
        """Дата регистрации пользователя в Steam."""
        return self.data.get('memberSince')

    @property
    def steam_rating(self) -> float | None:
        """Рейтинг Steam пользователя (может отсутствовать)."""
        val = self.data.get('steamRating')
        try:
            return float(val) if val is not None else None
        except ValueError:
            return None

    @property
    def hours_played_2wk(self) -> float:
        """Количество часов, сыгранных за последние 2 недели."""
        val = self.data.get('hoursPlayed2Wk')
        try:
            return float(val)
        except (ValueError, TypeError):
            return 0.0

    @property
    def headline(self) -> str:
        """Краткий заголовок профиля (может быть None)."""
        return self.data.get('headline')

    @property
    def location(self) -> str:
        """Местоположение пользователя."""
        return self.data.get('location')

    @property
    def realname(self) -> str:
        """Настоящее имя пользователя."""
        return self.data.get('realname')

    @property
    def summary(self) -> str:
        """Описание профиля пользователя (HTML-теги <br> заменяются на перенос строки)."""
        summary = self.data.get('summary', '')
        return summary.replace('<br>', '\n') if summary else ''

    def __str__(self) -> str:
        """
        Возвращает краткое текстовое представление пользователя.
        """
        return (
            f"SteamUser({self.steam_id})\n"
            f"Имя: {self.realname}\n"
            f"Статус: {self.online_state} ({self.state_message})\n"
            f"Профиль: https://steamcommunity.com/id/{self.custom_url}\n"
            f"Регистрация: {self.member_since}\n"
            f"Местоположение: {self.location}\n"
            f"VAC бан: {'Да' if self.vac_banned else 'Нет'} | "
            f"Ограничен: {'Да' if self.is_limited_account else 'Нет'}"
        )

class VkUser:
    """ООП-модель пользователя ВКонтакте с доступом ко всем метаданным."""

    def __init__(self, data: Dict[str, Any]):
        self._data = data

    # 🔹 Основные данные
    @property
    def id(self) -> int:
        return self._data.get("id")

    @property
    def first_name(self) -> str:
        return self._data.get("first_name", "")

    @property
    def last_name(self) -> str:
        return self._data.get("last_name", "")

    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}".strip()

    @property
    def domain(self) -> str:
        return self._data.get("domain", "")

    @property
    def profile_url(self) -> str:
        return f"https://vk.com/{self.domain or 'id' + str(self.id)}"

    # 🔹 Демография
    @property
    def sex(self) -> str:
        return {1: "женский", 2: "мужской"}.get(self._data.get("sex"), "не указан")

    @property
    def bdate(self) -> Optional[str]:
        return self._data.get("bdate")

    @property
    def city(self) -> Optional[str]:
        return self._data.get("city", {}).get("title")

    @property
    def country(self) -> Optional[str]:
        return self._data.get("country", {}).get("title")

    @property
    def home_town(self) -> Optional[str]:
        return self._data.get("home_town")

    # 🔹 Социальные данные
    @property
    def followers(self) -> int:
        return self._data.get("followers_count", 0)

    @property
    def status(self) -> str:
        return self._data.get("status", "")

    @property
    def about(self) -> str:
        return self._data.get("about", "")

    @property
    def relation(self) -> str:
        relations = {
            0: "не указано", 1: "не женат/не замужем", 2: "есть друг/подруга",
            3: "помолвлен(а)", 4: "в браке", 5: "всё сложно",
            6: "в активном поиске", 7: "влюблён(а)", 8: "в гражданском браке"
        }
        return relations.get(self._data.get("relation"), "не указано")

    # 🔹 Контакты
    @property
    def mobile_phone(self) -> Optional[str]:
        return self._data.get("mobile_phone")

    @property
    def home_phone(self) -> Optional[str]:
        return self._data.get("home_phone")

    @property
    def site(self) -> Optional[str]:
        return self._data.get("site")

    @property
    def photo(self) -> str:
        return self._data.get("photo_max_orig", "")

    # 🔹 Образование и работа
    @property
    def university(self) -> str:
        return self._data.get("university_name", "")

    @property
    def faculty(self) -> str:
        return self._data.get("faculty_name", "")

    @property
    def graduation(self) -> Optional[int]:
        return self._data.get("graduation")

    @property
    def schools(self) -> List[Dict[str, Any]]:
        return self._data.get("schools", [])

    @property
    def career(self) -> List[Dict[str, Any]]:
        return self._data.get("career", [])

    @property
    def occupation(self) -> Optional[str]:
        occ = self._data.get("occupation")
        return occ.get("name") if occ else None

    # 🔹 Интересы
    @property
    def interests(self) -> str:
        return self._data.get("interests", "")

    @property
    def activities(self) -> str:
        return self._data.get("activities", "")

    @property
    def music(self) -> str:
        return self._data.get("music", "")

    @property
    def movies(self) -> str:
        return self._data.get("movies", "")

    @property
    def books(self) -> str:
        return self._data.get("books", "")

    @property
    def games(self) -> str:
        return self._data.get("games", "")

    @property
    def quotes(self) -> str:
        return self._data.get("quotes", "")

    # 🔹 Приватные и доп. поля
    @property
    def personal(self) -> Dict[str, Any]:
        return self._data.get("personal", {})

    @property
    def connections(self) -> Dict[str, Any]:
        return self._data.get("connections", {})

    # 🔹 Удобный вывод
    def summary(self) -> str:
        return (
            f"👤 {self.full_name}\n"
            f"Пол: {self.sex}\n"
            f"Дата рождения: {self.bdate or '—'}\n"
            f"Город: {self.city or '—'}, Страна: {self.country or '—'}\n"
            f"Статус: {self.status}\n"
            f"О себе: {self.about}\n"
            f"Подписчиков: {self.followers}\n"
            f"Профиль: {self.profile_url}"
        )


class ImageFormat:
    """Введите формат изображения. Поддерживаются: `.jpg`, `.webp`, `.gif`, `.bmp`, `.png`."""
    def __init__(self, format_: str):
        """Введите формат изображения. Поддерживаются: `.jpg`, `.webp`, `.gif`, `.bmp`, `.png`."""
        self.format_ = format_
        if format_ in ['.jpg', '.webp', '.gif', '.bmp', '.png']:
            return
        else:
            raise Exception("Неизвестный формат изображения.")

class RTMPServerInit:
    def __init__(self, url: str, key: str, user: str = None, password: str = None):
        """Ну, короче, инициализация класса для rtmp_livestream().\nurl: ссылОЧКА на RTMP. Пример: `rtmp://live.twitch.tv/app`.\nkey: ключ потока.\nuser: имя пользователя. Нигде не используется.\npassword: пароль. Нигде не используется."""
        self.key = key
        self.user = user
        self.password = password
        if url.startswith('rtmps://'):
            if not all([user, password]):
                self.url = url
            else:
                self.url = url.replace('rtmps://', f'rtmps://{user}:{password}@')
        else:
            if not all([user, password]):
                self.url = url
            else:
                self.url = url.replace('rtmp://', f'rtmp://{user}:{password}@')

class FaceInfo:
    def __init__(self, info: dict):
        self.info = info
    @property
    def gender(self):
        """Возвращаем пол человека на фотографии."""
        return self.info.get('gender')
    @property
    def race(self):
        """Возвращаем расу человека на фотографии."""
        return self.info.get('race')
    @property
    def age(self):
        """Возвращаем возраст человека на фотографии."""
        return self.info.get('age')
    @property
    def emotion(self):
        """Возвращаем эмоцию человека на фотографии."""
        return self.info.get('emotion')

class KworkOffer:
    def __init__(self, data: dict):
        self._data = data

    # Основные свойства для прямого доступа к простым полям
    @property
    def id(self) -> int:
        """ID оффера"""
        return self._data.get('id', 0)

    @property
    def status(self) -> str:
        """Статус оффера"""
        return self._data.get('status', '')

    @property
    def name(self) -> str:
        """Название оффера"""
        return self._data.get('name', '')

    @property
    def description(self) -> str:
        """Описание оффера"""
        return self._data.get('description', '')

    @property
    def price_limit(self) -> float:
        """Лимит цены"""
        return float(self._data.get('priceLimit', '0.00'))

    @property
    def possible_price_limit(self) -> int:
        """Возможный лимит цены"""
        return self._data.get('possiblePriceLimit', 0)

    @property
    def max_days(self) -> int:
        """Максимальная длительность выполнения в днях"""
        return int(self._data.get('max_days', '0'))

    @property
    def time_left(self) -> str:
        """Оставшееся время до истечения"""
        return self._data.get('timeLeft', '')

    @property
    def is_active(self) -> bool:
        """Активен ли оффер"""
        return self._data.get('isWantActive', False)

    @property
    def is_archived(self) -> bool:
        """Заархивирован ли оффер"""
        return self._data.get('isWantArchive', False)

    # Доступ к данным пользователя
    @property
    def user_id(self) -> int:
        """ID пользователя"""
        return self._data.get('user', {}).get('USERID', 0)

    @property
    def username(self) -> str:
        """Имя пользователя"""
        return self._data.get('user', {}).get('username', '')

    @property
    def user_profile_url(self) -> str:
        """URL профиля пользователя"""
        return self._data.get('wantUserGetProfileUrl', '')

    # Доступ к датам
    def get_date(self, date_type: str) -> str:
        """
        Получить дату из wantDates по типу (create, active, expire, reject)
        """
        return self._data.get('wantDates', {}).get(f'date{date_type.capitalize()}', '')

    @property
    def date_create(self) -> str:
        """Дата создания оффера"""
        return self.get_date('create')

    @property
    def date_active(self) -> str:
        """Дата активации оффера"""
        return self.get_date('active')

    @property
    def date_expire(self) -> str:
        """Дата истечения оффера"""
        return self.get_date('expire')

    # Доступ к статусу (altStatusHint)
    @property
    def status_color(self) -> str:
        """Цвет статуса"""
        return self._data.get('altStatusHint', {}).get('color', '')

    @property
    def status_title(self) -> str:
        """Название статуса"""
        return self._data.get('altStatusHint', {}).get('title', '')

    # Доступ к данным о бейджах пользователя
    def get_user_badges(self) -> list[dict]:
        """Список бейджей пользователя"""
        return self._data.get('user', {}).get('badges', [])

    @property
    def user_badge_titles(self) -> list[str]:
        """Список названий бейджей пользователя"""
        return [badge.get('badge', {}).get('title', '') for badge in self.get_user_badges()]

    # Доступ к статистике
    @property
    def wants_count(self) -> int:
        """Количество офферов пользователя"""
        return int(self._data.get('user', {}).get('data', {}).get('wants_count', '0'))

    @property
    def wants_hired_percent(self) -> int:
        """Процент нанятых по офферам"""
        return int(self._data.get('user', {}).get('data', {}).get('wants_hired_percent', '0'))

    # Доступ к категориям и просмотрам
    @property
    def category_id(self) -> str:
        """ID категории"""
        return self._data.get('category_id', '')

    @property
    def views(self) -> int:
        """Количество просмотров"""
        return int(self._data.get('views_dirty', '0'))

    # Доступ к доступным длительностям
    @property
    def available_durations(self) -> list[int]:
        """Список доступных длительностей выполнения"""
        return self._data.get('availableDurations', [])

    # Метод для проверки, есть ли портфолио
    @property
    def has_portfolio(self) -> bool:
        """Доступно ли портфолио"""
        return self._data.get('hasPortfolioAvailable', False)
    
    @property
    def url(self) -> str:
        """Ссылка на кворк."""
        return f'https://kwork.ru/projects/{self.id}'
    
    @property
    def dictify(self) -> dict:
        """Возвращаем словарь с кворком."""
        return self._data

class Resolution:
    def __init__(self, data: dict):
        self.data = data
    @property
    def height(self) -> int:
        """Возвращает высоту изображения."""
        return self.data.get('height')
    @property
    def width(self) -> int:
        """Возвращает ширину изображения."""
        return self.data.get('width')
    @property
    def orientation(self):
        """Возвращает ориентацию.\n0 - горизонтальная, 1 - вертикальная, 2 - квадратная."""
        if self.width > self.height:
            return 0
        elif self.width < self.height:
            return 1
        else:
            return 2

class YandexImage:
    def __init__(self, image: dict):
        self.image = image
    def get_image(self) -> bytes:
        """Изображение в байтах."""
        return self.image.get('data')
    def get_url(self) -> str:
        """Ссылка на изображение."""
        return self.image.get('url')
    def get_resolution(self) -> Resolution:
        """Возвращает высоту, ширину и ориентацию изображения."""
        image = Image.open(io.BytesIO(self.get_image()))
        resolution = image.size
        return Resolution({"width":resolution[0], 'height':resolution[1]})
    def get_size_mb(self):
        """Возвращает размер картинки в MB."""
        bytes_size = len(self.get_image()) 
        mbs = bytes_size / (1024 * 1024)
        return mbs
    def get_format(self):
        """Возвращает формат изображения."""
        image = Image.open(io.BytesIO(self.get_image()))
        return image.format.lower()
    def download(self, dir: str, name: str = None):
        """Просто скачаем локально.\ndir: директория. Если она не существует, мы создадим ее.\nname: имя изображения. Оно будет сгенерировано автоматически, если не указано."""
        if not os.path.exists(dir):
            os.mkdir(dir)
        if name:
            file = open(os.path.join(dir, f'{name}.jpg'), 'wb')
            file.write(self.get_image())
            file.close()
        else:
            r = random.random()
            file = open(os.path.join(dir, f'{r}.jpg'), 'wb')
            file.write(self.get_image())
            file.close()

class Cripto():
    """Класс со списком криптовалют, которые доступны для функции `crypto_price`.\nBITKOIN, USDT, DOGECOIN, HAMSTERCOIN"""
    BITKOIN = 'bitcoin'
    USDT = 'tether'
    DOGE = 'dogecoin'
    HMSTR = 'hamster'

class WBProduct:
    def __init__(self, data: dict):
        self.data = data
        self._raw_price = data.get('sizes', [{}])[0].get('price', {})

    @property
    def id(self) -> int:
        """ID товара"""
        return self.data.get('id', 0)

    @property
    def name(self) -> str:
        """Название товара"""
        return self.data.get('name', 'Без названия')

    @property
    def brand(self) -> str:
        """Бренд товара"""
        return self.data.get('brand', 'Без бренда')

    @property
    def price(self) -> float:
        """Финальная цена в рублях"""
        return self._raw_price.get('product', 0) / 100

    @property
    def basic_price(self) -> float:
        """Цена без скидок в рублях"""
        return self._raw_price.get('basic', 0) / 100

    @property
    def rating(self) -> float:
        """Рейтинг товара"""
        return float(self.data.get('reviewRating', 0))

    @property
    def feedbacks(self) -> int:
        """Количество отзывов"""
        return self.data.get('feedbacks', 0)

    @property
    def url(self) -> str:
        """Ссылка на товар"""
        return f"https://www.wildberries.ru/catalog/{self.id}/detail.aspx"

    @property
    def discount_percent(self) -> int:
        """Процент скидки"""
        if self.basic_price > 0:
            return int(100 - (self.price / self.basic_price * 100))
        return 0

    def __repr__(self):
        return f"<WBProduct: {self.name[:20]}... - {self.price}₽>"

class GeoFeature:
    """Класс для хранения информации о месте"""
    def __init__(self, name: str, lat: float, lon: float, address: str, distance: float, category: str):
        self.name = name
        self.lat = lat
        self.lon = lon
        self.address = address
        self.distance = distance
        self.category = category
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'name': self.name,
            'lat': self.lat,
            'lon': self.lon,
            'address': self.address,
            'distance': round(self.distance, 2),
            'category': self.category,
            'maps_url': f"https://www.google.com/maps/?q={self.lat},{self.lon}"
        }