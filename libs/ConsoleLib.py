"""
* ConsoleLib - библиотека для работы с консолью и оформлением
"""

# Импорт библиотек
import os, datetime, yaml

# Чтение конфигурации
if os.path.exists('config.yml') == False:
    print('[ERROR/ConsoleLib] Не удалось загрузить конфигурацию!')
    exit()
with open('config.yml', 'r') as file:
    config = yaml.safe_load(file)

# Работа консоли и оформление
backlight = config['Console']['Backlight']
company = config['Settings']['Game']

class PluginDebug:

    def __init__(self, plugin) -> None:
        self.plugin = plugin
    
    def log(self, message, on = True):

        now = datetime.datetime.now().strftime('%H:%M:%S')

        if backlight and on:
            return print(f'{colors.gray}{now} {colors.gray}[{colors.blue}Info/Plugins{colors.gray}] [{colors.blue}{self.plugin}{colors.gray}] {colors.white_blue}{message}{colors.reset}')
        elif on: 
            return print(f'{now} [Info/Plugins] [{colors.blue}{self.plugin}{colors.gray}] {message}')


class Console:
    """Данный класс имеет такие функции как `log()`, `worn()` и `error()`"""

    def __init__(self):
        pass

    def debug(message, tag = company):
        now = datetime.datetime.now().strftime('%H:%M:%S')

        if backlight: return print(f'{colors.gray}{now} {colors.yellow}[Debug/{tag}] {message}{colors.reset}')
        else: return print(f'{now} [Debug/{tag}] {message}')

    def log(message, tag = company, on = True, custom = False):
        """Функция `log()` принимает аргументы `message`, `tag` и выводят в консоль информационное оформленное сообщение"""

        now = datetime.datetime.now().strftime('%H:%M:%S')

        if backlight and on:
            if custom: return print(f'{colors.gray}{now} {colors.gray}[{colors.blue}{tag}{colors.gray}] {colors.white_blue}{message}{colors.reset}')
            else: return print(f'{colors.gray}{now} {colors.gray}[{colors.blue}Info/{tag}{colors.gray}] {colors.white_blue}{message}{colors.reset}')
        elif on: 
            if custom: return print(f'{now} [{tag}] {message}')
            else: return print(f'{now} [Info/{tag}] {message}')
    
    def worn(message, tag = company):
        """Функция `worn()` принимает аргументы `message`, `tag` и выводят в консоль предупреждение, оформленное сообщение"""

        now = datetime.datetime.now().strftime('%H:%M:%S')

        if backlight: return print(f'{colors.gray}{now} {colors.yellow}[WORNING/{tag}] {message}{colors.reset}')
        else: return print(f'{now} [WORNING/{tag}] {message}')

    def error(message, tag = company):
        """Функция `error()` принимает аргументы `message`, `tag` и выводят в консоль ошибку, оформленное сообщение"""

        now = datetime.datetime.now().strftime('%H:%M:%S')

        if backlight: return print(f'{colors.gray}{now} {colors.red}[ERROR/{tag}] {message}{colors.reset}')
        else: return print(f'{now} [ERROR/{tag}] {message}')

class msg:
    """Данный класс отвечает за форматирование текста в сообщениях бота"""

    def add(text, tag = company): return f'<b>* Система {tag}</b>\n{text}'
    def set(text, tag = f'Система {company}'): return f'<b>* {tag}</b>\n{text}'

# Цвета для вывода в консоль (Если терминал поддерживает, иначе нужно выключать через конфиги)
class colors:
    black = '\033[30m'; red = '\033[31m'; green = '\033[32m'
    yellow = '\033[33m'; blue = '\033[34m'; violet = '\033[35m'
    white_blue = '\033[36m'; gray = '\033[37m'

    dark = '\033[2m'; reset = '\033[0m'