"""
* ConnectID - библиотека для работы с файлами сохранения
"""

import os, sqlite3, hashlib, configparser, variables, json
from typing import Union
from math import inf
from libs.ConsoleLib import Console
from configuration import config

from aiogram.dispatcher.filters import BoundFilter
from aiogram import types

# Создание или загрузка базы данных
if not os.path.exists('data'): os.mkdir('data')

db = sqlite3.connect(f'data/ConnectID.db')
sql = db.cursor()

sql.execute("""CREATE TABLE IF NOT EXISTS Accounts 
(
    TelegramID INTEGER,
    Username TEXT,
    Login TEXT,
    Password TEXT,
    UserID INTEGER PRIMARY KEY AUTOINCREMENT
)
""")
sql.execute("""CREATE TABLE IF NOT EXISTS Players
(
    UserID INTEGER PRIMARY KEY AUTOINCREMENT,
    Data TEXT
)
""")
sql.execute("""CREATE TABLE IF NOT EXISTS CreatedPlayers
(
    UserID INTEGER REFERENCES Accounts (UserID) ON DELETE CASCADE,
    Data TEXT
);""")
sql.execute("""CREATE TABLE IF NOT EXISTS notifications 
(
    Login TEXT,
    Message TEXT
)
""")
sql.execute("""CREATE TABLE IF NOT EXISTS Permissions
(
    UserID INT,
    Permission TEXT
)
""")
sql.execute("""CREATE TABLE IF NOT EXISTS Locations
(
    UserID INTEGER,
    LocationID TEXT
)
""")
sql.execute("""CREATE TABLE IF NOT EXISTS listLocations
(
    LocationID TEXT,
    Data TEXT
)
""")
sql.execute(f"DELETE FROM Locations")
db.commit()

# Основной класс
class Connect():
    """Класс отвечающий за все действия над игроком.

    Функции в классе:
        `addPlayer()`: Создаёт файл персонажа.
        `readPlayer()`: Читает файл персонажа.
        `editPlayer()`: Редактирует файл персонажа.
        `deletePlayer()`: Удаляет файл персонажа.
    """

    def addPlayer(TelegramData: dict = None, UserID: int = None, Data: dict = '{}', Table: str = 'Players') -> None:
        """Функция `addPlayer()` создающая файл персонажа,
        если не указана переменная 'data', то создаётся файл с пустым значением.
        """
        if UserID == None:
            UserID = Database.UserID(TelegramData)

        sql.execute(f"INSERT INTO {Table} VALUES (?, json(?))", (UserID, json.dumps(Data)))
        db.commit()
    
    def readPlayer(TelegramData: dict = None, UserID: int = None, Table: str = 'Players') -> dict:
        """Функция `readPlayer()` считывает файл и выдаёт словарь значений игрока.

        Аргументы:
            TelegramData (_type_): Можно передать как и всё сообщение, так и чисто TelegramID.

        Возращает:
            dict: Все данные о игроке.
        """
        if UserID == None:
            UserID = Database.UserID(TelegramData)

        for value in sql.execute(f"SELECT * FROM {Table} WHERE UserID = '{UserID}'"):
            return json.loads(value[1])

    def editPlayer(Data = '{}', UserID = 1):
        """* Редактирование данных игрока"""

        sql.execute(f"DELETE FROM Players WHERE UserID = '{UserID}'")
        sql.execute(f"INSERT INTO Players VALUES (?, json(?))", (UserID, json.dumps(Data)))
        db.commit()

    def deletePlayer(TelegramData: dict = None, UserID: int = None, Table: str = 'Players') -> bool:
        """Функция `deletePlayer()` удаляет игровой файла персонажа

        Аргументы:
            TelegramData (_type_): Можно передать как и всё сообщение, так и чисто TelegramID.

        Возвращает:
            bool: True или False.
        """
        if UserID == None:
            UserID = Database.UserID(TelegramData)

        sql.execute(f"DELETE FROM {Table} WHERE UserID = '{UserID}'")
        db.commit()

    def checkPlayer(TelegramID) -> bool:
        """Функция `checkPlayer()` проверяет существование пользователя по базе данных, а также игровой аккаунт.

        Аргументы:
            TelegramData (_type_): Можно передать как и всё сообщение, так и чисто TelegramID.

        Возвращает:
            bool: True или False.
        """

        UserID = Database.UserID(TelegramID)

        sql.execute(f"SELECT * FROM Players WHERE UserID = {UserID}")
        if sql.fetchone() is None: return False
        return True
    
    def listPlayers(Table: str = 'Players') -> Union[int, bool]:
        ListUserID = []

        sql.execute(f"SELECT * FROM {Table}")
        if sql.fetchone() is None: return False
        for value in sql.execute(f"SELECT UserID FROM {Table}"):
            ListUserID.append(value[0])
        return ListUserID

class Database():
    """
    * Класс дающий возможность работать с базами данных
    """

    def UserID(TelegramID: Union[int, types.Message]) -> Union[int, bool]:
        """Функция `UserID()` считывает UserID игрока из базы данных используя TelegramID.

        Аргументы:
            TelegramData (_type_): Можно передать как и всё сообщение, так и чисто TelegramID.

        Возвращает:
            int: UserID игрока.
        """
        if isinstance(TelegramID, types.Message):
            TelegramID = TelegramID.from_user.id

        sql.execute(f"SELECT UserID FROM Accounts WHERE TelegramID = '{TelegramID}'")
        if sql.fetchone() is None: return False
        for value in sql.execute(f"SELECT UserID FROM Accounts WHERE TelegramID = '{TelegramID}'"):
            return value[0]
    
    def TelegramID(UserID: int) -> Union[int, bool]:
        """Функция `TelegramID()` считывает TelegramID пользователя из базы данных используя UserID.

        Аргументы:
            UserID (int): Можно передать UserID.

        Возвращает:
            int: TelegramID пользователя.
        """
        sql.execute(f"SELECT TelegramID FROM Accounts WHERE UserID = {UserID}")
        if sql.fetchone() is None: return False
        for value in sql.execute(f"SELECT TelegramID FROM Accounts WHERE UserID = {UserID}"):
            return value[0]

    def addAccount(TelegramData, Login, Password, Log = False):
        """Функция для создания нового аккаунта в базе данных

        Аргументы:
            TelegramData (_type_): Можно передать только сообщение (types.Message).
            Login (_type_): Логин игрока
            Password (_type_): Пароль игрока
            Log (bool, optional): Логирование действия. По умолчанию False.
        """

        sql.execute("""SELECT MAX(UserID) FROM Accounts""")
        UserID = sql.fetchone()[0]; UserID += 1

        sql.execute(f"INSERT INTO Accounts VALUES (?, ?, ?, ?, ?)", (TelegramData.from_user.id, TelegramData.from_user.username, Login, Password, UserID))
        db.commit()
        Console.log(f'Создан новый аккаунт. Данные о аккаунте:', 'ConnectID', Log)
        Console.log(f'Username: @{TelegramData.from_user.username}, TelegramID: {TelegramData.from_user.id}, игровой UserID: {UserID}.', 'ConnectID', Log)

    def edit(TelegramData, Key, Value, NewValue):
        """* Функция для редактирования значений в базе данных по ключу и значению"""

        sql.execute(f"UPDATE Accounts SET {Key} = {Value} WHERE {Key} = '{NewValue}'")
        db.commit()

    def logoutAccount(TelegramData: types.Message):
        """* Функция выхода из аккаунта"""

        sql.execute(f"UPDATE Accounts SET TelegramID = ? WHERE TelegramID = '{TelegramData.from_user.id}'", (None, ))
        sql.execute(f"UPDATE Accounts SET Username = ? WHERE Username = '{TelegramData.from_user.username}'", (None, ))
        db.commit()

    def checkLogin(TelegramData, Login):
        """* Функция для проверки существования логина, а также проверять, авторизован ли другой пользователь под этим аккаунтом"""

        sql.execute(f"SELECT TelegramID FROM Accounts WHERE Login = '{Login}'")
        if sql.fetchone() is None: return False
        else: return True
    
    def login(TelegramData, Login, Password) -> bool:
        """* Функция для входа в аккаунт"""

        for value in sql.execute(f"SELECT * FROM Accounts WHERE Login = '{Login}'"):
            if value[3] == Password and value[0] == None:
                sql.execute(f"UPDATE Accounts SET TelegramID = ? WHERE Login = '{Login}'", (TelegramData.from_user.id, ))
                sql.execute(f"UPDATE Accounts SET Username = ? WHERE Login = '{Login}'", (TelegramData.from_user.username, ))
                db.commit()
                return True
            else:
                return False

    def deleteAccount(TelegramData):
        """Функция deleteAccount() удаляет игровой файл и аккаунт с базы данных.

        Аргументы:
            TelegramData (_type_): Можно передать только сообщение (types.Message).

        Возвращает:
            int: UserID игрока.
        """

        for value in sql.execute(f"SELECT * FROM Accounts WHERE TelegramID = '{TelegramData.from_user.id}'"):
            Connect.deletePlayer(value[4])
            Console.log(f'Аккаунт удалён, Username: @{TelegramData.from_user.username}, TelegramID: {TelegramData.from_user.id}, игровой UID: {value[4]}.', 'ConnectID')

        sql.execute(f"DELETE FROM Accounts WHERE TelegramID = '{TelegramData.from_user.id}'")
        db.commit()

    def search(Key: str, Value: Union[str, int], ReturnValue: Union[str, int, tuple] = 'All', Table: str = 'Accounts', Log = False) -> Union[str, int, tuple]:
        """Функция проводит поиск по ключу и значению в базе данных, и возращает значения если они существуют в базе.
        Также можно выключить логирование в консоли.

        Аргументы:
            Key (str): По какому столбцу будет произведён поиск.
            Value (Union[str, int]): Какое значение должно быть у столбца.
            ReturnValue (Union[str, int, tuple], optional): Какое значение будет возвращено. По умолчанию 'All'.
            Table (str): Какая таблица используется для поиска. По умолчанию 'Accounts'.
            Log (bool, optional): Выводит полученные значения в консоль. По умолчанию False.

        Возвращает:
            Union[str, int, tuple]: Строку, число или кортеж.
        """
        
        sql.execute(f"SELECT * FROM {Table} WHERE {Key} = '{Value}'")
        if sql.fetchone() is None: return False
        else:
            for value in sql.execute(f"SELECT * FROM Accounts WHERE {Key} = '{Value}'"):
                Console.log('TelegramID, Username, Login, Password, UserID', 'ConnectID/Debug', Log)
                Console.log(f'[Debug] {value}', 'ConnectID', Log)
                if ReturnValue == 'TelegramID': return value[0]
                elif ReturnValue == 'Username': return value[1]
                elif ReturnValue == 'Login': return value[2]
                elif ReturnValue == 'Password': return value[3]
                elif ReturnValue == 'UserID': return value[4]
                elif ReturnValue == 'All': return value

    def check(TelegramData) -> bool:
        """Функция `check()` проверяет авторизован ли пользователь в аккаунте и возращает True/False.

        Аргументы:
            TelegramData (_type_): Можно передать как и всё сообщение, так и чисто TelegramID.

        Возращает:
            bool: True или False
        """

        if isinstance(TelegramData, int): TelegramID = TelegramData
        else: TelegramID = TelegramData.from_user.id

        sql.execute(f"SELECT TelegramID FROM Accounts WHERE TelegramID = '{TelegramID}'")
        if sql.fetchone() is None: return False
        else: return True
    
    def perms(TelegramData):

        UserID = Database.UserID(TelegramData)

        if UserID != False or UserID == 0:
            sql.execute(f"SELECT Permission FROM Permissions WHERE UserID = {UserID}")
            if sql.fetchone() is None: return False
            else:
                perms = []
                for value in sql.execute(f"SELECT Permission FROM Permissions WHERE UserID = {UserID}"):
                    perms.append(value[0])
                return perms
        else: return False

    def read(TelegramData) -> Union[dict, bool]:
        """* Функция читает базу данных по TelegramID и выдаёт информацию об аккаунте, если она есть."""
        
        if isinstance(TelegramData, int): TelegramID = TelegramData
        else: TelegramID = TelegramData.from_user.id

        sql.execute(f"SELECT TelegramID FROM Accounts WHERE TelegramID = '{TelegramID}'")
        if sql.fetchone() is None: return False
        else: 
            for value in sql.execute(f"SELECT * FROM Accounts WHERE TelegramID = '{TelegramID}'"):
                return value

    def readAll() -> None:
        """
        Функция читает всю базу данных и выводит все значения в консоль.
        Нужна для отладки в самом коде.
        """

        
        for value in sql.execute("SELECT * FROM Accounts"):
            Console.log('TelegramID, Username, Login, Password, UID, Settings, Permissions', 'ConnectID/All')
            Console.log(value, 'ConnectID/Debug')

Console.log('Библиотека успешно загружена!', 'ConnectID')

class Account:

    def __init__(self, message: types.Message) -> None:

        sql.execute(f"SELECT * FROM Accounts WHERE TelegramID = '{message.from_user.id}'")
        if sql.fetchone() is None:
            self.TelegramID = None
            self.Username = None
            self.Login = None
            self.Password = None
            self.UserID = None
            self.created = False

        else:
            sql.execute(f"SELECT * FROM Accounts WHERE TelegramID = '{message.from_user.id}'")
            data = sql.fetchone()
            self.TelegramID = data[0]
            self.Username = data[1]
            self.Login = data[2]
            self.Password = data[3]
            self.UserID = data[4]
            self.created = True

# Свои фильтры для удобной работы с ботом
class AccountCreated(BoundFilter):

    key = 'AccountCreated'

    def __init__(self, AccountCreated: bool) -> None:
        self.AccountCreated = AccountCreated

    async def check(self, message: types.Message) -> bool:
        if self.AccountCreated == True: return Database.check(message)
        else: return not Database.check(message)

class CharacterCreated(BoundFilter):

    key = 'CharacterCreated'

    def __init__(self, CharacterCreated: bool) -> None:
        self.CharacterCreated = CharacterCreated
    
    async def check(self, message: types.Message) -> bool:
        if self.CharacterCreated == True: Connect.checkPlayer(message)
        else: return not Connect.checkPlayer(message)

# 
# Создание первого аккаунта относящегося к мирозданию
#
sql.execute(f"SELECT TelegramID FROM Accounts WHERE Login = 'Universe'")
if sql.fetchone() is None:

    __TelegramID = None
    __Username = None

    password = 'Universe'
    # Создание объекта хеша SHA-256
    sha256 = hashlib.sha256()
    # Обновление хеша с данными
    sha256.update(password.encode('utf-8'))
    # Получаем результат в виде шестнадцатеричной строки
    result = sha256.hexdigest()

    if config['Account']['AutoLogin']['TelegramID'] != None and config['Account']['AutoLogin']['Username'] != None:
        __TelegramID = config['Account']['AutoLogin']['TelegramID']
        __Username = config['Account']['AutoLogin']['Username']
        Console.log('Автоматический вход в аккаунт. Логин: Universe', 'ConnectID')
        Console.log(f'Username: @{__Username}, TelegramID: {__TelegramID}.', 'ConnectID')
        
    Console.worn('Аккаунт мироздания не найден, создание нового аккаунта.', 'ConnectID')
    sql.execute(f"INSERT INTO Accounts VALUES (?, ?, ?, ?, ?)", (__TelegramID, __Username, 'Universe', result, 0))
    sql.execute(f"INSERT INTO Permissions VALUES (?, ?)", (0, '*'))
    db.commit()
    Console.log('Аккаунт мироздания создан. UserID: 0')

sql.execute(f"SELECT UserID FROM Players WHERE UserID = 0")
if sql.fetchone() is None:
    Console.worn('Персонаж мироздания не найден, создание нового персонажа.', 'ConnectID')
    Universe = variables.get("player")
    Universe['name'] = 'Мироздание'
    Universe['realName'] = 'Ноэр'
    Universe['gender'] = 'Неизвестно'
    Universe['age'] = 0
    Universe['species'] = 'Неизвестно'
    Universe['appearance'] = 'Неизвестно'
    Universe['character'] = 'Неизвестно'
    Universe['diet'] = 'Неизвестно'
    Universe['story'] = 'Неизвестно'
    Universe['level'] = '???'
    Universe['experience'] = '???'
    db = sqlite3.connect('data/ConnectID.db')
    sql = db.cursor()

    sql.execute(f"INSERT INTO Players VALUES (?, json(?))", (0, json.dumps(Universe)))
    db.commit()
    Console.log('Персонаж мироздания создан.')