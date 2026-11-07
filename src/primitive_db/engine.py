import prompt


def welcome():
    """Выводит приветствие и цикл с вводом команд."""
    print("<command> exit - выйти из программы")
    print("<command> help - справочная информация")

    while True:
        # Аналог prompt.string('Введите команду: ')
        command = prompt.string("Введите команду: ").strip().lower()

        if command == "exit":
            print("Выход из программы.")
            break

        elif command == "help":
            print("<command> exit - выйти из программы")
            print("<command> help - справочная информация")

        else:
            if command:  # игнорируем пустые строки
                print(f"Неизвестная команда: '{command}'. Введите 'help' для справки.")
