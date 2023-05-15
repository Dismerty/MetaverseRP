from dispatcher import dp, bot

from aiogram import types
from aiogram.dispatcher.storage import FSMContext

from libs.GameAssets import GameAssets
from libs.ChatLogger import ChatLogger
from libs import Connect, Console, Database, msg

@dp.message_handler(perms = 'bot.command.kick', commands = ['kick', 'лшсл'], commands_prefix = ['/', '.'], state = ChatLogger.GameChatState)
async def ChatCommandKick(message: types.Message, state: FSMContext):

    args = message.text.split(' ')
    UserID = Database.UserID(message)
    data = Connect.readPlayer(message)

    if len(args) == 1:
        await message.answer(msg.set('Команда /kick (ID) [-account] [-s]\n\n* Аргументы:\naccount - Кикает игрока с аккаунта.\ns - Кикает игрока без оповещения других игроков.\n\n<i>Используйте, чтобы кикнуть игрока с игрового чата.</i>'))
        return

    elif args[1].isdigit() is False:
        await message.answer(msg.set('Чтобы кикнуть игрока, нужно указать его ID.'))
        return
    
    elif int(args[1]) == UserID:
        await message.answer(msg.set('Вы не можете кикнуть самого себя!'))
        return

    if GameAssets.checkLocation(int(args[1])) == False:
        await message.answer(msg.set('Вы не можете кикнуть данного игрока, так как он находится не в чате!'))
        return

    TelegramID = Database.search('UserID', int(args[1]), 'TelegramID')
    kickedPlayer = Connect.readPlayer(TelegramID)

    GameAssets.removePlayerLocation(args[1])

    state = dp.current_state(chat = TelegramID, user = TelegramID)
    await state.set_state(await state.finish())

    arguments = []
    if len(args) >= 3:
        for a in args:
            if a != args[0] and a != args[1]:
                arguments.append(a)
    
    if '-account' in arguments:
        Database.logoutAccount(int(TelegramID))

        Console.log(f"{data['name']} исключил(а) игрока {kickedPlayer['name']} из аккаунта!")
        await message.answer(msg.set(f"Вы исключили игрока “{kickedPlayer['name']}” из аккаунта."))
        await bot.send_message(TelegramID, msg.set(f"Вы были исключены из аккаунта администратором “{data['name']}”!"), parse_mode = types.ParseMode.HTML)
    else:
        Console.log(f"{data['name']} исключил(а) игрока {kickedPlayer['name']} из чата!")
        await message.answer(msg.set(f"Вы исключили игрока “{kickedPlayer['name']}” из чата."))
        await bot.send_message(TelegramID, msg.set(f"Вы были исключены из чата администратором “{data['name']}”!"), parse_mode = types.ParseMode.HTML)
    
    if '-s' not in arguments:
        await ChatLogger.sendMessage(message, f"Администратор “{data['name']}” исключил игрока “{kickedPlayer['name']}” из чата.", [TelegramID])