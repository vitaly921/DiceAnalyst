import pygal
import customtkinter as ctk
from die import Die

# Создание двух кубиков: D6
die_1 = Die()
die_2 = Die()
die_3 = Die()

# Моделирование серии бросков с сохранением результатов в списке
results = []

for roll_num in range(3000):
    result = die_1.roll() + die_2.roll() + die_3.roll()
    results.append(result)

# Анализ результатов
frequencies = []
max_result = die_1.num_sides + die_2.num_sides + die_3.num_sides
for value in range(3, max_result+1):
    frequency = results.count(value)
    frequencies.append(frequency)


# Визуализация результатов
hist = pygal.Bar()

hist.title = "Results of rolling three D6 dice 1000 times."
hist.x_labels = [str(value) for value in range(3, max_result+1)]
hist.x_title = "Result"
hist.y_title = "Frequency of Result"

hist.add("D6", frequencies)
hist.render_to_file('die_visual.svg')


ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("Die_Test")
app.geometry("500x400")
app.resizable(False, False)

# Заголовок
title_label = ctk.CTkLabel(app, text="Задание основных параметров броска", font=("Arial", 20))
title_label.grid(row=0, column=0, columnspan=2, pady=10, padx=10, sticky="ew")

input_frame = ctk.CTkFrame(app, fg_color="transparent")
input_frame.grid(row=1, column=0, columnspan=2, pady=10, padx=10, sticky="ew")

# Настройка внутри input_frame
# Количество кубиков
dice_label = ctk.CTkLabel(input_frame, text="Количество кубиков:")
dice_label.grid(row=0, column=0, padx=7, pady=5)
dice_entry = ctk.CTkEntry(input_frame, placeholder_text="1-10", width=60)
dice_entry.grid(row=0, column=1, padx=7, pady=5, sticky="w")

# Количество бросков
rolls_label = ctk.CTkLabel(input_frame, text="Количество бросков:")
rolls_label.grid(row=0, column=2, padx=7, pady=5)
rolls_entry = ctk.CTkEntry(input_frame, placeholder_text="1-10000", width=60)
rolls_entry.grid(row=0, column=3, padx=7, pady=5, sticky="w")

# Режим расчёта
calc_mode_label = ctk.CTkLabel(input_frame, text="Calculate mode:")
calc_mode_label.grid(row=1, column=0, padx=7, pady=5, sticky="w")

calc_mode_var = ctk.StringVar(value="sum")
sum_radio = ctk.CTkRadioButton(input_frame, text="Summation", variable=calc_mode_var, value="sum")
sum_radio.grid(row=1, column=1, padx=7, pady=5, sticky="w")

product_radio = ctk.CTkRadioButton(input_frame, text="Composition", variable=calc_mode_var, value="product")
product_radio.grid(row=1, column=2, padx=7, pady=5, sticky="w")

# Тип диаграммы
chart_type_list = ["bar_vertical", "bar_horizontal", "circle", "linear", "pie"]
chart_type_label = ctk.CTkLabel(input_frame, text="Chart type:")
chart_type_label.grid(row=2, column=0, padx=7, pady=10, sticky="w")

chart_type_var = ctk.StringVar(value="bar_vertical")
chart_type_combobox = ctk.CTkComboBox(input_frame, variable=chart_type_var, values=chart_type_list, width=110)
chart_type_combobox.grid(row=2, column=1, padx=7, pady=10, sticky="w")
app.mainloop()


