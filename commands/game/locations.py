from dispatcher import dp

from libs.ChatLogger import ChatLogger
from libs.GameAssets import Player, Location
from libs import msg
from aiogram import types

@dp.message_handler(commands = ['locations', 'дщсфешщты'], commands_prefix = ['/', '.'], state = ChatLogger.GameChatState)
async def ChatCommandLocation(message: types.Message):

    MessageModifier = 'Полный список локаций.\n'

    for location in Location.list():
        l = Location(location)
        MessageModifier += f"\n<b>Локация “{l.name}”</b>\nID: <i>{location}</i>\n"

    await message.answer(msg.set(MessageModifier, 'Список локаций (Beta функции)'))