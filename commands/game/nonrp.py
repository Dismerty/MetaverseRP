from dispatcher import dp

from libs.ChatLogger import ChatLogger
from libs import Connect, msg
from aiogram import types

@dp.message_handler(commands = ['b', 'и'], commands_prefix = ['/', '.'], state = ChatLogger.GameChatState)
async def ChatNonRP(message: types.Message):

    if len(message.text.split(' ')) == 1:
        await message.answer(msg.set('Команда /b (message)\n\n<b>Аргументы</b>\nmessage - Текст сообщение, которое должно отправится в NonRP чат.\n\n<i>Используйте, чтобы написать в NonRP чат.</i>'))
        return

    data = Connect.readPlayer(message)
    await ChatLogger.sendMessageNonRP(message, data, message.text[3:])