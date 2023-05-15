"""
*  Команда для просмотра информации
"""
from dispatcher import dp
from libs.ConsoleLib import msg

from aiogram import types

@dp.message_handler(commands = ['help', 'рудз'], commands_prefix = ['/', '.'])
async def help(message: types.Message):

    help = """Здесь вы сможете узнать полную информацию по командам.

<b>Действия с аккаунтом</b>
/register - Зарегестрировать аккаунт.
/login - Войти в аккаунт.
/logout - Выйти из аккаунта.
/unregister - Удалить аккаунт.
<i>(Данные будут полностью удалены и не подлежат восстановлению)</i>

<b>Игровые команды</b>
/create - Создать нового персонажа.
/info - Просмотреть статистику персонажа.

<b>Обратная связь и чаты</b>
@MetaverseRP - Беседа проекта
@MetaverseRPAdmin - Администратор проекта
@GamePythonDev - Второй администратор"""

    await message.answer(msg.set(help, 'Помощь и информация по командам'))
