from dispatcher import dp
from configuration import config

from libs.ChatLogger import ChatLogger, ChatScanner
from libs.GameAssets import GameAssets, Player, Location
from libs import Console, msg
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

    if message.text.startswith('/'):
        await message.answer(msg.set("Неизвестная команда!"))
        return

    actions = await ChatLogger.sendMessageRP(message, Player.TelegramID(message).data)

    for action in actions:

        if not isinstance(action, dict):
            args = action.split(' ')

            if action.startswith('move') and len(args) == 2:

                if Player.TelegramID(message).move(args[1]):
                    player = Player.TelegramID(message)
                    location = Location(player.location())
                    await message.answer(msg.set(f"Вы переместились на локацию “{location.name}”."))


