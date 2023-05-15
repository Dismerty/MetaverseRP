import sys, os, zipfile
os.system('cls||clear'); print("MetaverseRP - MetaverseMMORPG Project 2021 (C)")

# Создание папок и распаковка файлов
if not os.path.isfile('config.yml'):
    print('[INFO] Создание файла config.yml.')
    zip = zipfile.PyZipFile(sys.argv[0])
    zip.extract('config.yml')

if not os.path.exists('plugins'):
    print('[INFO] Создание папки plugins.')
    os.mkdir('plugins')

if not os.path.exists('assets'):
    print('[INFO] Создание папки assets.')
    os.mkdir('assets')

if not os.path.exists('assets/locations'):
    print('[INFO] Создание папки locations в assets.')
    os.mkdir('assets/locations')

from libs import Console, msg

try:
    from aiogram.utils import executor
    from aiogram import types
    Console.log('Библиотека AIOGram успешно импортирована!')
except Exception as e:
    Console.error('Отсутствует библиотека AIOGram. Установить библиотеку можно командой \'pip install aiogram\'')
    Console.error(f'Ошибка: {e}'); exit()

# Импорт родных библиотек
import libs.ChatLogger
from libs.GameAssets import Location
from libs import Database
from configuration import config
from dispatcher import dp, bot

# Импортирование PluginLoader. Загрузка плагинов осуществляется раньше команд.
# Чтобы можно было добавить свой функционал командам регестрируя их раньше.
import libs.PluginLoader.PluginProcess

# Импортирование всех созданых команд в папке commands.
import commands, commands.admin, commands.game

# Загрузка всех локаций
Console.log('Загрузка локаций...')
Location.load()
Console.log('Локации успешно загружены!')

from libs.ChatLogger import ChatLogger
dp.register_message_handler(ChatLogger.GameChat, state = ChatLogger.GameChatState)
Console.log('Игровой чат загружен!')

async def Startup(dp):
    TelegramID = Database.TelegramID(0)
    await commands.CommandInfo.setDescriptionCommands(bot)

    Console.log('Бот успешно запущен!')
    if TelegramID != None:
        await bot.send_message(TelegramID, msg.set(f'''Бот успешно запущен!

<b>Техническая информация</b>
Версия Python: <i>{sys.version}</i>
Платформа: <i>{sys.platform}</i>''', f"Статус {config['Settings']['Game']}"), parse_mode = types.ParseMode.HTML)
    Console.log('Введите команду \"/start\" для начала работы с ботом!')

async def Shutdown(dp):
    Console.log('Завершение работы.')

def main():
    try:
        if config['Settings']['Internet'] == True:
            executor.start_polling(dp, skip_updates = True, on_startup = Startup, on_shutdown = Shutdown)

        else:
            Console.worn('Бот работает в автономном режиме.')
            Console.worn('Игнорирование подключения к серверам Telegram.')
            Console.log('Пропишите help для подробной информации.')

            while True:
                enter = input(' > ')

                if enter in ['stop', 'end', 'exit']:
                    Console.log('Завершение работы.')
                    exit()

                elif enter == 'help':
                    Console.log('''/stop - Остановка бота
                    /help - Информация о командах''')
                    
    except Exception as e:
        Console.error(f'Завершение работы.\nОшибка: {e}')

if __name__ == '__main__':
    main()
