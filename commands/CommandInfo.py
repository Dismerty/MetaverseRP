from aiogram import types

async def setDescriptionCommands(bot):
    await bot.set_my_commands([
        types.BotCommand("start", "Запустить бота"),
        types.BotCommand("help", "Помощь по командам"),
        types.BotCommand("info", "Информация о персонаже"),
        types.BotCommand("register", "Регистрация"),
        types.BotCommand("login", "Вход в аккаунт"),
        types.BotCommand("logout", "Выход из аккаунта")
    ])