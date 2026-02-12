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


def open_advanced_window():
    """Открытие окна расширенных настроек"""
    global advanced_window
    stats_options = ["variance", "mean", "mode", "Range", "Confidence interval", "Standard deviation", "Median",
                     "Kurtosis", "Skewness"]
    stats_vars = {}
    columns = 3

    advanced_window = ctk.CTkToplevel(app)
    advanced_window.title("Advanced settings")
    advanced_window.geometry("500x600")
    advanced_window.resizable(False, False)

    # Установка родительского окна
    advanced_window.transient(app)
    # Блокировка главного окна
    advanced_window.grab_set()

    advanced_window.grid_columnconfigure(0, weight=1)
    advanced_window.grid_columnconfigure(1, weight=1)

    # Заголовок окна
    header = ctk.CTkLabel(advanced_window, text="Advanced settings", font=("Arial", 20), anchor="center")
    header.grid(row=0, column=0, columnspan=2, pady=10, padx=10, sticky="ew")

    stats_label = ctk.CTkLabel(advanced_window, text="Statistical characteristics calculation", font=("Arial", 12), width=60)
    stats_label.grid(row=1, column=0, padx=10, pady=0, sticky="w")

    container = ctk.CTkFrame(advanced_window, fg_color="transparent", height=130, width=450)
    container.grid(row=2, column=0, columnspan=2, pady=0, padx=10, sticky="ew")
    container.grid_propagate(False)

    # Настраиваем grid внутри контейнера
    container.grid_columnconfigure(0, weight=1)
    container.grid_rowconfigure(0, weight=1)

    stats_frame = ctk.CTkScrollableFrame(container, corner_radius=10, fg_color="#2b2b2b")
    stats_frame.grid(row=0, column=0, sticky="nsew")

    # Создание ряда чекбоксов для выбора статистических характеристик
    for i, name in enumerate(stats_options):
        var = ctk.BooleanVar(value=False)
        stats_vars[name] = var

        checkbox = ctk.CTkCheckBox(stats_frame, text=name, variable=var)

        row = i // columns
        column = i % columns

        checkbox.grid(row=row, column=column, padx=10, pady=7, sticky="w")




    def on_close_advanced():
        """Обработчик закрытия окна"""
        global advanced_window
        # Разблокировка главного окна
        advanced_window.grab_release()
        advanced_window.destroy()
        advanced_window = None
        #action_button.configure(state="normal")
        #advanced_check.configure(state="normal")
    # Перехват системного события закрытия окна
    advanced_window.protocol("WM_DELETE_WINDOW", on_close_advanced)


app.mainloop()


