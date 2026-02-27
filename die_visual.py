import pygal
import customtkinter as ctk
import simulation as sim
from PIL import Image
from die import Die
from main_window import MainWindow
from die_widget import DieWidget
import charts as ch
from dice_table import DiceTable

# Задание количества кубиков и бросков
count_dices = 7
count_rolls = 3000

# Создание определенного количества кубиков
dice = [Die() for _ in range(count_dices)]
# Моделирование серии бросков с сохранением результатов в списке
results = sim.roll_dice(dice, count_rolls)
# Подсчет минимального и максимального результата одновременного броска кубиков
min_result, max_result = sim.calc_result_range(dice)
# Подсчет частоты выпадения каждого результата
frequencies = sim.calc_frequency(results, min_result, max_result)


# Задание заголовка диаграммы
title = f"Results of rolling {count_dices} dice {count_rolls} times."
# Задание меток оси X
x_labels = [str(value) for value in range(count_dices, max_result+1)]
# Создание диаграммы
chart = ch.build_chart("bar_vertical", title, x_labels, frequencies)
# Сохранение диаграммы в файл
chart.render_to_file('die_visual.svg')


# Задание стиля окна
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# Создание главного окна настроек
app = MainWindow(count_dices, count_rolls)

# Запуск приложения
app.mainloop()


