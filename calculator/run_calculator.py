
from calculator import RPNCalculator


def main():
    # Создаем калькулятор
    calc = RPNCalculator()

    print("=" * 50)
    print("КАЛЬКУЛЯТОР С ОБРАТНОЙ ПОЛЬСКОЙ НОТАЦИЕЙ")
    print("=" * 50)
    print("Поддерживаемые операции:")
    print("  +, -, *, /, ^ (степень)")
    print("  sqrt(), sin(), cos()")
    print("  Скобки ( )")
    print("=" * 50)

    while True:
        try:
            # Ввод выражения
            expr = input("\nВведите выражение (или 'exit' для выхода): ").strip()

            if expr.lower() in ['exit', 'quit', 'q', 'выход']:
                print("До свидания!")
                break

            if not expr:
                continue

            # Вычисление
            result = calc.calculate(expr)
            rpn = calc.get_rpn()

            # Вывод результатов
            print(f"Выражение: {expr}")
            print(f"RPN: {' '.join(rpn)}")
            print(f"Результат: {result}")

        except Exception as e:
            print(f"Ошибка: {e}")


if __name__ == "__main__":
    main()