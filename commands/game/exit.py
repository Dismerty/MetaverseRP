from dispatcher import dp, bot

from aiogram import types
from aiogram.dispatcher.storage import FSMContext

from libs.GameAssets import Player, Location
from libs.ChatLogger import ChatLogger
from libs import msg

@dp.message_handler(commands = ['exit', 'учше'], commands_prefix = ['/', '.'], state = ChatLogger.GameChatState)
async def ChatNonRP(message: types.Message, state: FSMContext):
    player = Player.TelegramID(message)
    location = Location(player.location())
    await message.answer(msg.set(f'Вы вышли из игрового чата MetaversRP!\nВаше последнее местоположение: {location.name}\n\n<i>Введите /chat для возращения в игровой чат</i>'), parse_mode = types.ParseMode.HTML)
    player.kick()
    await state.finish()