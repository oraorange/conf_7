import os
import sys
import getpass
import socket


class ShellEmulator:
    """Основной класс эмулятора командной строки."""
    
    def __init__(self):
        self.username = getpass.getuser()
        self.hostname = socket.gethostname()
        self.vfs_name = "default_vfs"  # Имя VFS по умолчанию
        self.running = True
        
    def get_prompt(self) -> str:
        """Возвращает строку приглашения."""
        return f"{self.username}@{self.hostname}:{self.vfs_name}$ "
    
    def expand_vars(self, text: str) -> str:
        """Раскрывает переменные окружения."""
        return os.path.expandvars(text)
    
    def parse_input(self, user_input: str):
        """Парсит ввод пользователя."""
        if not user_input.strip():
            return None, []
        
        expanded = self.expand_vars(user_input)
        parts = expanded.strip().split()
        return parts[0], parts[1:]
    
    def handle_command(self, command: str, args: list):
        """Обрабатывает команду."""
        if command == "exit":
            print("Завершение работы эмулятора.")
            self.running = False
            
        elif command == "ls":
            print(f"[ls] аргументы: {args}")
            
        elif command == "cd":
            print(f"[cd] аргументы: {args}")
            
        else:
            print(f"Ошибка: неизвестная команда '{command}'")
            print("Доступные команды: ls, cd, exit")
    
    def run(self):
        """Основной цикл REPL."""
        print("=" * 50)
        print(f"Эмулятор командной строки (Вариант 7)")
        print(f"Пользователь: {self.username}@{self.hostname}")
        print(f"VFS: {self.vfs_name}")
        print("=" * 50)
        print("Введите команды. Для выхода введите 'exit'.")
        print("Поддерживаются переменные окружения: $HOME, $USER, $PATH")
        print("-" * 50)
        
        while self.running:
            try:
                # Получаем ввод
                user_input = input(self.get_prompt())
                
                # Парсим
                command, args = self.parse_input(user_input)
                
                if command is None:
                    continue
                
                # Обрабатываем команду
                self.handle_command(command, args)
                
            except KeyboardInterrupt:
                print("\n\nПрервано пользователем (Ctrl+C).")
                break
            except EOFError:
                print("\n\nЗавершение ввода.")
                break
            except Exception as e:
                print(f"\nКритическая ошибка: {e}")
                break


def main():
    """Точка входа в программу."""
    emulator = ShellEmulator()
    emulator.run()


if __name__ == "__main__":
    main()
