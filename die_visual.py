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
app.geometry("400x200")
app.resizable()

# Заголовок
title_label = ctk.CTkLabel(app, text="Настройка бросков кубиков", font=("Arial", 20))
title_label.pack(pady=20)

dice_frame = ctk.CTkFrame(app, fg_color="transparent")
dice_frame.pack(pady=5, padx=20, anchor="w", fill="x")
dice_label = ctk.CTkLabel(dice_frame, text="Введите количество кубиков:")
dice_label.pack(side="left", padx=10)
dice_entry = ctk.CTkEntry(dice_frame, placeholder_text="Введите число от 1 до 10")
dice_entry.pack(side="right", padx=10, fill="x", expand=True)

rolls_frame = ctk.CTkFrame(app, fg_color="transparent")
rolls_frame.pack(pady=5, padx=20, anchor="w", fill="x")
rolls_label = ctk.CTkLabel(rolls_frame, text="Количество бросков:")
rolls_label.pack(side="left", padx=10)
rolls_entry = ctk.CTkEntry(rolls_frame, placeholder_text="Введите число от 1 до 10000")
rolls_entry.pack(side="right", padx=10, fill="x", expand=True)


compare_var = ctk.BooleanVar(value=False)
compare_checkbox = ctk.CTkCheckBox(app, text="Сравнение с эталоном", variable=compare_var)
compare_checkbox.pack(side="left", padx=30)

next_button = ctk.CTkButton(app, text="Далее", width=100)
next_button.pack(side="bottom", pady=10)

app.mainloop()


