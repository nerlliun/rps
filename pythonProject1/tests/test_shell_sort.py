import sys
import os

# Добавляем путь к тестируемым модулям
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
sys.path.insert(0, project_root)

from src.shell_sort import shell_sort, is_sorted


def run_test(test_name, test_function):
    """Вспомогательная функция для запуска тестов"""
    print(f"Тест {test_name}: ", end='')
    try:
        test_function()
        print("ПРОЙДЕН")
    except AssertionError as error:
        print(f"НЕ ПРОЙДЕН - {error}")
    except Exception as error:
        print(f"ОШИБКА - {error}")


def test_empty_array():
    """Тест сортировки пустого массива"""
    input_data = []
    expected = []
    result = shell_sort(input_data)
    assert result == expected, f"Получено {result}, ожидалось {expected}"
    assert is_sorted(result), "Результат не отсортирован"


def test_single_element():
    """Тест сортировки массива из одного элемента"""
    input_data = [21]
    expected = [21]
    result = shell_sort(input_data)
    assert result == expected, f"Получено {result}, ожидалось {expected}"
    assert is_sorted(result), "Результат не отсортирован"


def test_sorted_array():
    """Тест сортировки уже отсортированного массива"""
    input_data = [1, 2, 3, 4, 5]
    expected = [1, 2, 3, 4, 5]
    result = shell_sort(input_data)
    assert result == expected, f"Получено {result}, ожидалось {expected}"
    assert is_sorted(result), "Результат не отсортирован"


def test_reverse_sorted():
    """Тест сортировки массива в обратном порядке"""
    input_data = [5, 4, 3, 2, 1]
    expected = [1, 2, 3, 4, 5]
    result = shell_sort(input_data)
    assert result == expected, f"Получено {result}, ожидалось {expected}"
    assert is_sorted(result), "Результат не отсортирован"


def test_random_array():
    """Тест сортировки случайного массива"""
    input_data = [10, 50, 30, 20, 40]
    expected = [10, 20, 30, 40, 50]
    result = shell_sort(input_data)
    assert result == expected, f"Получено {result}, ожидалось {expected}"
    assert is_sorted(result), "Результат не отсортирован"


def test_duplicates():
    """Тест сортировки массива с дубликатами"""
    input_data = [3, 1, 4, 1, 5, 9, 2, 5]
    result = shell_sort(input_data)
    assert is_sorted(result), "Результат не отсортирован"
    assert sorted(input_data) == result, "Потеряны элементы"


def test_negative_numbers():
    """Тест сортировки массива с отрицательными числами"""
    input_data = [-5, 12, -3, 0, -8, 7]
    expected = [-8, -5, -3, 0, 7, 12]
    result = shell_sort(input_data)
    assert result == expected, f"Получено {result}, ожидалось {expected}"
    assert is_sorted(result), "Результат не отсортирован"


def test_preserve_original():
    """Тест сохранения исходного массива"""
    original = [3, 1, 4, 1, 5]
    original_copy = original.copy()

    shell_sort(original)

    assert original == original_copy, "Исходный массив был изменен"


def run_all_tests():
    """Запуск всех тестов"""
    print("=" * 70)
    print("ТЕСТИРОВАНИЕ АЛГОРИТМА СОРТИРОВКИ ШЕЛЛА")
    print("=" * 70)
    print()

    tests = [
        ("Пустой массив", test_empty_array),
        ("Один элемент", test_single_element),
        ("Уже отсортирован", test_sorted_array),
        ("Обратный порядок", test_reverse_sorted),
        ("Случайный набор", test_random_array),
        ("Дубликаты", test_duplicates),
        ("Отрицательные числа", test_negative_numbers),
        ("Сохранение оригинала", test_preserve_original)
    ]

    for test_name, test_func in tests:
        run_test(test_name, test_func)

    print("\n" + "=" * 70)
    print("ТЕСТИРОВАНИЕ ЗАВЕРШЕНО")
    print("=" * 70)


if __name__ == "__main__":
    run_all_tests()
