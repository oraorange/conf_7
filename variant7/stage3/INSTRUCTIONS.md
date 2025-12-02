# Этап 3: Виртуальная файловая система (VFS)
## Вариант 7

### Что реализовано:
1.  **Поддержка ZIP архивов** как источника VFS
2.  **Base64 кодирование** для двоичных данных
3.  **Загрузка VFS** с проверкой формата
4.  **Сообщения об ошибках** загрузки (файл не найден, неверный формат)
5.  **Вывод MOTD** (message of the day) при старте, если файл существует
6.  **Создание VFS по умолчанию** в памяти
7.  **Команда vfs-info** с хешем SHA-256
8.  **Тестовые скрипты** для различных вариантов VFS

### Поддерживаемые форматы VFS:
1. **ZIP архив** - автоматически распаковывается в памяти
2. **JSON файл** - структурированное описание файловой системы
3. **По умолчанию** - создается при отсутствии указанного пути

### Как использовать:

#### 1. Запуск с ZIP VFS:
```bash
python emulator.py --vfs-path ../vfs_examples/simple_vfs.zip


2 Запуск с JSON VFS:


python emulator.py --vfs-path ../vfs_examples/json_vfs.json
3. Запуск без VFS (создаст по умолчанию):


python emulator.py
4. Запуск тестового скрипта:


python emulator.py --test-script ../scripts/test_vfs_simple.txt
5. Только информация о VFS:


python emulator.py --vfs-path ../vfs_examples/simple_vfs.zip --dump-vfs

Новые команды в эмуляторе:

ls - список файлов в текущей директории
cd <путь> - смена директории
pwd - текущая директория
cat <файл> - чтение содержимого файла
vfs-info - информация о загруженной VFS (имя + хеш SHA-256)
tree - дерево файловой системы
exit - выход
help - справка
Примеры использования:

text
student@localhost:/$ ls
home  etc  motd  README.txt

student@localhost:/$ cd home
student@localhost:/home$ ls
user

student@localhost:/home$ cd user
student@localhost:/home/user$ cat document.txt
This is a test document.
It has multiple lines.
Third line here.

student@localhost:/home/user$ vfs-info
=== ИНФОРМАЦИЯ О VFS ===
Имя: json_vfs
Текущий путь: /home/user
Хеш SHA-256: a1b2c3d4e5f6...
Корневая директория: есть

student@localhost:/home/user$ tree
/
├── home/
│   └── user/
│       ├── document.txt
│       └── config.cfg
├── etc/
│   └── hosts
└── README.md

Тестирование:

Тест 1: Минимальная VFS

bash
python emulator.py --test-script ../scripts/test_vfs_simple.txt
Тест 2: Сложная VFS (3+ уровня)

bash
python emulator.py --vfs-path ../vfs_examples/json_vfs.json --test-script ../scripts/test_vfs_complex.txt
Тест 3: Ошибка загрузки

bash
python emulator.py --vfs-path ./not_exist.zip
(должен создать VFS по умолчанию)

Тест 4: Неверный формат

bash
python emulator.py --vfs-path ../README.md
