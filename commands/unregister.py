"""
*  Команда для удаления аккаунта
"""
from dispatcher import dp, bot
from libs.ConsoleLib import msg
from libs.ConnectID import Database, Account

from aiogram import types
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext

# Состояния удаления аккаунта
class State_unreg(StatesGroup): Confirmation = State()

# Команда для удаления аккаунта
@dp.message_handler(AccountCreated = False, perms = 'bot.command.unreg', commands = ['unreg', 'unregister'], commands_prefix = ['/', '.'])
async def unreg(message: types.Message):
    await message.answer(msg.set('Вы не можете удалить аккаунт, так как не авторизованы!'))

@dp.message_handler(AccountCreated = True, perms = 'bot.command.unreg', commands = ['unreg', 'unregister'], commands_prefix = ['/', '.'])
async def unreg(message: types.Message, state: FSMContext):

    if Account(message).UserID == 0:
        await message.answer(msg.add('Невозможно удалить аккаунт мироздания, он является частью системы!'))
        await state.finish()
        return

    if not Account(message).created:
        await message.answer(msg.add('Вы не можете удалить аккаунт, так как вы не находитесь в нём.', 'Удаление аккаунта'))

    if Account(message).created:
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard = True, selective = True)
        keyboard.add('Подтвердить', 'Отклонить')

        async with state.proxy() as data:
            data['bot'] = await message.answer(msg.add('Вы уверены что хотите удалить аккаунт?', 'Удаление аккаунта'), reply_markup = keyboard)
        
        await State_unreg.Confirmation.set()

# Если при удалении аккаунта выбор был сделан не правильно
@dp.message_handler(lambda message: message.text not in ["Подтвердить", "Отклонить"], state = State_unreg.Confirmation)
async def confirmation_unreg_invalid(message: types.Message, state: FSMContext):

    async with state.proxy() as data:
        await bot.delete_message(data['bot'].chat.id, data['bot'].message_id)
        await bot.delete_message(message.chat.id, message.message_id)

        keyboard = types.ReplyKeyboardMarkup(resize_keyboard = True, selective = True)
        keyboard.add('Подтвердить', 'Отклонить')

        data['bot'] = await message.answer(msg.add('Вы уверены что хотите удалить аккаунт?', 'Удаление аккаунта'), reply_markup = keyboard)

# Отмена или удаление аккаунта
@dp.message_handler(state = State_unreg.Confirmation)
async def confirmation_unreg(message: types.Message, state: FSMContext):

    async with state.proxy() as data:
        await bot.delete_message(data['bot'].chat.id, data['bot'].message_id)
        await bot.delete_message(message.chat.id, message.message_id)

    if message.text == 'Подтвердить':
        Database.deleteAccount(message)
        await message.answer(msg.add('Ваш аккаунт успешно удалён.', 'Удаление аккаунта'))

    await state.finish()
