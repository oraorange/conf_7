#!/bin/bash
echo "Тестирование этапа 1 (REPL)"
echo "=========================="

# Переходим в корневую директорию проекта
cd ../..

# Проверяем наличие Python
if ! command -v python3 &> /dev/null; then
    echo "Ошибка: Python3 не установлен"
    exit 1
fi

# Проверяем наличие основного файла
if [ ! -f "src/emulator.py" ]; then
    echo "Ошибка: файл src/emulator.py не найден"
    exit 1
fi

echo "1. Проверка синтаксиса Python..."
python3 -m py_compile src/emulator.py
if [ $? -eq 0 ]; then
    echo "✓ Синтаксис корректен"
else
    echo "✗ Ошибка синтаксиса"
    exit 1
fi

echo ""
echo "2. Запуск эмулятора (тестовый режим)..."
echo "Для теста эмулятор будет запущен с автоматическим выходом."
echo "Если зависнет более 5 секунд - нажмите Ctrl+C"

# Создаём тестовый скрипт с командами
TEST_INPUT=$(cat << EOF
ls -la
cd \$HOME
unknown_command
exit
EOF
)

# Запускаем эмулятор с тестовыми командами
echo "$TEST_INPUT" | timeout 5 python3 src/emulator.py 2>&1 | head -20

echo ""
echo "Тестирование завершено!"
echo "Для полной проверки запустите: python3 src/emulator.py"
