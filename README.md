# primitive-db
Primitive DB
Учебная консольная база данных на Python. Поддерживает управление таблицами, CRUD-операции, хранение в JSON, проверку типов, подтверждение удаления, обработку ошибок, замер времени и кэширование выборок через замыкание. Реализация процедурная, без собственных классов и цветного вывода.

Требования
Python 3.12 или новее;
uv;
Git для клонирования;
make — для использования Makefile (необязательно для прямых команд uv).
Зависимости приложения: prompt и prettytable. Ruff — зависимость для разработки. Разработка возможна в Windows/Git Bash; для записи asciinema используется отдельная среда Ubuntu/WSL.

Установка и запуск
git clone https://github.com/lebedins2-hue/project-2_-Lebedinskii-_-M26-555.git
cd project-2_Lebedinskii_M26_555
uv sync
uv run database

Альтернативные варианты запуска:
uv run project
uv run python -m primitive_db.main

Ручная активация окружения для uv run не требуется. При необходимости в Git Bash с Windows используется Python source .venv\Scripts\Activate.ps1, а в Ubuntu — source .venv/bin/activate

Управление таблицами
Поддерживаемые типы столбцов: int, str, bool.

Столбец ID:int добавляется автоматически и располагается первым. Структура таблиц сохраняется в файле db_meta.json в текущей рабочей директории и доступна после повторного запуска программы.

Доступные команды:

create_table <имя> <столбец:тип> ... - создать таблицу.
list_tables - показать список таблиц.
drop_table <имя> - удалить таблицу.
help - показать справку.
exit - завершить работу.
Пример:

create_table users name:str age:int is_active:bool
list_tables
drop_table users
exit