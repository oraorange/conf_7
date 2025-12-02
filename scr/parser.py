import shlex
import os

class Parser:
    def parse(self, input_string):
        # Раскрываем переменные окружения
        expanded = os.path.expandvars(input_string)
        # Разбиваем на токены с учетом кавычек
        tokens = shlex.split(expanded)
        if not tokens:
            return "", []
        cmd = tokens[0]
        args = tokens[1:]
        return cmd, args
