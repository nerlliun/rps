import sys
import os
import time
import random
from contextlib import contextmanager

# Добавляем путь к проекту
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.database import init_db, save_array, clear_all_arrays
from src.shell_sort import shell_sort

# Используем отдельную БД для тестов
TEST_DB_PATH = os.path.join(os.path.dirname(__file__), 'test_database.db')


@contextmanager
def test_db():
    """Временная БД для тестов"""
    import src.database
    original_path = src.database.DB_PATH
    src.database.DB_PATH = TEST_DB_PATH

    if os.path.exists(TEST_DB_PATH):
        os.remove(TEST_DB_PATH)

    init_db()

    try:
        yield
    finally:
        if os.path.exists(TEST_DB_PATH):
            os.remove(TEST_DB_PATH)
        src.database.DB_PATH = original_path


def generate_random_array(size):
    """Генерация случайного массива"""
    return [random.randint(-100, 100) for _ in range(size)]


def test_add_arrays(count):
    """Тест добавления count массивов"""
    print(f"\n--- Тест добавления {count} массивов ---")

    with test_db():
        start_time = time.time()

        for i in range(count):
            size = random.randint(5, 20)
            original = generate_random_array(size)
            sorted_arr = shell_sort(original)
            save_array(1, original, sorted_arr)

        elapsed = time.time() - start_time

        from src.database import get_db
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT COUNT(*) as cnt FROM arrays')
            count_result = cursor.fetchone()
            added_count = count_result['cnt']

        success = (added_count == count)
        print(f"Результат: {'УСПЕХ' if success else 'НЕУДАЧА'}")
        print(f"Время: {elapsed:.3f} сек")
        print(f"Скорость: {count / elapsed:.1f} записей/сек")
        print(f"Добавлено записей: {added_count}")


def test_load_and_sort(count):
    """Тест выгрузки и сортировки count массивов"""
    print(f"\n--- Тест выгрузки и сортировки {count} массивов ---")

    with test_db():
        arrays = []
        for i in range(count):
            size = random.randint(5, 20)
            original = generate_random_array(size)
            arrays.append(original)
            sorted_arr = shell_sort(original)
            save_array(1, original, sorted_arr)

        start_time = time.time()
        successful = 0

        from src.database import get_db
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT original_array FROM arrays')
            rows = cursor.fetchall()

            for row in rows:
                original = list(map(int, row['original_array'].split()))
                test_sorted = shell_sort(original)

                is_sorted_correct = all(test_sorted[i] <= test_sorted[i + 1]
                                        for i in range(len(test_sorted) - 1))
                if is_sorted_correct:
                    successful += 1

        elapsed = time.time() - start_time
        avg_time = elapsed / count if count > 0 else 0

        success = (successful == count)
        print(f"Результат: {'УСПЕХ' if success else 'НЕУДАЧА'}")
        print(f"Общее время: {elapsed:.3f} сек")
        print(f"Среднее время на массив: {avg_time * 1000:.2f} мс")
        print(f"Успешно обработано: {successful}/{count}")


def test_clear_database(count):
    """Тест очистки БД с count записями"""
    print(f"\n--- Тест очистки БД ({count} записей) ---")

    with test_db():
        for i in range(count):
            size = random.randint(5, 20)
            original = generate_random_array(size)
            sorted_arr = shell_sort(original)
            save_array(1, original, sorted_arr)

        start_time = time.time()
        deleted = clear_all_arrays()  # изменено с clear_all_database
        elapsed = time.time() - start_time

        from src.database import get_db
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT COUNT(*) as cnt FROM arrays')
            remaining = cursor.fetchone()['cnt']

        success = (deleted == count and remaining == 0)
        print(f"Результат: {'УСПЕХ' if success else 'НЕУДАЧА'}")
        print(f"Время: {elapsed:.3f} сек")
        print(f"Удалено записей: {deleted}")
        print(f"Осталось записей: {remaining}")


def run_all_tests():
    """Запуск всех интеграционных тестов"""
    print("=" * 70)
    print("ИНТЕГРАЦИОННОЕ ТЕСТИРОВАНИЕ - СОРТИРОВКА ШЕЛЛА")
    print("=" * 70)

    # Тест 1: Добавление массивов
    for count in [100, 1000, 10000]:
        test_add_arrays(count)
        print("-" * 40)

    # Тест 2: Выгрузка и сортировка
    for count in [100, 1000, 10000]:
        for run in range(1, 4):
            print(f"\n--- Запуск {run} для {count} массивов ---")
            test_load_and_sort(count)
        print("-" * 40)

    # Тест 3: Очистка БД
    for count in [100, 1000, 10000]:
        test_clear_database(count)
        print("-" * 40)

    print("\n" + "=" * 70)
    print("ТЕСТИРОВАНИЕ ЗАВЕРШЕНО")
    print("=" * 70)


if __name__ == "__main__":
    run_all_tests()
