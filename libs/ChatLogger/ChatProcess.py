"""
* ChatLogger - библиотека для работы с игровым чатом
"""
from dispatcher import bot

from libs.ConnectID import Database
from libs.GameAssets import GameAssets
from .ChatScanner import ChatScanner
from libs import Console, msg, colors

import yaml
from typing import Union

from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types

with open('config.yml', 'r') as file:
    config = yaml.safe_load(file)

'''company = config['Settings']['Game']
ability = ['регенерация', 'регенерацию']

class ChatScanner():

    def action(TelegramData: Union[dict, str], Actions: list) -> dict:
        if isinstance(TelegramData, str): text = TelegramData
        else: text = TelegramData.text

        line = 0; actions = []
        while text.find('[', line) != -1:
            line = text.find('[', line)
            end = text.find(']', line)

            for p in Actions:
                if text.casefold()[line - len(p):line] == p and text[line + 1:end].isdigit():
                    actions.append([text[line - len(p):line], int(text[line + 1:end])])
            line += end - line

        edit = text
        for d in actions:
            edit = edit.replace(f'{d[0]}[{d[1]}]', f'{d[0]}', 1)
            d[0] = d[0].lower()
        return [edit, actions]'''

class ChatLogger(StatesGroup):
    # Состояние чата, игрок находясь в состоянии чата может писать сообщения другим игрокам, а
    # также выполнять команды разрешённые в чате.
    GameChatState = State()

    async def log(TelegramData: types.Message, data: dict):
        """Функция `log()` выводит в консоль сообщение отправленное игроком в чат.

        Аргументы:
            TelegramData (dict): Можно передать только сообщение (types.Message).
            data (dict): Значение с данными игрока.
        """
        UserID = Database.UserID(TelegramData)
        if len(TelegramData.text.split("\n")) == 1:
            Console.log(f"{colors.gray}({colors.green}{TelegramData.from_user.id}/{UserID}{colors.gray}){colors.green} {data['name']} - {'∞' if data['level'] >= 1000000 else data['level']} уровень > {TelegramData.text}", f"Chat/{GameAssets.readLocation(TelegramData)['Name']}", custom = True)
        else:
            msg = TelegramData.text.split("\n")
            Console.log(f"{colors.gray}({colors.green}{TelegramData.from_user.id}/{UserID}{colors.gray}){colors.green} {data['name']} - {'∞' if data['level'] >= 1000000 else data['level']} уровень:", f"Chat/{GameAssets.readLocation(TelegramData)['Name']}", custom = True)
            for msg in msg:
                Console.log(f'{colors.gray}({colors.green}{TelegramData.from_user.id}/{UserID}{colors.gray}){colors.green}  {msg}', f'Chat/{GameAssets.readLocation(TelegramData)["Name"]}', custom = True)

    async def sendMessage(TelegramData: dict, text: str, NotSendMessage: list):

        if text == None: text = TelegramData.text
        for player in GameAssets.checkAllPlayersLocation():
            if Database.TelegramID(player) != False:
                TelegramID = Database.TelegramID(player)
                if TelegramID != TelegramData.from_user.id and TelegramID not in NotSendMessage:
                    await bot.send_message(TelegramID, msg.set(text), parse_mode = types.ParseMode.HTML)
    

    async def sendMessageRP(TelegramMessage: types.Message,
                            data: dict,
                            text = None,
                            NotSendMessage: list = [],
                            Scanner = True) -> Union[list, None]:
        """Функция `sendMessageRP()` отправляет сообщение всем игрокам на локации.

        Аргументы:
            TelegramData (dict): Можно передать только сообщение (types.Message).
            data (dict): Значение с данными игрока.
            text (_type_, optional): Текст, который будет отправлен игрокам. Значение по умолчанию None.
        """
        if Scanner:
            scan = ChatScanner(TelegramMessage)

        await ChatLogger.log(TelegramMessage, data)
        UserID = Database.UserID(TelegramMessage)

        if text == None and not Scanner: text = TelegramMessage.text
        elif Scanner: text = scan.EditedMessage
        for TelegramID in GameAssets.checkPlayersLocation(GameAssets.readLocation(TelegramMessage)['ID']):

            if TelegramID != TelegramMessage.from_user.id and TelegramID not in NotSendMessage and text != '':
                await bot.send_message(TelegramID, f"<b>{UserID}. {data['name']} - {'∞' if data['level'] >= 1000000 else data['level']} уровень</b>\n{text}")
        
        if Scanner: return scan.Actions
    
    async def sendMessageNonRP(TelegramData: dict, Data: dict, text = None):
        """Функция `sendMessageNonRP()` отправляет сообщение в НонРП чат всем игрокам на локации.

        Аргументы:
            TelegramData (dict): Можно передать только сообщение (types.Message).
            data (dict): Значение с данными игрока.
            text (_type_, optional): Текст, который будет отправлен игрокам. Значение по умолчанию None.
        """
        await ChatLogger.log(TelegramData, Data)
        UserID = Database.UserID(TelegramData)

        if text == None: text = TelegramData.text
        for TelegramID in GameAssets.checkPlayersLocation(GameAssets.readLocation(TelegramData)['ID']):

            if TelegramID != TelegramData.from_user.id:
                await bot.send_message(TelegramID, f'<b>{UserID}. {Data["name"]} - NonRP</b>\n{text}', parse_mode = types.ParseMode.HTML)


'''
@dp.message_handler(state = ChatLogger.GameChat)
async def GameChat(message: types.Message):

    def decorator(func):
        def decorator2(*args, **kwargs):
            return func(*args, **kwargs)
        return decorator2
    return decorator
    #def decorator():
    #    GameFunction(Player = Player(message))
    #return decorator
    await ChatLogger.sendMessageRP(message, Player(message).data)

    if action[1] != []:
        for a in action[1][0]:
            Effects.addEffect(EffectsList.regeneration(a[1], 3))

    attack = ChatScanner.action(message)
    original = attack[0]
    edited = attack[1][0][0]
    print(attack)
    
    if attack[1] != []:
        player = GameAssets.readPlayer(message, attack[1][0][1])

        player['health'][0] -= 20
        GameAssets.editPlayer(player, attack[1][0][1])
        TelegramID = Database.TelegramID(attack[1][0][1])
        UserID = Database.UserID(message)

        await message.answer(msg.set(f'Вы атаковали игрока “{GameAssets.readPlayer(UserID = attack[1][0][1])["name"]}”'))
        
        if GameAssets.readPlayer(UserID = attack[1][0][1])["health"][0] <= 0:
            GameAssets.deletePlayer(UserID = attack[1][0][1])
            await bot.send_message(TelegramID, f"<b>{UserID}. {Data['name']} - {Data['level']} уровень</b>\n{message.text}\n\n<i>Вы потеряли оставшееся здоровье...</i>")
            await bot.send_message(TelegramID, msg.set(f'Ваш персонаж не смог противостоять самой смерти!...\n\n<i>Используйте команду /create для создания нового персонажа!</i>'))

            state = dp.current_state(chat = TelegramID, user = TelegramID)
            await state.set_state(await state.finish())
        else:
            await bot.send_message(TelegramID, f"<b>{UserID}. {Data['name']} - {Data['level']} уровень</b>\n{message.text}\n\n<i>Вы потеряли 20 ед. здоровья</i>")

        message.text = attack[0]
        await ChatLogger.sendMessageRP(message, Data, NotSendMessage = [TelegramID])
        return

    elif ChatScanner.Attack(message)[1] == [] and message.text.find('[') != -1 and message.text.find(']') != -1 and message.text.find('[') < message.text.find(']'):

        command = message.text[message.text.find('[') + 1:message.text.find(']')]

        if len(message.text[message.text.find('['):message.text.find(']')+1]) + 12 > len(message.text):
            await message.answer(msg.set('Переместиться на другую локацию можно РП путём!'))
            return

        elif command not in GameAssets.listLocations():
            await message.answer(msg.set('Такой локации не существует!'))
            return

        text = message.text.replace(f'[{command}]', '')
        if text != '': await ChatLogger.sendMessageRP(message, Data, text)
        GameAssets.addPlayerLocation(command, message.from_user.id)
        await message.answer(msg.set(f'Вы переместились на локацию: {GameAssets.readLocation(message)["Name"]}'))
        return

    elif '/help' in args[0] or '.рудз' in args[0]:
        await bot.send_message(message.from_user.id, msg.set('/help - открыть меню помощи\n/exit - выйти из игрового чата', 'Помощь'), parse_mode=types.ParseMode.HTML)
        return
'''
