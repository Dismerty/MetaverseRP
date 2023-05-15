"""
*  Команда для регистрации аккаунта
"""
from dispatcher import dp, bot
from libs.ConsoleLib import msg
from libs.ConnectID import Database

from aiogram import types

from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext

import hashlib

class RegisterForm(StatesGroup):
    login = State()
    password = State()

@dp.message_handler(AccountCreated = True, commands = ['reg', 'register', 'куп', 'купшыеук'], commands_prefix = ['/', '.'])
async def register(message: types.Message):
    await message.answer(msg.set('Вы не можете повторно создать аккаунт!'))

@dp.message_handler(AccountCreated = False, commands = ['reg', 'register', 'куп', 'купшыеук'], commands_prefix = ['/', '.'])
async def register(message: types.Message):
    await message.answer(msg.set('Придумайте любой свободный логин.', 'Создание нового аккаунта'))
    await RegisterForm.login.set()

@dp.message_handler(lambda message: message.text in str(Database.search('Login', message.text)), state = RegisterForm.login)
async def login_error(message: types.Message):
    await message.answer(msg.set('Такой логин уже существует, придумайте другой!', 'Создание нового аккаунта'))

@dp.message_handler(state = RegisterForm.login)
async def login(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['login'] = message.text
    
    await message.answer(msg.set('Придумайте надёжный пароль.', 'Создание нового аккаунта'))

    await RegisterForm.next()

@dp.message_handler(lambda message: len(message.text) < 8, state = RegisterForm.password)
async def password_error_8(message: types.Message, state: FSMContext):
    await message.answer(msg.set('Пароль не может быть меньше 8 символов!', 'Создание нового аккаунта'))

@dp.message_handler(lambda message: len(message.text) > 32, state = RegisterForm.password)
async def password_error_32(message: types.Message, state: FSMContext):
    await message.answer(msg.set('Пароль не может быть больше 32 символов!', 'Создание нового аккаунта'))

@dp.message_handler(state = RegisterForm.password)
async def password(message: types.Message, state: FSMContext):

    # Создание объекта хеша SHA-256
    sha256 = hashlib.sha256()
    # Обновление хеша с данными
    sha256.update(message.text.encode('utf-8'))
    # Получаем результат в виде шестнадцатеричной строки
    result = sha256.hexdigest()

    async with state.proxy() as data:
        Database.addAccount(message, data['login'], result, True)

    await message.answer(msg.set('Аккаунт успешно создан!', 'Создание нового аккаунта'))

    await state.finish()
