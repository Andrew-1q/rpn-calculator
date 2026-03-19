"""
Модуль калькулятора с обратной польской нотацией.
Поддерживает операции: +, -, *, /, ^ (возведение в степень), sqrt, sin, cos
"""

import math
import operator
from typing import Union, List


class RPNCalculator:
    """
    Калькулятор, преобразующий инфиксную запись в обратную польскую нотацию
    и вычисляющий результат.
    """

    # Приоритеты операций (больше число - выше приоритет)
    PRIORITY = {
        '+': 1,
        '-': 1,
        '*': 2,
        '/': 2,
        '^': 3,
        'sqrt': 4,
        'sin': 4,
        'cos': 4,
        '(': 0,
        ')': 0
    }

    # Операциии и соответствующие функции
    OPERATIONS = {
        '+': operator.add,
        '-': operator.sub,
        '*': operator.mul,
        '/': operator.truediv,
        '^': pow,
        'sqrt': math.sqrt,
        'sin': math.sin,
        'cos': math.cos
    }

    def __init__(self):
        """Инициализация калькулятора."""
        self.expression = ""
        self.rpn_tokens = []
        self.result = None

    def tokenize(self, expression: str) -> List[str]:
        """
        Разбивает выражение на токены.

        Args:
            expression: Строка с математическим выражением

        Returns:
            Список токенов
        """
        expression = expression.replace(' ', '')
        tokens = []
        i = 0
        length = len(expression)

        while i < length:
            char = expression[i]

            # Проверка на числа (включая десятичные и отрицательные)
            if char.isdigit() or (char == '.' and i + 1 < length and expression[i + 1].isdigit()):
                num_start = i
                while i < length and (expression[i].isdigit() or expression[i] == '.'):
                    i += 1
                tokens.append(expression[num_start:i])
                continue

            # Проверка на функции
            if char.isalpha():
                func_start = i
                while i < length and expression[i].isalpha():
                    i += 1
                func_name = expression[func_start:i]
                if func_name in self.PRIORITY:
                    tokens.append(func_name)
                else:
                    raise ValueError(f"Неизвестная функция: {func_name}")
                continue

            # Обработка операторов и скобок
            if char in '+-*/^()':
                # Проверка на унарный минус
                if char == '-' and (i == 0 or expression[i - 1] in '(+*/^'):
                    tokens.append('0')  # Добавляем 0 для обработки унарного минуса
                tokens.append(char)
                i += 1
                continue

            raise ValueError(f"Недопустимый символ: {char}")

        return tokens

    def infix_to_rpn(self, tokens: List[str]) -> List[str]:
        """
        Преобразует инфиксную запись в обратную польскую нотацию (алгоритм сортировочной станции).

        Args:
            tokens: Список токенов в инфиксной записи

        Returns:
            Список токенов в RPN
        """
        output = []
        stack = []

        #for token in tokens:
            # Если токен - число
            if self._is_number(token):
                output.append(token)

            # Если токен - функция
            elif token in ['sqrt', 'sin', 'cos']:
                stack.append(token)

            # Если токен - оператор
            elif token in self.OPERATIONS:
                while (stack and stack[-1] != '(' and
                       self.PRIORITY.get(stack[-1], 0) >= self.PRIORITY[token]):
                    output.append(stack.pop())
                stack.append(token)

            # Если токен - открывающая скобка
            elif token == '(':
                stack.append(token)

            # Если токен - закрывающая скобка
            elif token == ')':
                while stack and stack[-1] != '(':
                    output.append(stack.pop())
                if stack and stack[-1] == '(':
                    stack.pop()  # Удаляем '('
                # Если на вершине стека функция, добавляем её в выходную строку
                if stack and stack[-1] in ['sqrt', 'sin', 'cos']:
                    output.append(stack.pop())

        # Выталкиваем оставшиеся операторы из стека
        while stack:
            if stack[-1] == '(':
                raise ValueError("Несбалансированные скобки")
            output.append(stack.pop())

        return output

    def evaluate_rpn(self, rpn_tokens: List[str]) -> float:
        """
        Вычисляет значение выражения в RPN.

        Args:
            rpn_tokens: Список токенов в RPN

        Returns:
            Результат вычисления
        """
        stack = []

        for token in rpn_tokens:
            if self._is_number(token):
                stack.append(float(token))
            elif token in self.OPERATIONS:
                if token in ['sqrt', 'sin', 'cos']:
                    # Унарные операции
                    if len(stack) < 1:
                        raise ValueError(f"Недостаточно операндов для {token}")
                    a = stack.pop()
                    result = self.OPERATIONS[token](a)
                else:
                    # Бинарные операции
                    if len(stack) < 2:
                        raise ValueError(f"Недостаточно операндов для {token}")
                    b = stack.pop()
                    a = stack.pop()
                    result = self.OPERATIONS[token](a, b)
                stack.append(result)

        if len(stack) != 1:
            raise ValueError("Некорректное выражение")

        return stack[0]

    def calculate(self, expression: str) -> float:
        """
        Основной метод: вычисляет значение выражения.

        Args:
            expression: Строка с математическим выражением

        Returns:
            Результат вычисления
        """
        self.expression = expression
        tokens = self.tokenize(expression)
        self.rpn_tokens = self.infix_to_rpn(tokens)
        self.result = self.evaluate_rpn(self.rpn_tokens)
        return self.result

    def _is_number(self, token: str) -> bool:
        """
        Проверяет, является ли токен числом.

        Args:
            token: Строка для проверки

        Returns:
            True, если токен - число, иначе False
        """
        try:
            float(token)
            return True
        except ValueError:
            return False

    def get_rpn(self) -> List[str]:
        """Возвращает RPN представление последнего вычисленного выражения."""
        return self.rpn_tokens

    def get_last_result(self) -> float:
        """Возвращает результат последнего вычисления."""
        return self.result