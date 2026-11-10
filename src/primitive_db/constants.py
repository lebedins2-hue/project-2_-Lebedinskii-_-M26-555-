META_FILE = "db_meta.json"
VALID_TYPES = ("int", "str", "bool")
ID_COLUMN = "ID"
ID_TYPE = "int"
DATA_DIR = "data"
TYPE_CLASSES = {
    "int": int,
    "str": str,
    "bool": bool
}
TABLE_MISSING_MESSAGE = 'Ошибка: Таблица "{table_name}" не существует.'
INVALID_VALUE_MESSAGE = "Некорректное значение: {value}. Попробуйте снова."