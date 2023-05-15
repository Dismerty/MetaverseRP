from libs import Console, ChatLogger
from dispatcher import dp
from functools import wraps

def RegisterGameCommand(*custom_filters, commands = None, regexp = None, content_types = None,
                        run_task = None, **kwargs):
    def wrapper(callback):
        @wraps(callback)
        def subwrapper():
            Console.debug(f"Загружена игровая команда плагина {callback}", "Plugins")
            dp.register_message_handler(callback, *custom_filters,
                                          commands = commands,
                                          regexp = regexp,
                                          content_types = content_types,
                                          state = ChatLogger.GameChatState,
                                          run_task = run_task,
                                          **kwargs)
        return subwrapper
    return wrapper

def RegisterCommand(*custom_filters, commands = None, regexp = None, content_types = None,
                        state = None, run_task = None, **kwargs):
    def wrapper(callback):
        @wraps(callback)
        def subwrapper():
            Console.debug(f"Загружена команда плагина {callback}", "Plugins")
            dp.register_message_handler(callback, *custom_filters,
                                          commands = commands,
                                          regexp = regexp,
                                          content_types = content_types,
                                          state = state,
                                          run_task = run_task,
                                          **kwargs)
        return subwrapper
    return wrapper