#!/usr/bin/env python3
"""
Этап 2: Конфигурация эмулятора командной строки
Вариант 7
Поддержка параметров командной строки, YAML-конфига, логирования
"""

import os
import sys
import re
import argparse
import yaml
import json
from datetime import datetime

# ==================== КОНФИГУРАЦИЯ ====================

class Config:
    """Класс для работы с конфигурацией"""
    
    def __init__(self):
        self.vfs_path = None
        self.log_path = None
        self.script_path = None
        self.config_path = None
        self.prompt_format = "user@host:vfs$ "
        
    def load_from_file(self, config_path):
        """Загружает конфигурацию из YAML-файла"""
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                config_data = yaml.safe_load(f)
                
            if config_data:
                self.vfs_path = config_data.get('vfs_path', self.vfs_path)
                self.log_path = config_data.get('log_path', self.log_path)
                self.script_path = config_data.get('script_path', self.script_path)
                self.prompt_format = config_data.get('prompt_format', self.prompt_format)
                
            print(f"[CONFIG] Загружена конфигурация из файла: {config_path}")
            return True
            
        except FileNotFoundError:
            print(f"[ERROR] Конфигурационный файл не найден: {config_path}")
            return False
        except yaml.YAMLError as e:
            print(f"[ERROR] Ошибка чтения YAML-файла: {e}")
            return False
    
    def load_from_args(self, args):
        """Загружает конфигурацию из аргументов командной строки"""
        if args.vfs_path:
            self.vfs_path = args.vfs_path
        if args.log_path:
            self.log_path = args.log_path
        if args.script_path:
            self.script_path = args.script_path
        if args.config_path:
            self.config_path = args.config_path
            
    def print_config(self):
        """Выводит текущую конфигурацию"""
        print("\n=== ТЕКУЩАЯ КОНФИГУРАЦИЯ ===")
        print(f"VFS путь:     {self.vfs_path or 'Не указан'}")
        print(f"Лог файл:     {self.log_path or 'Не указан'}")
        print(f"Скрипт:       {self.script_path or 'Не указан'}")
        print(f"Конфиг файл:  {self.config_path or 'Не указан'}")
        print(f"Формат prompt: {self.prompt_format}")
        print("=" * 30)

# ==================== ЛОГИРОВАНИЕ ====================

class Logger:
    """Класс для логирования в JSON формате"""
    
    def __init__(self, log_path=None):
        self.log_path = log_path
        self.logs = []
        
    def log(self, event_type, command="", args=None, error_msg=""):
        """Записывает событие в лог"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "event_type": event_type,
            "command": command,
            "arguments": args if args else [],
            "error_message": error_msg,
            "user": os.getenv("USER", "unknown")
        }
        
        # Выводим в консоль
        print(f"[LOG] {event_type}: {command} {args if args else ''} {error_msg if error_msg else ''}")
        
        # Сохраняем в памяти
        self.logs.append(log_entry)
        
        # Записываем в файл если указан путь
        if self.log_path:
            try:
                with open(self.log_path, 'a', encoding='utf-8') as f:
                    json.dump(log_entry, f, ensure_ascii=False)
                    f.write('\n')
            except Exception as e:
                print(f"[ERROR] Не удалось записать в лог-файл: {e}")

# ==================== СТАРТОВЫЙ СКРИПТ ====================

def run_startup_script(script_path, emulator):
    """Выполняет стартовый скрипт"""
    if not script_path or not os.path.exists(script_path):
        print(f"[INFO] Стартовый скрипт не найден: {script_path}")
        return
    
    print(f"\n=== ВЫПОЛНЕНИЕ СТАРТОВОГО СКРИПТА: {script_path} ===")
    
    try:
        with open(script_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            
        for line_num, line in enumerate(lines, 1):
            line = line.strip()
            
            # Пропускаем пустые строки и комментарии
            if not line or line.startswith('#'):
                continue
                
            print(f"\n[Скрипт строка {line_num}] {line}")
            print("-" * 40)
            
            # Имитируем выполнение команды
            parts = line.split()
            if parts:
                cmd = parts[0]
                args = parts[1:]
                
                if cmd == "echo":
                    print(' '.join(args))
                elif cmd == "ls":
                    print(f"Список файлов в текущей директории")
                elif cmd == "cd":
                    if args:
                        print(f"Переход в директорию: {args[0]}")
                    else:
                        print("Ошибка: не указана директория")
                else:
                    print(f"Команда '{cmd}' принята")
                    
    except Exception as e:
        print(f"[ERROR] Ошибка выполнения скрипта: {e}")

# ==================== ПАРСЕР АРГУМЕНТОВ ====================

def parse_arguments():
    """Парсит аргументы командной строки"""
    parser = argparse.ArgumentParser(
        description='Эмулятор командной строки UNIX (Вариант 7)',
        epilog='Пример: python emulator.py --vfs-path ./vfs.zip --script startup.txt'
    )
    
    parser.add_argument(
        '--vfs-path',
        help='Путь к виртуальной файловой системе (ZIP)'
    )
    
    parser.add_argument(
        '--log-path',
        help='Путь к лог-файлу (JSON формат)'
    )
    
    parser.add_argument(
        '--script-path',
        help='Путь к стартовому скрипту'
    )
    
    parser.add_argument(
        '--config-path',
        default='config.yaml',
        help='Путь к конфигурационному файлу YAML (по умолчанию: config.yaml)'
    )
    
    parser.add_argument(
        '--dump-config',
        action='store_true',
        help='Вывести конфигурацию и выйти'
    )
    
    return parser.parse_args()

# ==================== ОСНОВНОЙ КЛАСС ЭМУЛЯТОРА ====================

class Emulator:
    """Основной класс эмулятора"""
    
    def __init__(self, config):
        self.config = config
        self.logger = Logger(config.log_path)
        self.running = True
        
    def expand_env_vars(self, text):
        """Раскрывает переменные окружения"""
        return re.sub(r'\$(\w+)', lambda m: os.getenv(m.group(1), ''), text)
    
    def execute_command(self, cmd_line):
        """Выполняет одну команду"""
        cmd_line = self.expand_env_vars(cmd_line)
        parts = cmd_line.split()
        
        if not parts:
            return
            
        cmd = parts[0]
        args = parts[1:]
        
        # Логируем вызов команды
        self.logger.log("COMMAND", cmd, args)
        
        if cmd == "exit":
            print("Выход из эмулятора.")
            self.running = False
            
        elif cmd == "ls":
            print(f"Команда 'ls': аргументы = {args}")
            print("(Заглушка: список файлов)")
            
        elif cmd == "cd":
            print(f"Команда 'cd': аргументы = {args}")
            if args:
                print(f"(Переход в: {args[0]})")
            else:
                print("(Ошибка: не указан путь)")
                self.logger.log("ERROR", cmd, args, "Не указан путь для cd")
                
        elif cmd == "conf-dump":
            print("\n=== ТЕКУЩАЯ КОНФИГУРАЦИЯ (conf-dump) ===")
            for key, value in vars(self.config).items():
                print(f"{key}: {value}")
                
        elif cmd == "log-test":
            print("Тестирование логирования...")
            self.logger.log("TEST", "log-test", ["arg1", "arg2"])
            self.logger.log("ERROR", "fake-cmd", [], "Тестовая ошибка")
            print("Логи записаны")
            
        elif cmd == "help":
            print("\n=== ДОСТУПНЫЕ КОМАНДЫ ===")
            print("  ls                   - список файлов")
            print("  cd <dir>             - сменить директорию")
            print("  conf-dump            - вывести конфигурацию")
            print("  log-test             - протестировать логирование")
            print("  exit                 - выйти из эмулятора")
            print("  help                 - эта справка")
            
        else:
            print(f"Ошибка: неизвестная команда '{cmd}'")
            self.logger.log("ERROR", cmd, args, "Неизвестная команда")
    
    def run_interactive(self):
        """Запускает интерактивный режим"""
        print("\n" + "=" * 50)
        print("ЭМУЛЯТОР КОМАНДНОЙ СТРОКИ UNIX")
        print("Вариант 7 - Этап 2: Конфигурация")
        print("=" * 50)
        
        vfs_name = "myvfs"
        hostname = "localhost"
        user = os.getenv("USER", "student")
        
        while self.running:
            prompt = self.config.prompt_format.replace("user", user) \
                                              .replace("host", hostname) \
                                              .replace("vfs", vfs_name)
            
            try:
                cmd_line = input(prompt).strip()
                if not cmd_line:
                    continue
                    
                self.execute_command(cmd_line)
                
            except KeyboardInterrupt:
                print("\n\nПрервано пользователем.")
                break
            except Exception as e:
                print(f"\nКритическая ошибка: {e}")
                self.logger.log("FATAL", "", [], str(e))
                break

# ==================== ГЛАВНАЯ ФУНКЦИЯ ====================

def main():
    """Главная функция"""
    print("=" * 60)
    print("ЭМУЛЯТОР КОМАНДНОЙ СТРОКИ - ЭТАП 2: КОНФИГУРАЦИЯ")
    print("=" * 60)
    
    # 1. Парсим аргументы командной строки
    args = parse_arguments()
    print("\n=== АРГУМЕНТЫ КОМАНДНОЙ СТРОКИ ===")
    for arg_name, arg_value in vars(args).items():
        print(f"{arg_name}: {arg_value}")
    
    # 2. Загружаем конфигурацию
    config = Config()
    
    # Сначала из файла (если указан)
    if args.config_path:
        config.load_from_file(args.config_path)
    
    # Затем из командной строки (имеет приоритет)
    config.load_from_args(args)
    
    # 3. Выводим итоговую конфигурацию
    config.print_config()
    
    # 4. Если запрошен только вывод конфигурации - выходим
    if args.dump_config:
        print("\nРежим dump-config: выход")
        return
    
    # 5. Создаем эмулятор
    emulator = Emulator(config)
    
    # 6. Запускаем стартовый скрипт (если есть)
    if config.script_path:
        run_startup_script(config.script_path, emulator)
    
    # 7. Запускаем интерактивный режим
    emulator.run_interactive()
    
    # 8. Завершение
    print("\n" + "=" * 50)
    print("Эмулятор завершил работу")
    print(f"Логи сохранены: {config.log_path or 'в памяти'}")
    print("=" * 50)

# ==================== ТОЧКА ВХОДА ====================

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nПрограмма прервана пользователем")
    except Exception as e:
        print(f"\nНепредвиденная ошибка: {e}")
        sys.exit(1)
