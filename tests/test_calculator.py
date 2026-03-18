"""
Модуль тестирования калькулятора RPN.
"""

import unittest
import math
from calculator.rpn_calculator import RPNCalculator


class TestRPNCalculator(unittest.TestCase):
    """Тесты для калькулятора RPN."""

    def setUp(self):
        """Подготовка к тестам."""
        self.calc = RPNCalculator()

    # Тесты токенизации
    def test_tokenize_simple(self):
        """Тест токенизации простого выражения."""
        tokens = self.calc.tokenize("3+5")
        self.assertEqual(tokens, ['3', '+', '5'])

    def test_tokenize_with_spaces(self):
        """Тест токенизации с пробелами."""
        tokens = self.calc.tokenize("3 + 5 * 2")
        self.assertEqual(tokens, ['3', '+', '5', '*', '2'])

    def test_tokenize_with_parentheses(self):
        """Тест токенизации со скобками."""
        tokens = self.calc.tokenize("(3+5)*2")
        self.assertEqual(tokens, ['(', '3', '+', '5', ')', '*', '2'])

    def test_tokenize_decimal(self):
        """Тест токенизации десятичных чисел."""
        tokens = self.calc.tokenize("3.5+2.1")
        self.assertEqual(tokens, ['3.5', '+', '2.1'])

    def test_tokenize_functions(self):
        """Тест токенизации функций."""
        tokens = self.calc.tokenize("sqrt(4)+sin(0)")
        self.assertEqual(tokens, ['sqrt', '(', '4', ')', '+', 'sin', '(', '0', ')'])

    def test_tokenize_unary_minus(self):
        """Тест токенизации унарного минуса."""
        tokens = self.calc.tokenize("-5+3")
        self.assertEqual(tokens, ['0', '-', '5', '+', '3'])

    def test_tokenize_invalid_character(self):
        """Тест обработки недопустимого символа."""
        with self.assertRaises(ValueError) as context:
            self.calc.tokenize("3$5")
        self.assertIn("Недопустимый символ", str(context.exception))

    def test_tokenize_unknown_function(self):
        """Тест обработки неизвестной функции."""
        with self.assertRaises(ValueError) as context:
            self.calc.tokenize("unknown(5)")
        self.assertIn("Неизвестная функция", str(context.exception))

    # Тесты преобразования в RPN
    def test_infix_to_rpn_simple(self):
        """Тест преобразования простого выражения в RPN."""
        tokens = ['3', '+', '5']
        rpn = self.calc.infix_to_rpn(tokens)
        self.assertEqual(rpn, ['3', '5', '+'])

    def test_infix_to_rpn_priority(self):
        """Тест преобразования с учётом приоритетов."""
        tokens = ['3', '+', '5', '*', '2']
        rpn = self.calc.infix_to_rpn(tokens)
        self.assertEqual(rpn, ['3', '5', '2', '*', '+'])

    def test_infix_to_rpn_parentheses(self):
        """Тест преобразования со скобками."""
        tokens = ['(', '3', '+', '5', ')', '*', '2']
        rpn = self.calc.infix_to_rpn(tokens)
        self.assertEqual(rpn, ['3', '5', '+', '2', '*'])

    def test_infix_to_rpn_power(self):
        """Тест преобразования с возведением в степень."""
        tokens = ['2', '^', '3', '+', '4']
        rpn = self.calc.infix_to_rpn(tokens)
        self.assertEqual(rpn, ['2', '3', '^', '4', '+'])

    def test_infix_to_rpn_functions(self):
        """Тест преобразования с функциями."""
        tokens = ['sqrt', '(', '4', ')']
        rpn = self.calc.infix_to_rpn(tokens)
        self.assertEqual(rpn, ['4', 'sqrt'])

    def test_infix_to_rpn_unbalanced_parentheses(self):
        """Тест обработки несбалансированных скобок."""
        tokens = ['(', '3', '+', '5']
        with self.assertRaises(ValueError) as context:
            self.calc.infix_to_rpn(tokens)
        self.assertIn("Несбалансированные скобки", str(context.exception))

    # Тесты вычисления RPN
    def test_evaluate_rpn_simple(self):
        """Тест вычисления простого RPN выражения."""
        rpn = ['3', '5', '+']
        result = self.calc.evaluate_rpn(rpn)
        self.assertEqual(result, 8.0)

    def test_evaluate_rpn_complex(self):
        """Тест вычисления сложного RPN выражения."""
        rpn = ['3', '5', '2', '*', '+']
        result = self.calc.evaluate_rpn(rpn)
        self.assertEqual(result, 13.0)

    def test_evaluate_rpn_division(self):
        """Тест вычисления с делением."""
        rpn = ['10', '3', '/']
        result = self.calc.evaluate_rpn(rpn)
        self.assertAlmostEqual(result, 3.3333333333333335)

    def test_evaluate_rpn_power(self):
        """Тест вычисления степени."""
        rpn = ['2', '3', '^']
        result = self.calc.evaluate_rpn(rpn)
        self.assertEqual(result, 8.0)

    def test_evaluate_rpn_sqrt(self):
        """Тест вычисления квадратного корня."""
        rpn = ['4', 'sqrt']
        result = self.calc.evaluate_rpn(rpn)
        self.assertEqual(result, 2.0)

    def test_evaluate_rpn_sin(self):
        """Тест вычисления синуса."""
        rpn = ['0', 'sin']
        result = self.calc.evaluate_rpn(rpn)
        self.assertEqual(result, 0.0)

    def test_evaluate_rpn_cos(self):
        """Тест вычисления косинуса."""
        rpn = ['0', 'cos']
        result = self.calc.evaluate_rpn(rpn)
        self.assertEqual(result, 1.0)

    def test_evaluate_rpn_insufficient_operands(self):
        """Тест обработки недостаточного количества операндов."""
        rpn = ['3', '+']
        with self.assertRaises(ValueError) as context:
            self.calc.evaluate_rpn(rpn)
        self.assertIn("Недостаточно операндов", str(context.exception))

    def test_evaluate_rpn_invalid_expression(self):
        """Тест обработки некорректного выражения."""
        rpn = ['3', '5']
        with self.assertRaises(ValueError) as context:
            self.calc.evaluate_rpn(rpn)
        self.assertIn("Некорректное выражение", str(context.exception))

    # Интеграционные тесты
    def test_calculate_simple(self):
        """Тест полного цикла вычисления простого выражения."""
        result = self.calc.calculate("3+5")
        self.assertEqual(result, 8.0)
        self.assertEqual(self.calc.get_rpn(), ['3', '5', '+'])

    def test_calculate_with_parentheses(self):
        """Тест полного цикла вычисления выражения со скобками."""
        result = self.calc.calculate("(3+5)*2")
        self.assertEqual(result, 16.0)
        self.assertEqual(self.calc.get_rpn(), ['3', '5', '+', '2', '*'])

    def test_calculate_complex(self):
        """Тест полного цикла вычисления сложного выражения."""
        result = self.calc.calculate("3+5*2-8/4")
        self.assertEqual(result, 11.0)  # 3 + 10 - 2 = 11

    def test_calculate_with_power(self):
        """Тест полного цикла вычисления со степенью."""
        result = self.calc.calculate("2^3+4")
        self.assertEqual(result, 12.0)

    def test_calculate_with_functions(self):
        """Тест полного цикла вычисления с функциями."""
        result = self.calc.calculate("sqrt(9)+sin(0)")
        self.assertEqual(result, 3.0)

    def test_calculate_decimal(self):
        """Тест полного цикла вычисления с десятичными числами."""
        result = self.calc.calculate("3.5+2.1")
        self.assertAlmostEqual(result, 5.6)

    def test_calculate_unary_minus(self):
        """Тест полного цикла вычисления с унарным минусом."""
        result = self.calc.calculate("-5+3")
        self.assertEqual(result, -2.0)

    def test_calculate_nested_functions(self):
        """Тест полного цикла вычисления с вложенными функциями."""
        result = self.calc.calculate("sqrt(sin(0)+cos(0))")
        self.assertEqual(result, 1.0)


if __name__ == '__main__':
    unittest.main()