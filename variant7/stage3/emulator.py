#!/usr/bin/env python3
"""
Этап 3: Виртуальная файловая система (VFS)
Вариант 7
Поддержка ZIP-архивов как источника VFS, Base64 для двоичных данных
"""

import os
import sys
import re
import argparse
import yaml
import json
import zipfile
import base64
import hashlib
from datetime import datetime
from io import BytesIO

# ==================== VFS (ВИРТУАЛЬНАЯ ФС) ====================

class VFSNode:
    """Узел виртуальной файловой системы"""
    
    def __init__(self, name, node_type="file"):
        self.name = name
        self.type = node_type  # "file" или "directory"
        self.content = b"" if node_type == "file" else None
        self.children = {} if node_type == "directory" else None
        self.permissions = "644" if node_type == "file" else "755"
        self.owner = "user"
        self.group = "group"
        
    def add_child(self, node):
        """Добавляет дочерний узел (для директорий)"""
        if self.type != "directory":
            raise ValueError("Можно добавлять только в директорию")
        self.children[node.name] = node
        
    def get_path(self, path):
        """Возвращает узел по пути"""
        if path == "" or path == ".":
            return self
            
        parts = path.strip("/").split("/")
        if not parts[0]:
            parts = parts[1:]
            
        current = self
        for part in parts:
            if current.type != "directory":
                return None
            if part not in current.children:
                return None
            current = current.children[part]
            
        return current
        
    def list_dir(self, path=""):
        """Список содержимого директории"""
        node = self.get_path(path)
        if not node or node.type != "directory":
            return None
            
        return list(node.children.keys())

class VFS:
    """Виртуальная файловая система"""
    
    def __init__(self):
        self.root = VFSNode("/", "directory")
        self.current_path = "/"
        self.name = "unnamed"
        self.source_hash = ""
        
    def load_from_zip(self, zip_path):
        """Загружает VFS из ZIP архива"""
        try:
            if not os.path.exists(zip_path):
                raise FileNotFoundError(f"ZIP файл не найден: {zip_path}")
                
            with zipfile.ZipFile(zip_path, 'r') as zipf:
                # Читаем motd если есть
                motd_content = ""
                if "motd" in zipf.namelist():
                    with zipf.open("motd") as f:
                        motd_content = f.read().decode('utf-8', errors='ignore')
                        print(f"[VFS] Прочитан motd: {motd_content[:50]}...")
                
                # Строим дерево файлов
                for file_info in zipf.infolist():
                    if file_info.filename.endswith('/'):
                        continue  # Пропускаем директории
                        
                    # Создаем путь в VFS
                    parts = file_info.filename.split('/')
                    current_dir = self.root
                    
                    # Создаем промежуточные директории
                    for part in parts[:-1]:
                        if part and part not in current_dir.children:
                            dir_node = VFSNode(part, "directory")
                            current_dir.add_child(dir_node)
                        if part:
                            current_dir = current_dir.children[part]
                    
                    # Создаем файл
                    with zipf.open(file_info.filename) as f:
                        content = f.read()
                        file_node = VFSNode(parts[-1], "file")
                        file_node.content = base64.b64encode(content).decode('ascii')
                        current_dir.add_child(file_node)
                
                # Вычисляем хеш
                with open(zip_path, 'rb') as f:
                    self.source_hash = hashlib.sha256(f.read()).hexdigest()
                    
                self.name = os.path.basename(zip_path)
                print(f"[VFS] Загружена VFS из {zip_path}")
                print(f"[VFS] Хеш SHA-256: {self.source_hash[:16]}...")
                
                return motd_content
                
        except zipfile.BadZipFile:
            raise ValueError(f"Некорректный ZIP архив: {zip_path}")
        except Exception as e:
            raise RuntimeError(f"Ошибка загрузки VFS: {e}")
    
    def load_from_json(self, json_path):
        """Загружает VFS из JSON файла"""
        try:
            with open(json_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
            def build_node(node_data, parent):
                if node_data['type'] == 'directory':
                    node = VFSNode(node_data['name'], 'directory')
                    for child in node_data.get('children', []):
                        child_node = build_node(child, node)
                        node.add_child(child_node)
                else:
                    node = VFSNode(node_data['name'], 'file')
                    content_b64 = node_data.get('content', '')
                    node.content = content_b64
                    node.permissions = node_data.get('permissions', '644')
                    
                return node
                
            self.root = build_node(data['root'], None)
            self.name = data.get('name', 'json_vfs')
            
            with open(json_path, 'rb') as f:
                self.source_hash = hashlib.sha256(f.read()).hexdigest()
                
            print(f"[VFS] Загружена VFS из JSON: {json_path}")
            return ""
            
        except Exception as e:
            raise RuntimeError(f"Ошибка загрузки JSON VFS: {e}")
    
    def create_default(self):
        """Создает VFS по умолчанию"""
        self.root = VFSNode("/", "directory")
        
        # Создаем базовую структуру
        home = VFSNode("home", "directory")
        self.root.add_child(home)
        
        user = VFSNode("user", "directory")
        home.add_child(user)
        
        etc = VFSNode("etc", "directory")
        self.root.add_child(etc)
        
        # Добавляем motd
        motd = VFSNode("motd", "file")
        motd.content = base64.b64encode(b"Welcome to the emulator!\nThis is default VFS.\n").decode('ascii')
        self.root.add_child(motd)
        
        # Добавляем README
        readme = VFSNode("README.txt", "file")
        readme.content = base64.b64encode(b"Default VFS created by emulator.\n").decode('ascii')
        self.root.add_child(readme)
        
        self.name = "default_vfs"
        self.source_hash = hashlib.sha256(b"default").hexdigest()
        print("[VFS] Создана VFS по умолчанию")
    
    def change_dir(self, path):
        """Изменяет текущую директорию"""
        if path.startswith("/"):
            target_path = path
        else:
            # Относительный путь
            if self.current_path == "/":
                target_path = "/" + path
            else:
                target_path = self.current_path.rstrip("/") + "/" + path
                
        # Нормализуем путь
        parts = target_path.strip("/").split("/")
        normalized_parts = []
        
        for part in parts:
            if part == ".":
                continue
            elif part == "..":
                if normalized_parts:
                    normalized_parts.pop()
            else:
                normalized_parts.append(part)
                
        target_path = "/" + "/".join(normalized_parts)
        
        # Проверяем существование
        node = self.root.get_path(target_path.lstrip("/"))
        if not node or node.type != "directory":
            return False
            
        self.current_path = target_path
        return True
    
    def list_current_dir(self):
        """Список файлов в текущей директории"""
        node = self.root.get_path(self.current_path.lstrip("/"))
        if not node or node.type != "directory":
            return []
        return node.list_dir("")
    
    def cat_file(self, path):
        """Читает содержимое файла"""
        if not path.startswith("/"):
            # Относительный путь
            if self.current_path == "/":
                path = "/" + path
            else:
                path = self.current_path.rstrip("/") + "/" + path
                
        node_path = path.lstrip("/")
        node = self.root.get_path(node_path)
        
        if not node or node.type != "file":
            return None
            
        try:
            return base64.b64decode(node.content.encode('ascii')).decode('utf-8', errors='replace')
        except:
            return "[BINARY DATA]"

# ==================== ЭМУЛЯТОР С VFS ====================

class EmulatorVFS:
    """Эмулятор с поддержкой VFS"""
    
    def __init__(self, config):
        self.config = config
        self.vfs = VFS()
        self.logger = None  # Логирование из этапа 2
        self.running = True
        
        # Загружаем VFS
        self.load_vfs()
        
    def load_vfs(self):
        """Загружает VFS в зависимости от конфигурации"""
        vfs_path = self.config.get('vfs_path')
        
        if not vfs_path:
            print("[INFO] Путь к VFS не указан, создаем по умолчанию")
            self.vfs.create_default()
            return True
            
        if not os.path.exists(vfs_path):
            print(f"[ERROR] Файл VFS не найден: {vfs_path}")
            print("[INFO] Создаем VFS по умолчанию")
            self.vfs.create_default()
            return False
            
        try:
            if vfs_path.endswith('.zip'):
                motd = self.vfs.load_from_zip(vfs_path)
                if motd:
                    print(f"\n{'='*50}")
                    print("MOTD (Message of the Day):")
                    print(motd)
                    print('='*50)
            elif vfs_path.endswith('.json'):
                self.vfs.load_from_json(vfs_path)
            else:
                print(f"[ERROR] Неподдерживаемый формат VFS: {vfs_path}")
                self.vfs.create_default()
                return False
                
            return True
            
        except Exception as e:
            print(f"[ERROR] Ошибка загрузки VFS: {e}")
            self.vfs.create_default()
            return False
    
    def execute_command(self, cmd_line):
        """Выполняет команду"""
        parts = cmd_line.strip().split()
        if not parts:
            return
            
        cmd = parts[0]
        args = parts[1:]
        
        if cmd == "exit":
            print("Выход из эмулятора.")
            self.running = False
            
        elif cmd == "ls":
            if not args:
                files = self.vfs.list_current_dir()
                if files is None:
                    print("Ошибка: не директория")
                elif files:
                    for f in files:
                        print(f)
                else:
                    print("(пусто)")
            else:
                for arg in args:
                    print(f"ls {arg}: (пока не реализовано для путей)")
                    
        elif cmd == "cd":
            if not args:
                print("Использование: cd <путь>")
            else:
                if self.vfs.change_dir(args[0]):
                    print(f"Перешел в: {self.vfs.current_path}")
                else:
                    print(f"Ошибка: директория не найдена: {args[0]}")
                    
        elif cmd == "pwd":
            print(self.vfs.current_path)
            
        elif cmd == "cat":
            if not args:
                print("Использование: cat <файл>")
            else:
                content = self.vfs.cat_file(args[0])
                if content:
                    print(content)
                else:
                    print(f"Ошибка: файл не найден или недоступен: {args[0]}")
                    
        elif cmd == "vfs-info":
            print("\n=== ИНФОРМАЦИЯ О VFS ===")
            print(f"Имя: {self.vfs.name}")
            print(f"Текущий путь: {self.vfs.current_path}")
            print(f"Хеш SHA-256: {self.vfs.source_hash}")
            print(f"Корневая директория: есть")
            
        elif cmd == "tree":
            self.print_tree()
            
        elif cmd == "help":
            print("\n=== ДОСТУПНЫЕ КОМАНДЫ (VFS) ===")
            print("  ls                   - список файлов в текущей директории")
            print("  cd <путь>            - сменить директорию")
            print("  pwd                  - текущая директория")
            print("  cat <файл>           - показать содержимое файла")
            print("  vfs-info             - информация о загруженной VFS")
            print("  tree                 - показать дерево файловой системы")
            print("  exit                 - выйти из эмулятора")
            print("  help                 - эта справка")
            
        else:
            print(f"Неизвестная команда: {cmd}")
            print("Введите 'help' для списка команд")
    
    def print_tree(self, node=None, prefix="", is_last=True):
        """Выводит дерево файловой системы"""
        if node is None:
            node = self.vfs.root
            
        connector = "└── " if is_last else "├── "
        print(prefix + connector + node.name + ("/" if node.type == "directory" else ""))
        
        if node.type == "directory" and node.children:
            new_prefix = prefix + ("    " if is_last else "│   ")
            children_list = list(node.children.values())
            for i, child in enumerate(children_list):
                self.print_tree(child, new_prefix, i == len(children_list) - 1)
    
    def run_interactive(self):
        """Запускает интерактивный режим"""
        print("\n" + "="*60)
        print("ЭМУЛЯТОР КОМАНДНОЙ СТРОКИ С VFS")
        print("Вариант 7 - Этап 3: Виртуальная файловая система")
        print("="*60)
        print(f"Загружена VFS: {self.vfs.name}")
        print(f"Хеш: {self.vfs.source_hash[:16]}...")
        print("Введите 'help' для списка команд")
        print("="*60)
        
        while self.running:
            try:
                # Формируем приглашение
                user = "student"
                hostname = "localhost"
                path_display = self.vfs.current_path
                if len(path_display) > 20:
                    path_display = "..." + path_display[-17:]
                    
                prompt = f"{user}@{hostname}:{path_display}$ "
                cmd_line = input(prompt)
                
                self.execute_command(cmd_line)
                
            except KeyboardInterrupt:
                print("\n\nПрервано пользователем.")
                break
            except EOFError:
                print("\n\nКонец ввода.")
                break
            except Exception as e:
                print(f"\nОшибка: {e}")

# ==================== КОНФИГУРАЦИЯ ====================

def load_config(config_path="config.yaml"):
    """Загружает конфигурацию"""
    config = {
        'vfs_path': None,
        'prompt': "user@host:path$ "
    }
    
    if config_path and os.path.exists(config_path):
        try:
            with open(config_path, 'r') as f:
                yaml_config = yaml.safe_load(f)
                if yaml_config:
                    config.update(yaml_config)
        except Exception as e:
            print(f"Ошибка чтения конфига: {e}")
    
    return config

# ==================== ТЕСТОВЫЕ СКРИПТЫ ====================

def run_test_script(emulator, script_path):
    """Выполняет тестовый скрипт"""
    if not os.path.exists(script_path):
        print(f"Скрипт не найден: {script_path}")
        return
        
    print(f"\n=== ВЫПОЛНЕНИЕ ТЕСТОВОГО СКРИПТА: {script_path} ===")
    
    with open(script_path, 'r') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
                
            print(f"\n> {line}")
            emulator.execute_command(line)
    
    print("\n=== ТЕСТОВЫЙ СКРИПТ ЗАВЕРШЕН ===")

# ==================== ГЛАВНАЯ ФУНКЦИЯ ====================

def main():
    """Главная функция"""
    parser = argparse.ArgumentParser(description='Эмулятор с VFS (Этап 3)')
    parser.add_argument('--vfs-path', help='Путь к VFS (ZIP/JSON)')
    parser.add_argument('--config', default='config.yaml', help='Конфигурационный файл')
    parser.add_argument('--test-script', help='Тестовый скрипт для выполнения')
    parser.add_argument('--dump-vfs', action='store_true', help='Вывести информацию о VFS и выйти')
    
    args = parser.parse_args()
    
    # Загружаем конфигурацию
    config = load_config(args.config)
    
    # Приоритет: командная строка > конфиг файл
    if args.vfs_path:
        config['vfs_path'] = args.vfs_path
    
    print("\n" + "="*60)
    print("ЭТАП 3: ВИРТУАЛЬНАЯ ФАЙЛОВАЯ СИСТЕМА (VFS)")
    print("="*60)
    print(f"Конфиг: {args.config}")
    print(f"VFS путь: {config['vfs_path'] or 'не указан (будет создана по умолчанию)'}")
    print("="*60)
    
    # Создаем эмулятор
    emulator = EmulatorVFS(config)
    
    # Если запрошен только вывод информации
    if args.dump_vfs:
        emulator.execute_command("vfs-info")
        return
    
    # Если указан тестовый скрипт
    if args.test_script:
        run_test_script(emulator, args.test_script)
        return
    
    # Запускаем интерактивный режим
    emulator.run_interactive()
    
    print("\n" + "="*60)
    print("Работа эмулятора завершена")
    print("="*60)

# ==================== ТОЧКА ВХОДА ====================

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nПрограмма прервана")
    except Exception as e:
        print(f"\nКритическая ошибка: {e}")
        sys.exit(1)
