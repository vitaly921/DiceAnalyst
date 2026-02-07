from collections import Counter

def roll_dice(dice, rolls, mode="sum"):
    """Моделирование броска кубиков"""
    # Создание пустого списка для хранения результатов
    results = []
    # Перебор заданного количества одновременных бросков
    for _ in range(rolls):
        # Бросок каждого кубика и сохранение результата
        values = [d.roll() for d in dice]
        # Если выбран режим суммирования
        if mode == "sum":
            # Результаты бросков каждой серии складываются и добавляются в список
            results.append(sum(values))
        # Если выбран режим перемножения
        elif mode == "product":
            # Задание начального значения
            result = 1
            # Для каждого значения в текущей серии
            for value in values:
                # Перемножение результатов серии
                result *= value
            # Добавление результатов перемножения серии в список
            results.append(result)
    # Возвращение списка результатов
    return results


def calc_result_range(dice, mode="sum"):
    """Вычисление диапазона возможных результатов"""
    # Определение начальных значений
    min_result = 0
    max_result = 0
    # Для режима суммирования
    if mode == "sum":
        # Минимальный результат - это количество кубиков в серии
        min_result = len(dice)
        # Максимальный результат - это сумма максимальных значений для каждого кубика
        max_result = sum([d.num_sides for d in dice])
    # Для режима перемножения
    elif mode == "product":
        # Задание начальных значений
        min_result = 1
        max_result = 1
        # Для каждого кубика в серии
        for d in dice:
            # Перемножение максимальных значений всех кубиков в серии
            max_result *= d.num_sides
    # Возвращение минимального и максимального значения сложения/умножения
    return min_result, max_result



def calc_frequency(results, min_result, max_result):
    """Подсчет частоты появления результатов"""
    # Создание объекта Counter для подсчета количества каждого результата в списке results
    counter = Counter(results)
    # Создаем и возвращаем список частот появления результатов в определенном диапазоне
    return [counter.get(value, 0) for value in range(min_result, max_result + 1)]


