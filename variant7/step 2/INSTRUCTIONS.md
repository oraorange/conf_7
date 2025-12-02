# Этап 2: Конфигурация
## Вариант 7

### Что реализовано:
1.  Параметры командной строки (--vfs-path, --log-path, --script-path, --config-path)
2.  Конфигурационный файл YAML
3.  Логирование в JSON формате
4.  Стартовый скрипт с поддержкой комментариев
5.  Приоритеты: командная строка > конфигурационный файл
6.  Команда conf-dump для вывода конфигурации
7.  Обработка ошибок конфигурации

### Как запустить:

#### 1. Базовый запуск (использует config.yaml):
```bash
python emulator.py

### с параметрами ком строки
python emulator.py \
  --vfs-path ./vfs.zip \
  --log-path ./emulator.log \
  --script-path ./startup.txt

###с указанием конфгурационного файла
python emulator.py --config-path my_config.yaml

### Только вывод конфигурации:
python emulator.py --config-path config.yaml --dump-config

### примеры команд в эмуляторе
user@localhost:myvfs$ ls -la
user@localhost:myvfs$ cd /home
user@localhost:myvfs$ conf-dump
user@localhost:myvfs$ log-test
user@localhost:myvfs$ help
user@localhost:myv7s$ exit

### структура лог-файла
{
  "timestamp": "2024-01-15T10:30:00",
  "event_type": "COMMAND",
  "command": "ls",
  "arguments": ["-la"],
  "error_message": "",
  "user": "student"
}

### тесты
cd scripts
bash test_params.sh

