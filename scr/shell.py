import os
import shlex
from src.parser import Parser
from src.commands import Commands

class Shell:
    def __init__(self):
        self.vfs_name = "default_vfs"  # пока что фиктивное имя
        self.parser = Parser()
        self.commands = Commands()
        self.running = True
        
    def get_prompt(self):
        # Приглашение должно содержать имя VFS, как в варианте №7
        return f"[{self.vfs_name}] $ "
    
    def run(self):
        print("Добро пожаловать в эмулятор командной строки!")
        print(f"VFS: {self.vfs_name}")
        print("Введите 'exit' для выхода.")
        print("-" * 40)
        
        while self.running:
            try:
                user_input = input(self.get_prompt()).strip()
                if not user_input:
                    continue
                
                # Разбираем команду
                cmd, args = self.parser.parse(user_input)
                
                # Проверяем, есть ли такая команда
                if cmd == "exit":
                    self.running = False
                    print("Выход из эмулятора.")
                elif hasattr(self.commands, cmd):
                    # Вызываем команду
                    func = getattr(self.commands, cmd)
                    func(*args)
                else:
                    print(f"Ошибка: неизвестная команда '{cmd}'")
                    
            except KeyboardInterrupt:
                print("\nВыход по Ctrl+C")
                self.running = False
            except Exception as e:
                print(f"Ошибка выполнения: {e}")
