"""
*  Первоначальная команда
"""
from dispatcher import dp
from libs import msg

from aiogram import types

from configuration import config
game = config['Settings']['Game']

@dp.message_handler(AccountCreated = False, commands = ['start', 'ыефке'], commands_prefix = ['/', '.'])
async def starting(message: types.Message):
    MessageModifier = '''

<i>Cоздайте аккаунт командой /register.
Если уже у вас есть аккаунт, то пропишите /login.</i>'''

    await message.answer(msg.add(f'Добро пожаловать в игровое пространство <a href="https://vk.com/metaverse_rpg_project">{game}</a>!{MessageModifier}'), disable_web_page_preview = True)

@dp.message_handler(CharacterCreated = False, commands = ['start', 'ыефке'], commands_prefix = ['/', '.'])
async def starting(message: types.Message):
    MessageModifier = '''

<i>Cоздайте персонажа командой /create.</i>'''

    await message.answer(msg.add(f'Добро пожаловать в игровое пространство <a href="https://vk.com/metaverse_rpg_project">{game}</a>!{MessageModifier}'), disable_web_page_preview = True)

@dp.message_handler(commands = 'start')
async def starting(message: types.Message):
    
    MessageModifier = '\n\n<i>Пропишите команду /chat чтобы начать играть.</i>'

    await message.answer(msg.add(f'Добро пожаловать в игровое пространство <a href="https://vk.com/metaverse_rpg_project">{game}</a>!{MessageModifier}'), disable_web_page_preview = True)