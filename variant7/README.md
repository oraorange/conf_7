# Эмулятор командной строки UNIX
## Вариант №7

### Этап 1: REPL
- Реализован базовый интерфейс командной строки
- Команды: ls, cd, exit, help
- Поддержка переменных окружения ($HOME, $USER)

### Как запустить:
```bash
cd variant7/stage1
python emulator.py
### Этап 2: Конфигурация
- Параметры командной строки: --vfs-path, --log-path, --script-path, --config-path
-  Конфигурационный файл YAML
-  Логирование событий в JSON формате
-  Стартовый скрипт с поддержкой комментариев
-  Приоритет командной строки над конфигурационным файлом
-  Команда `conf-dump` для вывода текущей конфигурации
-  Обработка ошибок чтения конфигурационных файлов

#### Примеры запуска:
```bash
# С параметрами командной строки
python variant7/stage2/emulator.py --vfs-path ./vfs.zip --log-path ./app.log

# С конфигурационным файлом
python variant7/stage2/emulator.py --config-path variant7/stage2/config.yaml

# Только вывод конфигурации
python variant7/stage2/emulator.py --config-path config.yaml --dump-config


### Файлы этапа 2:
variant7/step2/emulator.py - основной код
variant7/stepe2/config.yaml - конфигурация
variant7/step2/INSTRUCTIONS.md - инструкции
scripts/startup.txt - стартовый скрипт
scripts/test_params.sh - тестовые скрипты
logs/example.log - пример лог-файла

