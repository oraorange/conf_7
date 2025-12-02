#!/bin/bash
# Тестовые скрипты для проверки параметров командной строки
# Вариант 7, Этап 2

echo "Тест 1: Запуск с параметрами командной строки"
python ../variant7/stage2/emulator.py \
  --vfs-path ./test_vfs.zip \
  --log-path ./test.log \
  --script-path ./startup.txt

echo ""
echo "Тест 2: Запуск с конфигурационным файлом"
python ../variant7/stage2/emulator.py \
  --config-path ../variant7/stage2/config.yaml

echo ""
echo "Тест 3: Вывод только конфигурации (dump-config)"
python ../variant7/stage2/emulator.py \
  --config-path ../variant7/stage2/config.yaml \
  --dump-config

echo ""
echo "Тест 4: Приоритет командной строки над конфигом"
python ../variant7/stage2/emulator.py \
  --config-path ../variant7/stage2/config.yaml \
  --vfs-path ./override.zip \
  --log-path ./override.log
