"""
Модуль реализации сортировки Шелла (Shellsort)
Алгоритм: улучшенная сортировка вставками с убывающим шагом
"""


def shell_sort(array):
    """
    Сортировка Шелла с последовательностью шагов (убывающей)
    Используется последовательность: n//2, n//4, ..., 1
    """
    # Создаем копию, чтобы не изменять оригинал
    result = array.copy()

    # Пустой список или из одного элемента сразу возвращаем
    if len(result) <= 1:
        return result

    n = len(result)
    # Начальный шаг
    gap = n // 2

    # Пока шаг больше 0
    while gap > 0:
        # Сортировка вставками с текущим шагом
        for i in range(gap, n):
            temp = result[i]
            j = i

            # Сдвигаем элементы, отсортированные на текущем шаге
            while j >= gap and result[j - gap] > temp:
                result[j] = result[j - gap]
                j -= gap

            result[j] = temp

        # Уменьшаем шаг
        gap //= 2

    return result


def shell_sort_with_stats(array):
    """
    Сортирует список и собирает статистику выполнения
    Возвращает: (отсортированный_массив, словарь_со_статистикой)
    """
    result = array.copy()

    if len(result) <= 1:
        return result, {'comparisons': 0, 'swaps': 0, 'passes': 0}

    n = len(result)
    gap = n // 2

    # Статистика
    comparisons = 0  # количество сравнений элементов
    swaps = 0  # количество обменов (фактических перестановок)
    passes = 0  # количество проходов (итераций внешнего цикла)

    while gap > 0:
        passes += 1  # каждый новый шаг - новый проход

        for i in range(gap, n):
            temp = result[i]
            j = i

            # Сравниваем и сдвигаем элементы
            while j >= gap:
                comparisons += 1  # сравнение result[j - gap] > temp
                if result[j - gap] > temp:
                    # Сдвигаем элемент вправо
                    result[j] = result[j - gap]
                    swaps += 1  # это операция присваивания, считаем как обмен
                    j -= gap
                else:
                    break

            # Если позиция изменилась, вставляем элемент
            if j != i:
                result[j] = temp
                swaps += 1  # вставка элемента

        gap //= 2

    statistics = {
        'comparisons': comparisons,
        'swaps': swaps,
        'passes': passes
    }

    return result, statistics


def is_sorted(array):
    """
    Проверяет, отсортирован ли список по возрастанию
    """
    for i in range(len(array) - 1):
        if array[i] > array[i + 1]:
            return False
    return True
