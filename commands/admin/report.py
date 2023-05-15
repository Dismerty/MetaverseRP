"""
*  Команда для проверки запросов на создания персонажа и проверки жалоб
"""
from dispatcher import dp, bot
from libs.ConsoleLib import Console, msg
from libs.ConnectID import Connect, Database

from aiogram import types
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.types.reply_keyboard import ReplyKeyboardRemove

class ReportForm(StatesGroup):
    Select = State()
    PlayerCreate = State()
    PlayerCreateDeny = State()
    Done = State()

powers = ['Пусто']

@dp.message_handler(perms = 'bot.command.report', commands = 'report') # Имя персонажа
async def report(message: types.Message):

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard = True, selective = True)
    keyboard.add('Создание персонажей')
    keyboard.add('Отмена')

    await message.answer(msg.set('Что вы хотите проверить?', 'Система репортов'), reply_markup = keyboard)

    await ReportForm.next()

@dp.message_handler(state=ReportForm.Select)
async def reportSelect(message: types.Message, state: FSMContext):
    
    if message.text in 'Отмена':
        await message.answer(msg.set('Действие отменено', 'Система репортов'), reply_markup = ReplyKeyboardRemove())
        await state.finish(); return
    
    elif message.text in 'Создание персонажей':
        reports = Connect.listPlayers('CreatedPlayers')

        if reports == False:
            await message.answer(msg.set('Заявки на создание персонажей в данный момент отсутствуют.', 'Система репортов'),  reply_markup = ReplyKeyboardRemove())
            await state.finish(); return

        keyboard = types.ReplyKeyboardMarkup(resize_keyboard = True, selective = True)
        for report in reports: keyboard.add(f'Проверить UID: {report}')
        keyboard.add('Отмена')
        await message.answer(msg.set('Какую заявку вы хотите проверить?', 'Система репортов'), reply_markup = keyboard)
        await ReportForm.PlayerCreate.set()

    else:
        await message.answer(msg.set('Используйте клавиатуру ниже!', 'Система репортов'))


@dp.message_handler(state=ReportForm.PlayerCreate)
async def reportPlayerCreate(message: types.Message, state: FSMContext):

    if message.text in 'Отмена':
        await message.answer(msg.set('Действие отменено...', 'Система репортов'), reply_markup = ReplyKeyboardRemove())
        await state.finish(); return
    elif Connect.readPlayer(UserID = message.text[15:]):
        await message.answer(msg.set('Используйте клавиатуру ниже!', 'Система репортов'))
        await state.finish(); return

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard = True, selective = True)
    keyboard.add('Назначить способности')
    keyboard.add('Без способностей')
    keyboard.add('Отклонить')
    keyboard.add('Отложить')

    data = Connect.readPlayer(UserID = message.text[15:], Table = 'CreatedPlayers') #File.read('data/profiles/', f'{message.text[15:]}.dat')
    await message.answer(msg.set(f"Данные о персонаже:\nИмя: {data['name']}\nПол: <i>{data['gender']}</i>\nВозраст: <i>{data['age']}</i>\nРаса: <i>{data['species']}</i>\nВнешность: <i>{data['appearance']}</i>\nХарактер: <i>{data['character']}</i>\nРацион питания: <i>{data['diet']}</i>\nИстория: <i>{data['story']}</i>\n\n<b>Примечание: Вы должны подобрать способности для этого персонажа.</b>", 'Система репортов'), reply_markup = keyboard)
    async with state.proxy() as data:
        data['UserID'] = message.text[15:]
    await ReportForm.Done.set()

@dp.message_handler(state=ReportForm.Done)
async def reportPlayerCreate(message: types.Message, state: FSMContext):
    
    if message.text in 'Назначить способности':
        keyboard = types.ReplyKeyboardMarkup()
        for power in powers: keyboard.add(power)
        await message.answer(msg.set('Выберите способность, которую назначите этому персонажу.', 'Система репортов'), reply_markup = keyboard)
        await state.finish(); return
    elif message.text in 'Без способностей':
        await message.answer(msg.set('Анкета успешно принята!\n\n<b>Данная функция будет удалена!</b>', 'Система репортов (Pre-Alpha Функции)'), reply_markup = ReplyKeyboardRemove())
        async with state.proxy() as data:
            player = Connect.readPlayer(UserID = data['UserID'], Table = 'CreatedPlayers')
            Connect.addPlayer(UserID = data['UserID'], Data = player)
            Connect.deletePlayer(UserID = data['UserID'], Table = 'CreatedPlayers')
            Console.log(f'Принята анкета с UserID: {data["UserID"]}', 'Репорты')
        await state.finish()
    elif message.text in 'Отложить':
        await message.answer(msg.set('Вы отложили просмотр репортов', 'Система репортов'), reply_markup = ReplyKeyboardRemove())
        await state.finish(); return
    elif message.text in 'Отклонить':
        await message.answer(msg.set('Опишите причину отклонения анкеты ниже', 'Система репортов'), reply_markup = ReplyKeyboardRemove())
        await ReportForm.PlayerCreateDeny.set()
    else:
        await message.answer(msg.set('Используйте клавиатуру ниже!', 'Система репортов'))

@dp.message_handler(state=ReportForm.PlayerCreateDeny)
async def reportPlayerCreate(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        TelegramID = Database.search('UserID', data['UserID'], 'TelegramID')
        if TelegramID != None:
            await bot.send_message(TelegramID, msg.set(f'Вашу анкету отклонили по причине:\n<i>{message.text}</i>\n\n<b>Примечание: Вы можете повторно подать заявку на создания персонажа.</b>', 'Создание игрового персонажа'))
        else:
            await message.answer(msg.set('Анкета успешно отклонена!\n\n<b>Пользователь не может получить уведомление о отклонении, так как он не авторизован в аккаунте</b>', 'Система репортов'), reply_markup = ReplyKeyboardRemove())
            Connect.deletePlayer(UserID = data['UserID'], Table = 'CreatedPlayer')
            await state.finish(); return
    await message.answer(msg.set('Анкета успешно отклонена!', 'Система репортов'), reply_markup = ReplyKeyboardRemove())
    Connect.deletePlayer(UserID = data['UserID'], Table = 'CreatedPlayer')
    await state.finish()