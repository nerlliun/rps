"""
Главный модуль консольного приложения
Демонстрирует работу сортировки Шелла
"""

import sys
import os

# Добавляем путь для импорта модулей проекта
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

from src.shell_sort import shell_sort_with_stats, is_sorted
from src.utils import (
    read_from_keyboard,
    generate_random_array,
    load_from_file,
    print_results
)


def display_menu():
    """Отображение главного меню"""
    print("\n" + "=" * 60)
    print("ПРОГРАММА СОРТИРОВКИ ШЕЛЛА")
    print("=" * 60)
    print("Выберите способ ввода данных:")
    print("  1. Ввод с клавиатуры")
    print("  2. Генерация случайных чисел")
    print("  3. Загрузка из файла")
    print("  4. Выход")
    print("-" * 60)


def get_array_from_user():
    """
    Получение массива от пользователя с возможностью повторной попытки
    Возвращает массив или None, если пользователь хочет выйти
    """
    while True:
        display_menu()

        choice = input("Ваш выбор (1-4): ").strip()

        # Выход из программы
        if choice == '4':
            return None

        if choice == '1':
            user_array = read_from_keyboard()

        elif choice == '2':
            user_array = generate_random_array()

        elif choice == '3':
            filename = input("Введите имя файла: ").strip()
            user_array = load_from_file(filename)

        else:
            print("Ошибка: неверный выбор. Используйте 1, 2, 3 или 4")
            input("\nНажмите Enter для продолжения...")
            continue

        # Проверка корректности полученного массива
        if user_array is None:
            print("Не удалось получить массив.")
            retry = input("Повторить попытку? (y/n): ").strip().lower()
            if retry in ('y', 'yes', 'да', 'д'):
                continue
            return None

        if len(user_array) == 0:
            print("Ошибка: массив пуст")
            retry = input("Повторить попытку? (y/n): ").strip().lower()
            if retry in ('y', 'yes', 'да', 'д'):
                continue
            return None

        return user_array


def save_results_to_file(filename, user_array, sorted_array, statistics):
    """
    Сохранение результатов в файл с проверками
    Возвращает True при успешном сохранении, False при ошибке
    """
    # Проверка на пустое имя
    if not filename:
        print("Ошибка: имя файла не может быть пустым")
        return False

    # Проверка на недопустимые символы
    invalid_chars = '<>:"/\\|?*'
    if any(char in filename for char in invalid_chars):
        print("Ошибка: имя файла содержит недопустимые символы")
        return False

    # Проверка, не является ли имя папкой
    if os.path.isdir(filename):
        print("Ошибка: указанное имя является папкой, а не файлом")
        return False

    # Проверка существования файла
    if os.path.exists(filename):
        print("Ошибка: указанное имя уже существует")
        return False

    # Попытка сохранить
    try:
        # Создаем директорию, если её нет
        file_dir = os.path.dirname(filename)
        if file_dir and not os.path.exists(file_dir):
            os.makedirs(file_dir)

        with open(filename, 'w', encoding='utf-8') as file:
            file.write("РЕЗУЛЬТАТЫ СОРТИРОВКИ ШЕЛЛА\n")
            file.write("=" * 40 + "\n\n")

            file.write("ИСХОДНЫЙ МАССИВ:\n")
            file.write(' '.join(str(x) for x in user_array) + "\n\n")

            file.write("ОТСОРТИРОВАННЫЙ МАССИВ:\n")
            file.write(' '.join(str(x) for x in sorted_array) + "\n\n")

            file.write("СТАТИСТИКА:\n")
            file.write(f"  Количество сравнений: {statistics['comparisons']}\n")
            file.write(f"  Количество обменов: {statistics['swaps']}\n")
            file.write(f"  Количество проходов: {statistics['passes']}\n")

        print(f"Результаты сохранены в файл '{filename}'")
        return True

    except PermissionError:
        print("Ошибка: нет прав для записи в файл")
        return False

    except IOError as e:
        print(f"Ошибка при сохранении в файл: {e}")
        return False

    except Exception as e:
        print(f"Непредвиденная ошибка при сохранении: {e}")
        return False


def main():
    """Основная функция программы"""

    while True:
        # Получаем массив от пользователя
        user_array = get_array_from_user()

        # Если пользователь выбрал выход
        if user_array is None:
            print("Программа завершена.")
            break

        # Вывод исходного массива
        print(f"\nИсходный массив: {user_array}")

        # Сортировка
        print("Выполняется сортировка...")
        sorted_array, statistics = shell_sort_with_stats(user_array)

        # Проверка корректности сортировки
        if is_sorted(sorted_array):
            print("Сортировка выполнена успешно")
        else:
            print("ОШИБКА: массив не отсортирован!")

        # Вывод результатов
        print_results(user_array, sorted_array, statistics)

        # Предложение сохранить результаты
        save_choice = input("\nСохранить результаты в файл? (y/n): ").strip().lower()
        if save_choice in ('y', 'yes', 'да', 'д'):
            while True:
                filename = input("Имя файла для сохранения: ").strip()

                if save_results_to_file(filename, user_array, sorted_array, statistics):
                    break
                else:
                    retry = input("Повторить попытку? (y/n): ").strip().lower()
                    if retry not in ('y', 'yes', 'да', 'д'):
                        break

        # Предложение продолжить или выйти
        continue_choice = input("\nВыполнить новую сортировку? (y/n): ").strip().lower()
        if continue_choice not in ('y', 'yes', 'да', 'д'):
            print("Программа завершена.")
            break


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nПрограмма прервана пользователем.")
        sys.exit(0)
    except Exception as error:
        print(f"\nНепредвиденная ошибка: {error}")
        sys.exit(1)
