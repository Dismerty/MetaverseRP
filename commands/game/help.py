from dispatcher import dp

from libs.ChatLogger import ChatLogger
from libs import msg
from aiogram import types

@dp.message_handler(commands = ['help', 'рудз'], commands_prefix = ['/', '.'], state = ChatLogger.GameChatState)
async def ChatCommandInfo(message: types.Message):
    
    help = """Здесь вы сможете узнать полную информацию по командам.

<b>RolePlay команды</b>
/b (сообщение) - Отправляет сообщение в NonRP чат локации.
/exit - Выход из игрового чата.

<b>Игровые команды</b>
/info - Просмотреть статистику персонажа.

<b>Обратная связь и чаты</b>
@MetaverseRP - Беседа проекта
@MetaverseRPAdmin - Администратор проекта
@GamePythonDev - Второй администратор"""

    await message.answer(msg.set(help, 'Помощь и информация по командам'))