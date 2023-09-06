"""
* GamePocess - библиотека для обработки каждой игровой механики
(В некоторых случаях может понадобиться отдельная папка )
"""

from libs.ConsoleLib import Console
from libs.ConnectID import Connect, Database, db, sql

import sqlite3, json, os, asyncio

from dispatcher import dp
from aiogram import types
from typing import Any, Union

class Player:

    class UserID:

        def __init__(self, UserID: int) -> None:
            self.UserID: int = UserID
            self.TelegramID: int = Database.TelegramID(self.UserID)

            self.login: str = Database.search('TelegramID', self.TelegramID, 'Login')
            self.password: str = Database.search('TelegramID', self.TelegramID, 'Password')
            self.data: dict = Connect.readPlayer(self.TelegramID)

            self.name: str = self.data['name']
            self.realName: str = self.data['realName']
            self.gender: str = self.data['gender']
            self.age: Union[int, str] = self.data['age']
            self.species: str = self.data['species']
            self.appearance: str = self.data['appearance']
            self.character: str = self.data['character']
            self.diet: str = self.data['diet']
            self.story: str = self.data['story']

            self.health: health = health(self.TelegramID)
            self.satiety: satiety = satiety(self.TelegramID)

            self.level: int = self.data['level']
            self.experience: int = self.data['experience']
            self.inventory: dict = self.data['inventory']
            self.capabilities: dict = self.data['capabilities']

        def move(self, LocationID: str) -> None:
            """Помещает или перемещает игрока на локацию в зависимости от ситуации.

            Аргументы:
                LocationID (str): ID локации на которую должен попасть игрок.
                TelegramID (int, optional): Можно передать как и всё сообщение, так и чисто TelegramID. Значение по умолчанию None.
                UserID (int, optional): ID игрового аккаунта. Значение по умолчанию None.
            """
            sql.execute(f"SELECT LocationID FROM listLocations WHERE LocationID = '{LocationID}'")
            if sql.fetchone() is None: return False

            sql.execute(f"DELETE FROM Locations WHERE UserID = '{self.UserID}'")
            sql.execute(f"SELECT LocationID FROM Locations WHERE UserID = {self.UserID}")
            if sql.fetchone() is None:
                sql.execute(f"INSERT INTO locations VALUES (?, ?)", (self.UserID, LocationID))
                db.commit()
                return True
        
        def location(self) -> str:
            sql.execute(f"SELECT LocationID FROM Locations WHERE UserID = {self.UserID}")
            return sql.fetchone()[0]

        def kick(self) -> bool:
            """Убирает игрока с локации.

            Аргументы:
                UserID (int): ID игрового аккаунта.
            """
            sql.execute(f"SELECT LocationID FROM Locations WHERE UserID = {self.UserID}")
            if sql.fetchone() is not None:
                sql.execute(f"DELETE FROM Locations WHERE UserID = {self.UserID}")
                db.commit(); return True
            else: return False

    class TelegramID:

        def __init__(self, TelegramID: Union[int, types.Message]) -> None:
            self.UserID: int = Database.UserID(TelegramID)
            if isinstance(TelegramID, types.Message):
                self.TelegramID: int = TelegramID.from_user.id

            self.login: str = Database.search('TelegramID', self.TelegramID, 'Login')
            self.password: str = Database.search('TelegramID', self.TelegramID, 'Password')
            self.data: dict = Connect.readPlayer(self.TelegramID)

            self.name: str = self.data['name']
            self.realName: str = self.data['realName']
            self.gender: str = self.data['gender']
            self.age: Union[int, str] = self.data['age']
            self.species: str = self.data['species']
            self.appearance: str = self.data['appearance']
            self.character: str = self.data['character']
            self.diet: str = self.data['diet']
            self.story: str = self.data['story']

            self.health: health = health(self.TelegramID)
            self.satiety: satiety = satiety(self.TelegramID)

            self.level: int = self.data['level']
            self.experience: int = self.data['experience']
            self.inventory: dict = self.data['inventory']
            self.capabilities: dict = self.data['capabilities']

        def move(self, LocationID: str) -> None:
            """Помещает или перемещает игрока на локацию в зависимости от ситуации.

            Аргументы:
                LocationID (str): ID локации на которую должен попасть игрок.
                TelegramID (int, optional): Можно передать как и всё сообщение, так и чисто TelegramID. Значение по умолчанию None.
                UserID (int, optional): ID игрового аккаунта. Значение по умолчанию None.
            """
            sql.execute(f"SELECT LocationID FROM listLocations WHERE LocationID = '{LocationID}'")
            if sql.fetchone() is None: return False

            sql.execute(f"DELETE FROM Locations WHERE UserID = '{self.UserID}'")
            sql.execute(f"SELECT LocationID FROM Locations WHERE UserID = {self.UserID}")
            if sql.fetchone() is None:
                sql.execute(f"INSERT INTO locations VALUES (?, ?)", (self.UserID, LocationID))
                db.commit()
                return True

        def location(self) -> str:
            sql.execute(f"SELECT LocationID FROM Locations WHERE UserID = {self.UserID}")
            return sql.fetchone()[0]

        def kick(self) -> bool:
            """Убирает игрока с локации.

            Аргументы:
                UserID (int): ID игрового аккаунта.
            """
            sql.execute(f"SELECT LocationID FROM Locations WHERE UserID = {self.UserID}")
            if sql.fetchone() is not None:
                sql.execute(f"DELETE FROM Locations WHERE UserID = {self.UserID}")
                db.commit(); return True
            else: return False

    def check(UserID: int) -> bool:
        """Проверка на то, был ли персонаж создан.

        Аргументы:
            UserID (int): принимает UserID игрока

        Возращает:
            bool: True или False
        """
        sql.execute(f"SELECT * FROM Players WHERE UserID = {UserID}")
        if sql.fetchone() is None: return False
        return True

class health:
    
    def __init__(self, TelegramID) -> None:
        self.data: dict = Connect.readPlayer(TelegramID)
        self.value: int = self.data['health'][0]
        self.max: int = self.data['health'][1]

class satiety:
    
    def __init__(self, TelegramID) -> None:
        self.data = Connect.readPlayer(TelegramID)
        self.value = self.data['satiety'][0]
        self.max = self.data['satiety'][1]

class Location():

    def __init__(self, LocationID: str) -> None:

        self.LocationID = LocationID
        
        for value in sql.execute(f"SELECT Data FROM listLocations WHERE LocationID = '{self.LocationID}'"):
            self.data = json.loads(value[0])

        self.id = self.data['ID']
        self.name = self.data['Name']
        self.description = self.data['Description']
        self.capabilities = self.data['Capabilities']

    def load() -> None:
        """Функция `load()` полностью считывает файлы локаций и загружает в игру.
        Если локаций нет в папке, загружается локация пустота как значение по умолчанию.
        """
        sql.execute(f"DELETE FROM listLocations")

        if os.listdir('assets/locations') == []:
            sql.execute(f"INSERT INTO listLocations VALUES (?, json(?))", ('void', json.dumps({"ID":"void", "Name": "Пустота", "Spawn": True})))

        for file in os.listdir('assets/locations'):
            with open(f'assets/locations/{file}', encoding = 'UTF-8') as f:
                Data = json.load(f)
                
                sql.execute(f"INSERT INTO listLocations VALUES (?, json(?))", (Data['ID'], json.dumps(Data)))
        db.commit()

    def list() -> dict:
        """Функция `list()` считывает db и выдаёт словарь локаций.

        Возращает:
            dict: Весь список локаций со значениями в виде JSON объекта. Пример {LocationID: Data}.
        """
        locations = []

        for value in sql.execute("SELECT * FROM listLocations"):
            locations.append(value[0])
        
        return locations

    def spawn() -> dict:
        """Возвращает локацию со спавном.

        Возращает:
            dict: Место спавна игроков.
        """

        for spawnLocation in sql.execute("SELECT Data FROM listLocations, json_each(Data, '$.Spawn') WHERE json_each.value = true"):
            return json.loads(spawnLocation[0])['ID']

class GameAssets:
    """Игровые ресурсы

    С помощью этой функции вы сможете получить все игровые данные о игроке.
    От имени персонажа до слотов его инвентаря.
    """
    
    def readLocation(message: types.Message):
        """Получает информацию о локации на которой находится игрок.

        Аргументы:
            message (_type_): _description_

        Возращает:
            _type_: _description_
        """
        UserID = Database.UserID(message)

        for location in sql.execute(f"SELECT LocationID FROM Locations WHERE UserID = {UserID}"):
            location = location[0]
        
        for value in sql.execute(f"SELECT Data FROM listLocations WHERE LocationID = '{location}'"):
            return json.loads(value[0])
    
    def addPlayerLocation(LocationID: str, TelegramID: int):
        """Добавляет игрока на локацию.

        Аргументы:
            LocationID (str): ID локации на которую должен попасть игрок.
            TelegramID (int, optional): Можно передать как и всё сообщение, так и чисто TelegramID. Значение по умолчанию None.
            UserID (int, optional): ID игрового аккаунта. Значение по умолчанию None.
        """
        UserID = Database.UserID(TelegramID)

        sql.execute(f"DELETE FROM Locations WHERE UserID = '{UserID}'")
        sql.execute(f"SELECT LocationID FROM Locations WHERE UserID = {UserID}")
        if sql.fetchone() is None:
            sql.execute(f"INSERT INTO locations VALUES (?, ?)", (UserID, LocationID))
            db.commit()
        
    def removePlayerLocation(UserID: str):
        """Убирает игрока с локации.

        Аргументы:
            UserID (str): ID игрового аккаунта.
        """

        sql.execute(f"SELECT LocationID FROM Locations WHERE UserID = {UserID}")
        if sql.fetchone() is not None:
            sql.execute(f"DELETE FROM locations WHERE UserID = {UserID}")
            db.commit()

    def checkLocation(UserID: int) -> Union[str, bool]:
        """Проверяет игрока в игровом чате и возращает локацию на которой он находится.
        Иначе вернёт False.

        Аргументы:
            UserID (int): ID игрового аккаунта.

        Возращает:
            Union[str, bool]: ID локации, иначе False.
        """

        sql.execute(f"SELECT LocationID FROM Locations WHERE UserID = {UserID}")
        if sql.fetchone() is None:
            return False

        for location in sql.execute(f"SELECT LocationID FROM Locations WHERE UserID = {UserID}"):
            return location[0] 
    
    def checkPlayersLocation(LocationID: str) -> Union[dict, bool]:

        sql.execute(f"SELECT * FROM Locations WHERE LocationID = '{LocationID}'")
        if sql.fetchone() is None: return False
        else:
            users = []; TelegramID = []
            for value in sql.execute(f"SELECT UserID FROM Locations WHERE LocationID = '{LocationID}'"):
                users.append(value[0])
                
            for user in users:
                for value in sql.execute(f"SELECT TelegramID FROM Accounts WHERE UserID = {user}"):
                    TelegramID.append(value[0])
            return TelegramID
    
    def checkAllPlayersLocation() -> Union[bool, list]:

        sql.execute(f"SELECT UserID FROM Locations")
        if sql.fetchone() is None: return False
        else:
            players = []
            for value in sql.execute(f"SELECT UserID FROM Locations"):
                players.append(value[0])
            return players

#def Player():
    
    #data = File.load('data/players/', f'{message.from_user.id}.dat')
    
    #name = 'test'
    #real_name: data['player']['real_name']
