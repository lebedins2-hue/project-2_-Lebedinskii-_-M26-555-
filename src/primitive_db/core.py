#Основная логика работы с таблицами и данными
from primitive_db.constants import (
        ID_COLUMN, 
        ID_TYPE,
        VALID_TYPES,
        TABLE_MISSING_MESSAGE,
        INVALID_VALUE_MESSAGE,
        TYPE_CLASSES)


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

def invalid(value):
    '''Сообщение о значении, не в соответствии со схемой'''
    raise ValueError(INVALID_VALUE_MESSAGE.format(value=value))

def validate_columns(columns):
    '''Проверить определения столбцов и поставить единственный ID первым'''
    if not columns:
        invalid("не указаны столбцы")
    result = [ID_COLUMN]
    seen = set()
    for column in columns:
        name, separator, column_type = column.partition(":")
        if (
            not separator
            or not name.isidentifier()
            or column_type not in VALID_TYPES
            or name in seen
        ):
            invalid(column)
        seen.add(name)
        if name == ID_COLUMN_NAME:
            if column != ID_COLUMN:
                invalid(column)
        else:
            result.append(column)
    return result


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
   column_names = []
   seen_names = set() 
   column_names.append(ID_COLUMN)

   for column in columns:
        parts = column.split(":",1)

        if len(parts) != 2 or not parts[0] or parts[1] not in VALID_TYPES:
            print(f"Неверный формат колонки '{column}': ожидается 'name:type'.")
            return None

        column_name, column_type = parts
        column_name = column_name.strip()
        column_type = column_type.strip()

        if not column_name:
            print(f"Ошибка: пустое имя колонки в '{column}'.")
            return None
               
        if not validate_name(column_name):
            print(f'Ошибка: Некорректное имя столбца "{column_name}"')
            return metadata
        
        
        if column_type not in VALID_TYPES:
            raise ValueError("не верный тип данных: ", column)

        if column_name in seen_names:
            raise ValueError("такое имя уже есть: ", column)

        seen_names.add(column_name)

        if column_name == ID_COLUMN:
            if column_type != ID_TYPE:
                raise ValueError(f"Ошибка: для колонки {ID_COLUMN} разрешён только тип {ID_TYPE}.")
                return None
            continue

        base[column_name] = column_type
        column_names.append(column_name)

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
    if not metadata or len(metadata) == 0:
        print("Таблиц нет")
        return 
    for table_name in metadata:
        print(f"{table_name}")

def validate_fields(schema, fields):
    '''Проверяет существование столбцов и типы переданных значений.'''
    for column_name, value in fields.items():
        if column_name not in schema:
            raise ValueError(f"Столбец `{column_name}` не существует")

        expected_type = TYPE_CLASSES[schema[column_name]]

        if type(value) is not expected_type:
            raise ValueError(
                f"Столбец `{column_name}` "
                f"требует тип {schema[column_name]}"
            )

def insert(metadata, table_name, table_data, values):
    '''Возвращает список записей с новой записью и автоматически созданным ID'''
    schema = get_schema(metadata, table_name)
    columns = [n for n in schema if n != ID_COLUMN]

    if len(values) != len(columns):
        raise ValueError(
            f"Ожидается значений: {len(columns)}, получено: {len(values)}"
        )

    record = dict(zip(columns, values))
    validate_fields(schema, record)

    new_id = max(
        (record[ID_COLUMN] for record in table_data),
        default=0,
    ) + 1

    new_record = {ID_COLUMN: new_id, **record}
    return [*table_data, new_record]

def get_schema(metadata, table_name):
    '''Проверить существование таблицы и вернуть соответствие имён типам'''
    if table_name not in metadata:
        raise ValueError(TABLE_MISSING_MESSAGE.format(table_name=table_name))
    columns = metadata[table_name]
    if validate_columns(columns) != columns:
        invalid("повреждённая схема таблицы")
    return dict(column.split(":") for column in columns)

