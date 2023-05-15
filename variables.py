from math import inf

variables = {
    "player": {
        "name": "{name}", # Имя
        "health": [100, 100], # Здоровье
        "satiety": [100, 100], # Сытость
        "realName": "{name}", # Реальное имя
        "gender": "{gender}", # Пол
        "age": "{age}", # Возраст
        "species": "{species}", # Раса
        "appearance": "{appearance}", # Внешность персонажа
        "character": "{character}", # Характер
        "diet": "{diet}", # Рацион питания
        "story": "{story}", # Краткая история
        "capabilities": {}, # Способности
        "level": 1, # Уровень
        "experience": 0, # Число опыта
        "inventory": # Инвентарь и слоты
        {
            "slots":
            {
                1:  None, 2:  None, 3:  None, 4:  None, 5:  None, 6:  None, 7:  None, 8:  None, 9:  None,
                10: None, 11: None, 12: None, 13: None, 14: None, 15: None, 16: None, 17: None, 18: None,
                19: None, 20: None, 21: None, 22: None, 23: None, 24: None, 25: None, 26: None, 27: None,
                28: None, 29: None, 30: None, 31: None, 32: None, 33: None, 34: None, 35: None, 36: None
            },
            "armor":
            {
                "helmet":     None,
                "chestplate": None,
                "glove":
                {
                    "left":  None,
                    "right": None
                },
                "paints": None,
                "boot":
                {
                    "left":  None,
                    "right": None
                },
                "accessories":
                {
                    "hand":
                    {
                        "left":  None,
                        "right": None
                    },
                    "neck": None
                }
            }
        }
    },
    "species":
    [
        "Люди",
        "Гномы",
        "Протарианцы",
        "Лингвинги",
        "Ноэрцы",
        "Каджит",
        "Берендей",
        "Сильфы",
        "Сильфы Света",
        "Сильфы Тьмы",
        "Драконо-Рождённые" 
    ]
}

def get(key): return variables[key]