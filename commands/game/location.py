from dispatcher import dp

from libs.ChatLogger import ChatLogger
from libs.GameAssets import Player, Location
from libs import msg
from aiogram import types

@dp.message_handler(commands = ['location', 'дщсфешщт'], commands_prefix = ['/', '.'], state = ChatLogger.GameChatState)
async def ChatCommandLocation(message: types.Message):
    player = Player.TelegramID(message)

    location = Location(player.location())
    await message.answer(msg.set(f'''Здесь находится вся информация локации на которой находитесь.

<b>Основная информация</b>
Название: <i>{location.name}</i>
Описание: <i>{location.description}</i>
Возможности: <i>{location.capabilities}</i>

<b>Внеигровая информация</b>
ID локации: <i>{location.id}</i>
''', 'Информация о локации'))