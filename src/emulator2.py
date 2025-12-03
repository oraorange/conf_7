
"""
Эмулятор командной строки (Вариант 7).
Этапы 1 и 2.
"""

import sys
import os
import shlex
import argparse # <-- Новый модуль для разбора аргументов командной строки
import json     # <-- Для логирования в JSON

class Emulator:
    """Класс, представляющий эмулятор командной строки."""

    def __init__(self, vfs_path=None, log_path=None, script_path=None, config_path=None):
        """
        Инициализация эмулятора с параметрами конфигурации.
        :param vfs_path: Путь к виртуальной файловой системе (пока не используется)
        :param log_path: Путь к файлу для логирования
        :param script_path: Путь к стартовому скрипту
        :param config_path: Путь к конфигурационному файлу YAML (пока не используется)
        """
        self.vfs_path = vfs_path
        self.log_path = log_path
        self.script_path = script_path
        self.config_path = config_path
        self.current_dir = "/"  # Текущая "директория" в VFS (пока имитация)

        # 6. Настройка логирования в JSON
        self.log_file = None
        if self.log_path:
            try:
                self.log_file = open(self.log_path, 'a', encoding='utf-8')
            except IOError as e:
                print(f"Ошибка открытия лог-файла {self.log_path}: {e}", file=sys.stderr)

        # Отладочный вывод всех заданных параметров (требование этапа)
        print("=== Параметры запуска эмулятора ===", file=sys.stderr)
        print(f"  VFS путь: {self.vfs_path}", file=sys.stderr)
        print(f"  Лог-файл: {self.log_path}", file=sys.stderr)
        print(f"  Скрипт:   {self.script_path}", file=sys.stderr)
        print(f"  Конфиг:   {self.config_path}", file=sys.stderr)
        print("===================================", file=sys.stderr)

    def log_command(self, command, args, error_message=None):
        """Логирование события вызова команды в формате JSON."""
        if not self.log_file:
            return
        log_entry = {
            "command": command,
            "args": args,
            "error": error_message
        }
        json.dump(log_entry, self.log_file, ensure_ascii=False)
        self.log_file.write('\n')
        self.log_file.flush()  # Сразу записываем на диск

    def execute_command(self, command, args, from_script=False):
        """Выполняет одну команду с аргументами."""
        # Логируем вызов команды (перед выполнением)
        self.log_command(command, args)

        if command == "exit":
            if not from_script:
                print("Выход из эмулятора.")
            return False  # Сигнал к выходу из цикла
        elif command == "ls":
            print(f"Команда: ls, Аргументы: {args}, Текущий каталог VFS: {self.current_dir}")
        elif command == "cd":
            if args:
                new_dir = args[0]
                print(f"Команда: cd, Переход в: {new_dir}")
                # Здесь будет сложная логика смены каталога в VFS
                self.current_dir = new_dir
            else:
                print("Ошибка: для команды 'cd' требуется аргумент (путь).")
                self.log_command(command, args, "Не указан аргумент пути")
        else:
            print(f"Ошибка: неизвестная команда '{command}'")
            self.log_command(command, args, "Неизвестная команда")
        return True  # Продолжаем работу

    def run_script(self, script_path):
        """Выполняет команды из стартового скрипта."""
        print(f"[Выполнение скрипта: {script_path}]")
        try:
            with open(script_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
        except IOError as e:
            # 8. Сообщить об ошибке чтения скрипта
            print(f"Ошибка чтения скрипта {script_path}: {e}", file=sys.stderr)
            return

        for line_num, line in enumerate(lines, start=1):
            line = line.strip()
            if not line or line.startswith('#'):  # Пропускаем пустые строки и комментарии (используем #)
                continue

            # 7. При выполнении скрипта отображаем и ввод, и вывод.
            print(f"vfs> {line}")  # Имитируем ввод пользователя

            # Разбираем и выполняем команду из скрипта
            expanded_line = os.path.expandvars(line)
            try:
                parts = shlex.split(expanded_line)
            except ValueError as e:
                print(f"  Ошибка разбора строки {line_num}: {e}")
                # 7. Ошибочные строки пропускаем (требование варианта)
                continue

            if not parts:
                continue

            command = parts[0]
            args = parts[1:]

            # Выполняем команду. Если команда вернула False (exit), прерываем выполнение скрипта.
            if not self.execute_command(command, args, from_script=True):
                print("  [Скрипт прерван командой 'exit']")
                break

        print(f"[Скрипт {script_path} выполнен]")

    def run_interactive(self):
        """Запускает интерактивный режим (REPL)."""
        print("Эмулятор командной строки (Вариант 7). Для выхода введите 'exit'.")
        while True:
            # Приглашение с именем VFS (берем из пути или имя файла)
            vfs_name = os.path.basename(self.vfs_path) if self.vfs_path else "noname"
            prompt = f"vfs:{vfs_name}> "
            try:
                user_input = input(prompt).strip()
            except EOFError:
                print()
                break
            except KeyboardInterrupt:
                print()
                continue

            if not user_input:
                continue

            expanded_input = os.path.expandvars(user_input)
            try:
                parts = shlex.split(expanded_input)
            except ValueError as e:
                print(f"Ошибка разбора команды: {e}")
                continue

            if not parts:
                continue

            command = parts[0]
            args = parts[1:]

            if not self.execute_command(command, args, from_script=False):
                break

    def cleanup(self):
        """Корректно закрывает ресурсы (например, лог-файл)."""
        if self.log_file:
            self.log_file.close()

def main():
    """Главная функция, разбирает аргументы и запускает эмулятор."""

    # 1. Парсим параметры командной строки с помощью argparse
    parser = argparse.ArgumentParser(description='Эмулятор командной строки (Вариант 7)')
    parser.add_argument('--vfs',  help='Путь к физическому расположению VFS')
    parser.add_argument('--log',  help='Путь к лог-файлу')
    parser.add_argument('--script', help='Путь к стартовому скрипту')
    parser.add_argument('--config', help='Путь к конфигурационному файлу YAML')
    # Можно добавить короткие версии аргументов, например: -v, -l, -s

    args = parser.parse_args()

    # 2 & 3. Конфигурационный файл YAML пока НЕ реализуем для простоты.
    # В полной версии здесь нужно было бы считать конфиг из YAML и объединить с аргументами.
    # 4. Приоритет: командная строка > конфиг-файл (пока не актуально).
    # 5. Сообщение об ошибке чтения конфиг-файла тоже пока пропускаем.

    # Создаем экземпляр эмулятора с переданными параметрами
    emulator = Emulator(
        vfs_path=args.vfs,
        log_path=args.log,
        script_path=args.script,
        config_path=args.config
    )

    # 7. Если указан скрипт - выполняем его
    if emulator.script_path:
        emulator.run_script(emulator.script_path)
        # После скрипта можно либо завершить работу, либо перейти в интерактивный режим.
        # По умолчанию завершаем, как в большинстве консольных утилит.
        print("Скрипт выполнен. Завершение работы.")
    else:
        # Если скрипта нет - запускаем интерактивный режим
        emulator.run_interactive()

    # Корректно завершаем работу
    emulator.cleanup()

if __name__ == "__main__":
    main()
