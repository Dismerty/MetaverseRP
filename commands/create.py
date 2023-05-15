"""
*  Команда для создания персонажа
"""
from dispatcher import dp
from libs.ConsoleLib import msg
from libs.ConnectID import Connect
import variables

import os, asyncio

from aiogram import types
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.types.reply_keyboard import ReplyKeyboardRemove

species = ['Люди', 'Гномы', 'Протарианцы', 'Лингвинги', 'Ноэрцы', 'Каджит', 'Берендей', 'Сильфы', 'Сильфы Света', 'Сильфы Тьмы', 'Драконо-Рождённые']

class Form(StatesGroup):
    gender = State() # Пол
    age = State() # Возраст
    species = State() # Раса
    appearance = State() # Внешность персонажа
    character = State() # Характер
    diet = State() # Рацион питания
    story = State() # Краткая история
    confirmation = State() # Подтверждение создания персонажа
    end = State() # Конец

@dp.message_handler(AccountCreated = False, commands = ['create', 'скуфеу'], commands_prefix = ['/', '.'])
async def create(message: types.Message):
    await message.answer(msg.set('''Для использования команды войдите или зарегестрируйте аккаунт.

<i>Для регистрации пропишите /register.
Для входа в аккаунт пропишите /login.</i>'''))

@dp.message_handler(CharacterCreated = True, commands = ['create', 'скуфеу'], commands_prefix = ['/', '.']) # Имя персонажа
async def create(message: types.Message):
    await message.answer(msg.set('''Вы не можете повторно создать персонажа.

<i>Пропишите команду /chat чтобы начать играть.</i>'''))

@dp.message_handler(CharacterCreated = False, commands = ['create', 'скуфеу'], commands_prefix = ['/', '.']) # Имя персонажа
async def create(message: types.Message, state: FSMContext):

    async with state.proxy() as data:
        data['bot'] = await message.answer(msg.set('Какое будут звать вашего персонажа?', 'Создание игрового персонажа'))

    await Form.next()

@dp.message_handler(state = Form.gender) # Выбор пола персонажа
async def player_gender(message: types.Message, state: FSMContext):
    async with state.proxy() as data:

        # Удаление сообщений и вписывание данных в переменную
        #await bot.delete_message(data['bot'].chat.id, data['bot'].message_id)
        #await bot.delete_message(message.chat.id, message.message_id)

        data['name'] = message.text

        keyboard = types.ReplyKeyboardMarkup(resize_keyboard = True, selective = True)
        keyboard.add('Мужской', 'Женский')

        data['bot'] = await message.answer(msg.set('Какой пол у персонажа?', 'Создание игрового персонажа'), reply_markup = keyboard)
    
    await Form.next()

@dp.message_handler(lambda message: message.text not in ['Мужской', 'Женский', 'Неизвестно'], state = Form.age) # Исключение, если игрок написал что-то другое
async def gender_error(message: types.Message, state: FSMContext):
    async with state.proxy() as data:

        # Удаление сообщений и вписывание данных в переменную
        #await bot.delete_message(data['bot'].chat.id, data['bot'].message_id)
        #await bot.delete_message(message.chat.id, message.message_id)

        keyboard = types.ReplyKeyboardMarkup(resize_keyboard = True, selective = True)
        keyboard.add('Мужской', 'Женский')

        data['bot'] = await message.answer(msg.set('Выбрать пол можно только на клавиатуре ниже!', 'Создание игрового персонажа'), reply_markup = keyboard)

@dp.message_handler(state = Form.age) # Какой возраст персонажа
async def player_age(message: types.Message, state: FSMContext):
    async with state.proxy() as data:

        # Удаление сообщений и вписывание данных в переменную
        #await bot.delete_message(message.chat.id, message.message_id)
        #await bot.delete_message(data['bot'].chat.id, data['bot'].message_id)

        data['gender'] = message.text

        await message.answer(msg.set('Сколько лет вашему персонажу?\n\n<i>Примечание: возраст можно вписать только цифрой, всё измеряется в годах.</i>', 'Создание игрового персонажа'), reply_markup = ReplyKeyboardRemove())

    await Form.next()

@dp.message_handler(lambda message: message.text in "Неизвестно" or not message.text.isdigit(), state=Form.species) # Исключение, если игрок не правильно вписал возраст персонажа
async def age_error(message: types.Message, state: FSMContext):
    async with state.proxy() as data:

        # Удаление сообщений и вписывание данных в переменную
        #await bot.delete_message(message.chat.id, message.message_id)
        #await bot.delete_message(bot_create_msg.chat.id, bot_create_msg.message_id)

        data['bot'] = await message.answer(msg.set('Введите число без дополнительных символов!', 'Создание игрового персонажа'))
        await Form.age.set()
    
    await Form.next()

@dp.message_handler(state = Form.species) # Выбор расы персонажа
async def player_species(message: types.Message, state: FSMContext):
    async with state.proxy() as data:

        # Удаление сообщений и вписывание данных в переменную
        #await bot.delete_message(data['bot'].chat.id, data['bot'].message_id)
        #await bot.delete_message(message.chat.id, message.message_id)

        data['age'] = int(message.text)

        keyboard = types.ReplyKeyboardMarkup(resize_keyboard = True, selective = True)
        for values in species: keyboard.add(values)

        data['bot'] = await message.answer(msg.set('К какой расе будет относиться ваш персонаж?', 'Создание игрового персонажа'), reply_markup = keyboard)
    
    await Form.next()

@dp.message_handler(lambda message: message.text not in species, state=Form.appearance)
async def species_error(message: types.Message, state: FSMContext):
    async with state.proxy() as data:

        # Удаление сообщений и вписывание данных в переменную
        #await bot.delete_message(data['bot'].chat.id, data['bot'].message_id)
        #await bot.delete_message(message.chat.id, message.message_id)

        keyboard = types.ReplyKeyboardMarkup(resize_keyboard = True, selective = True)
        for values in species: keyboard.add(values)

        data['bot'] = await message.answer(msg.set('Выбрать расу можно только на клавиатуре ниже!', 'Создание игрового персонажа'), reply_markup = keyboard)

@dp.message_handler(state=Form.appearance)
async def player_appearance(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        
        data['species'] = message.text

        # Удаление сообщений и вписывание данных в переменную
        #await bot.delete_message(data['bot'].chat.id, data['bot'].message_id)
        #await bot.delete_message(message.chat.id, message.message_id)

        data['bot'] = await message.answer(msg.set('Опишите внешний вид вашего персонажа.\n\n<i>Примечание: старайтесь написать подробное описание внешности вашего персонажа.</i>', 'Создание игрового персонажа'), reply_markup = ReplyKeyboardRemove())
    
    await Form.next()

@dp.message_handler(state=Form.character)
async def player_character(message: types.Message, state: FSMContext):
    async with state.proxy() as data:

        # Удаление сообщений и вписывание данных в переменную
        #await bot.delete_message(data['bot'].chat.id, data['bot'].message_id)
        #await bot.delete_message(message.chat.id, message.message_id)

        data['appearance'] = message.text

        data['bot'] = await message.answer(msg.set('Опишите характер вашего персонажа.\n\n<i>Примечание: старайтесь написать подробное описание характера вашего персонажа.</i>', 'Создание игрового персонажа'))
    
    await Form.next()

@dp.message_handler(state=Form.diet)
async def player_diet(message: types.Message, state: FSMContext):
    async with state.proxy() as data:

        # Удаление сообщений и вписывание данных в переменную
        #await bot.delete_message(data['bot'].chat.id, data['bot'].message_id)
        #await bot.delete_message(message.chat.id, message.message_id)

        data['character'] = message.text

        data['bot'] = await message.answer(msg.set('Опишите рацион питания вашего персонажа.\n\n<i>Примечание: старайтесь написать подробное описание рациона питания вашего персонажа.</i>', 'Создание игрового персонажа'))

    await Form.next()

@dp.message_handler(state=Form.story)
async def player_story(message: types.Message, state: FSMContext):
    async with state.proxy() as data:

        # Удаление сообщений и вписывание данных в переменную
        #await bot.delete_message(data['bot'].chat.id, data['bot'].message_id)
        #await bot.delete_message(message.chat.id, message.message_id)

        data['diet'] = message.text

        data['bot'] = await message.answer(msg.set('Опишите историю вашего персонажа.\n\n<i>Примечание: Вы можете кратко описать историю появления персонажа, или же как проходило его детство, всё зависит от вашей фантазии.</i>', 'Создание игрового персонажа'))

    await Form.next()

@dp.message_handler(state=Form.confirmation)
async def player_capabilities(message: types.Message, state: FSMContext):
    async with state.proxy() as data:

        # Удаление сообщений и вписывание данных в переменную
        #await bot.delete_message(data['bot'].chat.id, data['bot'].message_id)
        #await bot.delete_message(message.chat.id, message.message_id)

        data['story'] = message.text

        data['create'] = await message.answer(msg.set('Обработка анкеты...', 'Создание игрового персонажа'))

        keyboard = types.ReplyKeyboardMarkup(resize_keyboard = True, selective = True)
        keyboard.add('Подтвердить', 'Отмена')

        await asyncio.sleep(2)

        await message.answer(msg.set(f"Вот как выглядит ваша анкета персонажа:\nИмя: <i>{data['name']}</i>\nПол: <i>{data['gender']}</i>\nВозраст: <i>{data['age']}</i>\nРаса: <i>{data['species']}</i>\nВнешность: <i>{data['appearance']}</i>\nХарактер: <i>{data['character']}</i>\nРацион питания: <i>{data['diet']}</i>\nИстория: <i>{data['story']}</i>\n\n<i>Примечание: способности для персонажа выбирают администраторы</i>", 'Создание игрового персонажа'), reply_markup = keyboard)

    await Form.next()

@dp.message_handler(state=Form.end)
async def end(message: types.Message, state: FSMContext):
    async with state.proxy() as data:

        if 'Подтвердить' in message.text:
            if os.path.exists('data/profiles/') == False:
                os.mkdir('data/profiles/')

            player = variables.get("player")
            player['name'] = data['name']
            player['real_name'] = data['name']
            player['gender'] = data['gender']
            player['age'] = data['age']
            player['species'] = data['species']
            player['appearance'] = data['appearance']
            player['character'] = data['character']
            player['diet'] = data['diet']
            player['story'] = data['story']
            Connect.addPlayer(message, Data = player, Table = 'CreatedPlayers')

            await message.answer(msg.set('Персонаж успешно создан, ожидает проверки администрации.', 'Создание игрового персонажа'), reply_markup = ReplyKeyboardRemove())
            await state.finish(); return

        else:
            await message.answer(msg.set('Вы отменили подачу анкеты.\nДля повторного создания персонажа пропишите \"/create\"', 'Создание игрового персонажа'), reply_markup = ReplyKeyboardRemove())
            await state.finish(); return
