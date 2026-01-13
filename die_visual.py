import pygal
import customtkinter as ctk
from PIL import Image
from die import Die
from dice_widget import DieWidget

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
app.geometry("500x600")
app.resizable(False, False)

# Загрузка изображений кубиков
dice_images = {}
for sides in range(2, 13):
    img = Image.open(f"images/d{sides}.png")
    dice_images[str(sides)] = ctk.CTkImage(img, size=(100, 100))

# Список виджетов кубиков
dice_widgets = []

def build_dice_widgets(count):
    """Создание виджетов кубиков в определенном порядке"""
    for w in dice_scroll_frame.winfo_children():
        w.destroy()
    dice_widgets.clear()
    columns = 3

    for col in range(columns):
        dice_scroll_frame.grid_columnconfigure(col, weight=1)

    for i in range(count):
        die = DieWidget(dice_scroll_frame, dice_images)

        row = i // columns
        col = i % columns

        die.grid(row=row, column=col, padx=5, pady=5, sticky="ew")
        dice_widgets.append(die)

# Заголовок
title_label = ctk.CTkLabel(app, text="Setting the basic parameters of a die roll", font=("Arial", 20))
title_label.grid(row=0, column=0, columnspan=2, pady=10, padx=10, sticky="ew")

input_frame = ctk.CTkFrame(app, fg_color="transparent")
input_frame.grid(row=1, column=0, columnspan=2, pady=10, padx=10, sticky="ew")

# Настройка внутри input_frame
# Количество кубиков
dice_label = ctk.CTkLabel(input_frame, text="Number of dice:")
dice_label.grid(row=0, column=0, padx=7, pady=5)
dice_entry = ctk.CTkEntry(input_frame, placeholder_text="1-10", width=60)
dice_entry.grid(row=0, column=1, padx=7, pady=5, sticky="w")

# Количество бросков
rolls_label = ctk.CTkLabel(input_frame, text="Number of dice roll:")
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


# Новый блок с выбором количества граней кубиков
# Подзаголовок
faces_header = ctk.CTkLabel(app, text="Select number of sides for each die", font=("Arial", 18))
faces_header.grid(row=3, column=0, columnspan=2, pady=5, padx=10, sticky="ew")

faces_frame = ctk.CTkFrame(app, fg_color="transparent")
faces_frame.grid(row=4, column=0, columnspan=4, pady=5, padx=10, sticky="w")

uniform_faces_var = ctk.BooleanVar(value=True)

unform_check = ctk.CTkCheckBox(faces_frame, text="Uniform sides", variable=uniform_faces_var, width=250)
unform_check.grid(row=0, column=0, padx=7, pady=5, sticky="w")

sides_var = ctk.StringVar(value="6")
sides_label = ctk.CTkLabel(faces_frame, text="Number of sides:", width=60)
sides_label.grid(row=0, column=2, padx=7, pady=5, sticky="w")
sides_combobox = ctk.CTkComboBox(faces_frame, variable=sides_var,values=[str(i) for i in range(2, 13)], width=60)
sides_combobox.grid(row=0, column=3, padx=7, pady=5, sticky="e")

# Блок с виджетами кубиков
dice_table_container = ctk.CTkFrame(app, border_width=1, fg_color="transparent")
dice_table_container.grid(row=5, column=0, columnspan=2, pady=10, padx=10, sticky="ew")

dice_scroll_frame = ctk.CTkScrollableFrame(dice_table_container, width=460, height=200)
dice_scroll_frame.grid(row=6, column=0, columnspan=2, sticky="ew")

build_dice_widgets(5)

advanced_window = None



def on_advanced_toggle():
    """Обработчик переключения чек-бокса"""
    if advanced_var.get():
        action_button.configure(text="Next")
    else:
        action_button.configure(text="Analyze")

# Чек-бокс для расширенных настроек
advanced_var = ctk.BooleanVar(value=False)
advanced_check = ctk.CTkCheckBox(app, text="Advanced settings", variable=advanced_var, command=on_advanced_toggle)
advanced_check.grid(row=7, column=0, pady=5, padx=18, sticky="w")

def on_action_button():
    """Обработчик нажатия кнопки"""
    if advanced_var.get():
        open_advanced_window()
        #action_button.configure(state="disabled")
        #advanced_check.configure(state="disabled")
    else:
        print("Analyze button clicked")

# Кнопка для анализа по умолчанию
action_button = ctk.CTkButton(app, text="Analyze", width=100, command=on_action_button)
action_button.grid(row=8, column=0, columnspan=2, pady=10, padx=10)


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


