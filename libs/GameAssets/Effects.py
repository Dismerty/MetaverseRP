
from libs import Console, Connect
import asyncio

class EffectsList():

    async def testEffect():
        Console.log('Начало тестового эффекта')
        await asyncio.sleep(5.0)
        Console.log('Конец тестового эффекта')

    async def regeneration(UserID: int, time: float = 10):

        while time > 0:
            player = Connect.readPlayer(UserID = UserID)
            player['health'][0] += 10
            Connect.editPlayer(player, UserID)
            await asyncio.sleep(1)
            time -= 1
            

class Effects():
    
    def addEffect(effect):
        effects = asyncio.get_event_loop()
        effects.create_task(effect)