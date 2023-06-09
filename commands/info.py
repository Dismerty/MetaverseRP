from dispatcher import dp

from libs.ConnectID import Database
from libs.ConsoleLib import msg
from libs.GameAssets import Player
from aiogram import types

@dp.message_handler(AccountCreated = False, commands = ['info', 'штащ'], commands_prefix = ['/', '.'])
async def info(message: types.Message):
    await message.answer(msg.add('''Для использования команды войдите или зарегестрируйте аккаунт.

<i>Для регистрации пропишите /register.
Для входа в аккаунт пропишите /login.</i>'''))

@dp.message_handler(CharacterCreated = False, commands = ['info', 'штащ'], commands_prefix = ['/', '.'])
async def info(message: types.Message):
    await message.answer(msg.add('''Для использования команды создайте персонажа.
    
<i>Для создания персонажа пропишите /create.</i>'''))

@dp.message_handler(commands = ['info', 'штащ'], commands_prefix = ['/', '.'])
async def info(message: types.Message):

    args = message.text.split(' ')

    if len(args) == 1:
        player = Player.TelegramID(message)
        text = f"""Статистика вашего персонажа.

<b>Основная информация</b>
Имя: <i>{player.name}</i>
Пол: <i>{player.gender}</i>
Возраст: <i>{player.age}</i>
Раса: <i>{player.species}</i>
Внешность: <i>{player.appearance}</i>
Характер: <i>{player.character}</i>
Рацион питания: <i>{player.diet}</i>
Краткая история: <i>{player.story}</i>

<b>Дополнительная информация</b>
Уровень/Опыт: {'∞' if player.level >= 1000000 else player.level}/{'∞' if player.experience >= 1000000000 else player.experience}
Здоровье: {player.health.value}/{player.health.max} единиц.

<b>Техническая информация</b>
Логин: {Database.search('TelegramID', message.from_user.id, 'Login')}
UserID: {player.UserID}
"""
    
    elif len(args) == 2 and args[1].isdigit() and Player.check(args[1]):
        player = Player.UserID(args[1])
        text = f"""Статистика персонажа (UserID: {args[1]}).

<b>Основная информация</b>
Имя: <i>{player.name}</i>
Пол: <i>{player.gender}</i>
Возраст: <i>{player.age}</i>
Раса: <i>{player.species}</i>
Внешность: <i>{player.appearance}</i>
Характер: <i>{player.character}</i>
Рацион питания: <i>{player.diet}</i>
Краткая история: <i>{player.story}</i>

<b>Дополнительная информация</b>
Уровень/Опыт: {'∞' if player.level >= 1000000 else player.level}/{'∞' if player.experience >= 1000000000 else player.experience}
Здоровье: {player.health.value}/{player.health.max} единиц.
"""
    
    elif len(args) >= 3:
        await message.answer(msg.set('Команда /info (ID)\n\n<i>Используйте, чтобы посмотреть статистику другого игрока.</i>'))
        return

    elif not args[1].isdigit():
        await message.answer(msg.set('Аргумент ID может принимать только число!', 'Информация о персонаже'))
        return

    else:
        await message.answer(msg.set('Такого аккаунта не существует!', 'Информация о персонаже'))
        return

    await message.answer(msg.set(text, 'Информация о персонаже'))