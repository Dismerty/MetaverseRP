"""
* PluginLoader - библиотека для работы с плагинами
"""
import os, importlib, inspect
from libs import Console, ChatLogger
from functools import wraps
from dispatcher import dp

Console.log("Инициализация плагинов.", "Plugins")
plugins = os.listdir('plugins')

for plugin in plugins:
    if plugin != "__init__.py" and ".py" in plugin[-3:]:
        try:
            globals()[f"{plugin[:-3]}"] = importlib.import_module(f"plugins.{plugin[:-3]}")
            globals()[f"{plugin[:-3]}"].Plugin.OnLoad()
            for name, obj in inspect.getmembers(globals()[f"{plugin[:-3]}"]):
                if inspect.isfunction(obj) and hasattr(obj, '__wrapped__'):
                    obj()
        except Exception as e:
            Console.error(f"Не удалось загрузить плагин \"{plugin}\".\nПроизошла ошибка: {e}")
