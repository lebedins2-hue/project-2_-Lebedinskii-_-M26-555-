#Вспомогательные функции
import json
import os

from primitive_db.constants import DATA_DIR


def load_metadata(filepath):
    '''Загружает метаданные из JSON или возвращает пустой словарь.'''
    try:
        with open(filepath, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

def save_metadata(filepath, data):
    '''Сохраняет переданные данные в JSON словарь'''
    with open(filepath, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii = False, indent = 4)

def load_table_data(table_name):
    '''Загружает записи таблицы'''
    filepath = os.path.join(DATA_DIR, f"{table_name}.json")

    try:
        with open(filepath, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        return []

def save_table_data(table_name, data):
    '''Создаёт директорию и сохраняет записи таблицы'''

    os.makedirs(DATA_DIR, exist_ok=True)
    filepath = os.path.join(DATA_DIR, f"{table_name}.json")

    with open(filepath, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)