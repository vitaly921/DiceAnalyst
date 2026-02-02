from collections import Counter

def roll_dice(dice, rolls, mode="sum"):
    """Roll a dice"""
    results = []

    for _ in range(rolls):
        values = [d.roll() for d in dice]
        if mode == "sum":
            results.append(sum(values))
        elif mode == "product":
            result = 1
            for value in values:
                result *= value
            results.append(result)

    return results


def calc_result_range(dice, mode="sum"):
    min_result = 0
    max_result = 0

    if mode == "sum":
        min_result = len(dice)
        max_result = sum([d.num_sides for d in dice])
    elif mode == "product":
        min_result = 1
        max_result = 1
        for d in dice:
            max_result *= d.num_sides

    return min_result, max_result



def calc_frequency(results, min_result, max_result):
    counter = Counter(results)
    return [counter.get(value, 0) for value in range(min_result, max_result + 1)]


