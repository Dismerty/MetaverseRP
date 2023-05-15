from dispatcher import dp

from libs.ChatLogger import ChatLogger
from libs import Connect
from aiogram import types

@dp.message_handler(commands = ['b', 'и'], commands_prefix = ['/', '.'], state = ChatLogger.GameChatState)
async def ChatNonRP(message: types.Message):

    data = Connect.readPlayer(message)
    await ChatLogger.sendMessageNonRP(message, data, message.text[3:])