import json
import shlex
import prompt

from primitive_db.constants import ID_COLUMN, META_FILE
from primitive_db.core import (
    create_table,
    drop_table  )
from primitive_db.utils import (
    load_metadata,
    save_metadata,
    )

def print_help():
    """Prints the help message for the current mode."""
   
    print("\n***Процесс работы с таблицей***")
    print("Функции:")
    print("<command> create_table <имя_таблицы> <столбец1:тип> .. - создать таблицу")
    print("<command> list_tables - показать список всех таблиц")
    print("<command> drop_table <имя_таблицы> - удалить таблицу")
    
    print("\nОбщие команды:")
    print("<command> exit - выход из программы")
    print("<command> help - справочная информация\n") 

def run():
    """Выводит приветствие и цикл с вводом команд."""
    print_help()
    while True:
        # Аналог prompt.string('Введите команду: ')
        metadata = load_metadata(META_FILE)
        user_input = prompt.string("Введите команду: ").strip().lower()

        try:
            args = shlex.split(user_input)
        except ValueError:
            print(f"Некорректное значение: {user_input}. Попробуйте снова.")
            continue

        if not args:
            continue

        command = args[0]
        arguments = args[1:]

        if command == "exit":
            print("Выход из программы.")
            break

        elif command == "help":
            if arguments:
                raise ValueError(f"Команда 'help' не принимает аргументов. Передано: {' '.join(arguments)}")
            print_help()

        elif command == "create_table":
            if len(args) < 3:
                print(
                    "Некорректное значение: недостаточно аргументов. Попробуйте снова."
                    )
                continue       
            table_name = args[1]
            columns = args[2:]

            result = create_table(metadata, table_name, columns)

            if result is not None:
               metadata = result
               save_metadata(META_FILE, metadata)
               print(f"Таблица '{table_name}' создана и сохранена.")


        elif command == "drop_table":
            if len(args) != 2:
                print("Некорректное значение: аргументы команды. Попробуйте снова.")
                continue

            table_name = args[1]
            result = drop_table(metadata, table_name)

            if result is not None:
                # Только если удаление прошло успешно, обновляем и сохраняем
                metadata = result
                save_metadata(META_FILE, metadata)
                print(f'Таблица "{table_name}" успешно удалена.')
            else:
                print(f'Ошибка: Таблица "{table_name}" не существует.')

        else:
            print(f"Функции {command} нет. Попробуйте снова.")
