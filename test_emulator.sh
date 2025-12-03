#!/bin/bash
echo "Тест 1: Запуск без параметров"
python3 emulator.py

echo -e "\nТест 2: Запуск с лог-файлом"
python3 emulator.py --log test_log1.json --vfs dummy_vfs

echo -e "\nТест 3: Запуск со скриптом"
python3 emulator.py --script test.script --log test_log2.json

echo -e "\nТест 4: Все параметры вместе"
python3 emulator.py --vfs /some/path --log all_log.json --script test.script --config config.yaml 2>&1 | head -20
