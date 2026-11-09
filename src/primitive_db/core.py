#Основная логика работы с таблицами и данными
from primitive_db.constants import ID_COLUMN, ID_TYPE, VALID_TYPES


def validate_name(table_name):
    '''Проверка корректности имени таблицы и столбца'''
    if not table_name:
        return False

    first_ch = table_name[0]

    if not ("A" <= first_ch <= "Z" or "a" <= first_ch <= "z" or first_ch == "_"):
        return False

    for char in table_name[1:]:
        if not (
            "A" <= char <= "Z"
            or "a" <= char <= "z"
            or "0" <= char <= "9"
            or char == "_"
        ):
            return False

    return True

def create_table(metadata, table_name, columns):
   '''Создаёт и проверяет таблицу и добавляет столбец ID.'''

   if not validate_name(table_name):
        print(
            "Ошибка: не верное предстваление имени таблицы."
        )
        return metadata
   if table_name in metadata:
        print(f"Ошибка: Таблица `{table_name}` уже существует")
        return metadata
   
   if not columns:
        raise ValueError("Не указаны имена столбцов")

   base = {ID_COLUMN: ID_TYPE}
   column_names = set()

   for column in columns:
        parts = column.split(":",1)

        if len(parts) != 2:
            print(f"Неверный формат колонки '{column}': ожидается 'name:type'.")
            return metadata

        column_name, column_type = parts
        column_name = column_name.strip()
        column_type = column_type.strip()
               
        if not validate_name(column_name):
            print(f'Ошибка: Некорректное имя столбца "{column_name}"')
            return metadata
        
        
        if column_type not in VALID_TYPES:
            raise ValueError("не верный тип данных: ", column)

        if column_name in column_names:
            raise ValueError("такое имя уже есть: ", column)

        column_names.add(column_name)

        if column_name == ID_COLUMN:
            if column_type != ID_TYPE:
                raise ValueError("не верный тип данных: ", column)
            continue

        base[column_name] = column_type

   metadata[table_name] = base
   print(
        f'Таблица "{table_name}" успешно создана со столбцами: '
        f"{', '.join(column_names)}"
        )
   return metadata    


def drop_table(metadata, table_name):
    '''Удаляет таблицу и возвращает обновляет metadata'''
    if table_name not in metadata:
        print(f"Ошибка: Таблица `{table_name}` не существует")
        return None

    del metadata[table_name]
    return metadata


def list_tables(metadata):
    """Выводит имена существующих таблиц."""
    if not metadata:
        print("Таблиц нет")
        return 
    for table_name in metadata:
        print(f"{table_name}")