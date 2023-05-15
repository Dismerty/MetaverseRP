from dispatcher import dp

from libs import msg
from aiogram import types

@dp.message_handler(perms = 'bot.command.stop', commands = ['stop', 'ыещз'], commands_prefix = ['/', '.'])
async def ChatCommandStop(message: types.Message):

    await message.answer(msg.add('Данная функция не работает из-за несовместимости Aiogram с Telegram API'))
    
    #Console.log(f"Администратор “{Player(message).name}” завершает работу бота.")
    #await bot.close()