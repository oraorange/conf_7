import os
import getpass
import socket

class ShellEmulator:
    def __init__(self):
        self.running = True
        self.vfs_name = "default"  # пока заглушка
        
    def get_prompt(self):
        username = getpass.getuser()
        hostname = socket.gethostname()
        return f"{username}@{hostname}:{self.vfs_name}$ "
    
    def parse_command(self, input_line):
        # Поддержка раскрытия переменных окружения
        import re
        # Заменяем $HOME, $USER и т.д. на реальные значения
        input_line = re.sub(r'\$HOME', os.path.expanduser('~'), input_line)
        input_line = re.sub(r'\$USER', getpass.getuser(), input_line)
        
        parts = input_line.strip().split()
        if not parts:
            return None, []
        return parts[0], parts[1:]
    
    def handle_ls(self, args):
        print(f"ls called with args: {args}")
        # Заглушка - просто выводим имя и аргументы
        
    def handle_cd(self, args):
        print(f"cd called with args: {args}")
        # Заглушка
        
    def handle_exit(self, args):
        self.running = False
        print("Goodbye!")
    
    def run(self):
        print("Shell Emulator started. Type 'exit' to quit.")
        
        while self.running:
            try:
                user_input = input(self.get_prompt())
                command, args = self.parse_command(user_input)
                
                if not command:
                    continue
                    
                # Обработка команд
                if command == "ls":
                    self.handle_ls(args)
                elif command == "cd":
                    self.handle_cd(args)
                elif command == "exit":
                    self.handle_exit(args)
                else:
                    print(f"Error: unknown command '{command}'")
                    
            except KeyboardInterrupt:
                print("\nUse 'exit' to quit")
            except Exception as e:
                print(f"Error: {e}")

if __name__ == "__main__":
    shell = ShellEmulator()
    shell.run()
