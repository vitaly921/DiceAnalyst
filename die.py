from random import randint

class Die:
    """Класс представляющий один кубик."""
    def __init__(self, num_sides=6):
        """По умолчанию кубик имеет 6 граней."""
        self.num_sides = num_sides

    def roll(self):
        """Возвращает случайное значение от 1 до количества граней."""
        return randint(1, self.num_sides)