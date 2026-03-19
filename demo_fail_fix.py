"""
Демонстрация провального и успешного тестирования
"""

import unittest


class DemoTest(unittest.TestCase):
    def test_failing(self):
        """Этот тест специально провалится"""
        print("\n❌ Провальный тест: ожидаем 2, получили 1")
        self.assertEqual(1, 2, "Этот тест должен провалиться")

    def test_fixed(self):
        """Этот тест успешно проходит"""
        print("\n✅ Успешный тест: 1 == 1")
        self.assertEqual(1, 1, "Тест исправлен и проходит")


if __name__ == '__main__':
    print("=" * 50)
    print("ДЕМОНСТРАЦИЯ ТЕСТИРОВАНИЯ")
    print("=" * 50)

    # Запускаем тесты
    suite = unittest.TestLoader().loadTestsFromTestCase(DemoTest)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    print("\n" + "=" * 50)
    print("ИТОГИ:")
    print(f"Пройдено тестов: {result.testsRun - len(result.failures)}")
    print(f"Провалено тестов: {len(result.failures)}")
    print("=" * 50)