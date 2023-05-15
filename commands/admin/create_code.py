#class State_create_code(StatesGroup):
#    code_generate = State()
#
#@dp.message_handler(commands='create_code')
#async def create_code(message: types.Message):
#
#    if Connect.check_player(message, type = 'admin'):
#        keyboard = types.ReplyKeyboardMarkup(resize_keyboard = True, selective = True)
#        keyboard.add('Создание кода мироздания')
#
#        await message.answer(msg.add('Для создания кода, выберите какой код вы хотите создать.'), reply_markup = keyboard)
#        await State_create_code.code_generate.set()
#
#@dp.message_handler(state = State_create_code.code_generate)
#async def confirmation_unreg(message: types.Message, state: FSMContext):
#
#    global code_universe; code_universe = str(random.randrange(100000, 999999, 1))
#
#    await message.answer(msg.add(f'Генерация кода завершена!\n\n<b>Код мироздания: {code_universe}</b>\nДанный код будет доступен до конца сессии!\n(Данная функция неактиван, так как мироздание имеет UID: 0)'), reply_markup = ReplyKeyboardRemove())
#    await state.finish()