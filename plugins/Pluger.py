from libs.PluginLoader import Logger, RegisterCommand
from aiogram import types

Console = Logger('Pluger')

class Plugin:
    def OnLoad():
        Console.log('Плагин загружен!')

@RegisterCommand(commands = 'pluger')
async def pluger(message: types.Message):
    Console.log('Введена команда /pluger!')
    await message.answer('Pluger - Тестовый плагин v1')
