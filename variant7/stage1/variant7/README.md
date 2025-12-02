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

student@localhost:myvfs$ ls -la
Команда 'ls': аргументы = ['-la']

student@localhost:myvfs$ cd /home
Команда 'cd': аргументы = ['/home']

student@localhost:myvfs$ exit
Выход из эмулятора.
