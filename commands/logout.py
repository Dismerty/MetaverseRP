"""
*  Команда для выхода из аккаунта
"""
from dispatcher import dp, bot
from libs.ConsoleLib import Console, msg
from libs.ConnectID import Database

from aiogram import types
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext

class UnregForm(StatesGroup): Confirmation = State()

@dp.message_handler(AccountCreated = False, commands = ['logout', 'дщпщге'], commands_prefix = ['/', '.'])
async def logout(message: types.Message, state: FSMContext):
    await message.answer(msg.add('Вы не можете выйти из аккаунта, так как не авторизованы!'))

@dp.message_handler(AccountCreated = True, commands = ['logout', 'дщпщге'], commands_prefix = ['/', '.'])
async def logout(message: types.Message, state: FSMContext):

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard = True, selective = True)
    keyboard.add('Подтвердить', 'Отклонить')

    async with state.proxy() as data:
        data['bot'] = await message.answer(msg.add('Подтвердите выход из аккаунта аккаунт.'), reply_markup = keyboard)
    
    await UnregForm.Confirmation.set()

@dp.message_handler(lambda message: message.text not in ["Подтвердить", "Отклонить"], state = UnregForm.Confirmation)
async def confirmation_logout(message: types.Message, state: FSMContext):

    async with state.proxy() as data:
        await bot.delete_message(data['bot'].chat.id, data['bot'].message_id)
        await bot.delete_message(message.chat.id, message.message_id)

        keyboard = types.ReplyKeyboardMarkup(resize_keyboard = True, selective = True)
        keyboard.add('Подтвердить', 'Отклонить')

        data['bot'] = await message.answer(msg.add('Подтвердите выход из аккаунта аккаунт.'), reply_markup = keyboard)

@dp.message_handler(state = UnregForm.Confirmation)
async def logout_done(message: types.Message, state: FSMContext):

    async with state.proxy() as data:
        await bot.delete_message(data['bot'].chat.id, data['bot'].message_id)
        await bot.delete_message(message.chat.id, message.message_id)

    if message.text == 'Подтвердить':
        Console.log(f'Успешный выход из аккаунта.', 'ConnectID')
        Console.log(f'Username: @{message.from_user.username}, TelegramID: {message.from_user.id}.', 'ConnectID')
        Database.logoutAccount(message)
        await message.answer(msg.add('Вы вышли из аккаунта.'))

    await state.finish()
