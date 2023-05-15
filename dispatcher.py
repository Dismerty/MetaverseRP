# Системные библиотеки Python
import logging

# Библиотека AIOGram
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.bot.api import TelegramAPIServer

# Библиотеки бота
from libs.ConnectID import CharacterCreated, AccountCreated
from libs.FilterManager import Perms

# Родные библиотеки
from configuration import config

# Конфигурация логирования
if config['Settings']['Logging']: logging.basicConfig(level=logging.INFO)
else: logging.basicConfig(level=logging.ERROR)

if config['Settings']['LocalServer'] != None:
    # Подключение бота к локальному серверу
    localServer = TelegramAPIServer.from_base(config['Settings']['LocalServer'])
    bot = Bot(token = config['Settings']['Token'], server = localServer, parse_mode = "HTML")

else:
    # Подключение бота к серверам телеграма
    bot = Bot(token = config['Settings']['Token'], parse_mode = "HTML")

# Инициализация диспачера
dp = Dispatcher(bot, storage = MemoryStorage())

# Тут будет система привязки кастомных фильтров
dp.filters_factory.bind(Perms)
dp.filters_factory.bind(CharacterCreated)
dp.filters_factory.bind(AccountCreated)