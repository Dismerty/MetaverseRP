"""
*  Команда для входа в аккаунт
"""
from dispatcher import dp
from libs.ConsoleLib import Console, msg
from libs.ConnectID import Database

import hashlib

from aiogram import types
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext

class LoginForm(StatesGroup):
    login = State()
    password = State()

@dp.message_handler(commands = ['log', 'login', 'дщп', 'дщпшт'], commands_prefix = ['/', '.'])
async def register(message: types.Message):

    if Database.check(message) == True:
        await message.answer(msg.add('Вы не можете повторно войти в аккаунт!'))
        return

    await message.answer(msg.set('Введите логин.', 'Авторизация в аккаунт'))
    await LoginForm.login.set()

@dp.message_handler(state = LoginForm.login)
async def login(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['login'] = message.text
    
    await message.answer(msg.set('Введите пароль.', 'Авторизация в аккаунт'))

    await LoginForm.next()

@dp.message_handler(lambda message: len(message.text) < 8, state = LoginForm.password)
async def password_error_8(message: types.Message, state: FSMContext):
    await message.answer(msg.set('Пароль не может быть меньше 8 символов!', 'Авторизация в аккаунт'))

@dp.message_handler(lambda message: len(message.text) > 32, state = LoginForm.password)
async def password_error_32(message: types.Message, state: FSMContext):
    await message.answer(msg.set('Пароль не может быть больше 32 символов!', 'Авторизация в аккаунт'))

@dp.message_handler(state = LoginForm.password)
async def password(message: types.Message, state: FSMContext):

    # Создание объекта хеша SHA-256
    sha256 = hashlib.sha256()
    # Обновление хеша с данными
    sha256.update(message.text.encode('utf-8'))
    # Получаем результат в виде шестнадцатеричной строки
    result = sha256.hexdigest()

    async with state.proxy() as data:

        if Database.checkLogin(message, data['login']) == False:
            await message.answer(msg.set('Неправильный логин или пароль.\nДля повторной попытки пропишите \"/login\"', 'Авторизация в аккаунт'))
            Console.log(f'Неудачная попытка входа в аккаунт. Логин: {data["login"]}', 'ConnectID')
            Console.log(f'Username: @{message.from_user.username}, TelegramID: {message.from_user.id}.', 'ConnectID')
            await state.finish()
            return
        
        if Database.login(message, data['login'], result):
            await message.answer(msg.set('Вы успешно вошли в аккаунт!', 'Авторизация в аккаунт'))
            Console.log(f'Успешный вход в аккаунт. Логин: {data["login"]}', 'ConnectID')
            Console.log(f'Username: @{message.from_user.username}, TelegramID: {message.from_user.id}.', 'ConnectID')
            await state.finish()
            return
        else:
            await message.answer(msg.set('Неправильный логин или пароль.\nДля повторной попытки пропишите \"/login\"', 'Авторизация в аккаунт'))
            Console.log(f'Неудачная попытка входа в аккаунт. Логин: {data["login"]}', 'ConnectID')
            Console.log(f'Username: @{message.from_user.username}, TelegramID: {message.from_user.id}.', 'ConnectID')
            await state.finish()
            return
