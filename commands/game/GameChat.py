from dispatcher import dp
from configuration import config

from libs.ChatLogger import ChatLogger
from libs.GameAssets import GameAssets, Player, Location
from libs import msg
from aiogram import types

# Обработкичик на проверку создание аккаунтов и игрового персонажа
@dp.message_handler(AccountCreated = False, commands = ['chat', 'срфе'], commands_prefix = ['/', '.'])
async def chat(message: types.Message):
    await message.answer(msg.set('Вы не можете сейчас зайти в чат, для начала создайте или войдите в аккаунт... \n\n<i>Используйте команду /login или /register</i>'), parse_mode = types.ParseMode.HTML)

@dp.message_handler(CharacterCreated = False, commands = ['chat', 'срфе'], commands_prefix = ['/', '.'])
async def chat(message: types.Message):
    await message.answer(msg.set('Вы не можете сейчас зайти в чат, для начала создайте персонажа...\n\n<i>Используйте команду /create</i>'), parse_mode = types.ParseMode.HTML)

@dp.message_handler(AccountCreated = True, commands = ['chat', 'срфе'], commands_prefix = ['/', '.'])
async def chat(message: types.Message):
    Player.TelegramID(message).move(Location.spawn())

    await message.answer(msg.set(f"Добро пожаловать в игровой чат {config['Settings']['Company']}!\nТекущая локация: {GameAssets.readLocation(message)['Name']}\n\n<i>Введите /help для открытия меню помощи</i>"), parse_mode = types.ParseMode.HTML)
    await ChatLogger.GameChatState.set()

# Обработчик игрового чата
@dp.message_handler(state = ChatLogger.GameChatState)
async def GameChat(message: types.Message):
    await ChatLogger.sendMessageRP(message, Player.TelegramID(message).data)