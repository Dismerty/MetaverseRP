from aiogram import types

class ChatScanner:
    PowersList = ['лёд', 'огненный шар', 'огненного шара', 'огненному шару', 'огненным шаром', 'огненном шаре']

    def __init__(self, TelegramMessage: types.Message) -> None:

        self.EditedMessage: str = TelegramMessage.text # Отредактированное сообщение
        self.ActionsText: list = [] # Действие с текстом
        self.JustActions: list = [] # Только действие в квадратных скобках
        self.Actions: list = [] # Все действия

        '''
        Данный код ищет квадратные скобки, достаёт из них текстовое значение и перебирает ключевые слова команд.
        После, заносит команды в переменную ActionsText, где хранится команда и цифра из квадратных скобок.
        '''
        line = 0 # Сброс
        while TelegramMessage.text.find('[', line) != -1:
            line = TelegramMessage.text.find('[', line)
            end = TelegramMessage.text.find(']', line)

            for p in ChatScanner.PowersList:
                if TelegramMessage.text.casefold()[line - len(p):line] == p and TelegramMessage.text[line + 1:end].isdigit():
                    self.ActionsText.append([int(TelegramMessage.text[line + 1:end]), TelegramMessage.text[line - len(p):line]])
            
            line += end - line
            
        for d in self.ActionsText:
            self.EditedMessage = self.EditedMessage.replace(f'{d[1]}[{d[0]}]', f'{d[1]}', 1)
            d[1] = d[1].lower()

        '''
        Данный код по символам исчет квадратные скобки и достаёт из них значение.
        После, заносит команды в переменную JustActions.
        '''
        line = 0 # Сброс
        __boolen = False; __data = ''
        for __sumbol in  self.EditedMessage:
  
            if __sumbol.find('[') == 0 or __boolen:
                __data += __sumbol
                __boolen = True

                if __sumbol.find(']') == 0:
                    self.JustActions.append(__data[1:-1])
                    __boolen = False; __data = ''

        '''
        Тут идёт объединение команд из переменной JustActions и ActionsText в общую переменную Actions.
        P.S.: Первые значения в переменной Actions будут относится к ActionText, а остальные к JustAction.
        '''
        for d in self.JustActions:
            self.EditedMessage = self.EditedMessage.replace(f'[{d}]', '', 1)

        for d in self.ActionsText:
            self.Actions.append({d[0]: d[1]})
        
        for d in self.JustActions:
            self.Actions.append(d)

        self.EditedMessage = self.EditedMessage.replace('  ', ' ', 1)