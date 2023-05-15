from dispatcher import dp

from libs.ChatLogger import ChatLogger
from commands import info
from aiogram import types

@dp.message_handler(commands = ['info', 'штащ'], commands_prefix = ['/', '.'], state = ChatLogger.GameChatState)
async def ChatCommandInfo(message: types.Message):
    await info.info(message)