import re
from aiogram import types
from aiogram.dispatcher.filters import BoundFilter

from libs.ConnectID import Database

class Perms(BoundFilter):

    key = 'perms'

    def __init__(self, perms: str):
        self.perms = perms
    
    async def check(self, message: types.Message) -> bool:
        UserPermsList = Database.perms(message)
        if UserPermsList == False: return False

        for User in UserPermsList:
            ul = User.split('.'); pl = self.perms.split('.')
            regex = "^[a-z.]+$"; pattern = re.compile(regex)
            if not pattern.search(self.perms) or '' in pl: return False
            if '*' in ul and len(ul) <= len(pl) and not len(ul) > len(pl):
                for i in range(0, min(len(ul), len(pl))):
                    if '*' in ul[i]: return True
                    elif ul[i] != pl[i]: return False
                return True
            elif not '*' in ul and not len(ul) < len(pl) and len(ul) == len(pl) and not len(ul) > len(pl):
                for i in range(0, min(len(ul), len(pl))):
                    if ul[i] != pl[i]: return False
                return True
            else: return False