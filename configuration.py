# Библиотеки Python
import os, yaml

# Родные библиотеки
from libs import Console

if os.path.exists('config.yml'):
    Console.log('Чтение конфигурации.')
else:
    Console.error('Не удалось прочитать файл конфигураций!')
    exit()

with open('config.yml', 'r') as file:
    config = yaml.safe_load(file)
Console.log('Конфигурация успешно загружена!')

class Config:
    def read(path):
        with open(path, 'r') as file:
            return yaml.safe_load(file)