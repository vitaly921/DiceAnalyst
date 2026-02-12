import customtkinter as ctk
from PIL import Image

from dice_table import DiceTable

class MainWindow(ctk.CTk):
    """Создание главного окна"""
    def __init__(self, count_dices=3, count_rolls=3000):
        super().__init__()

        self.title("Die_Test")
        self.geometry("500x600")
        self.resizable(False, False)

        self.count_dices = count_dices
        self.count_rolls = count_rolls

        self.advanced_window = None

        self._load_images()
        self._create_variables()
        self._build_ui()

    def _load_images(self):
        """Загрузка изображений"""
        self.dice_images = {}
        for sides in range(2, 13):
            img = Image.open(f"images/d{sides}.png")
            self.dice_images[str(sides)] = ctk.CTkImage(img, size=(100, 100))

    def _create_variables(self):
        """Создание переменных"""
        self.calc_mode_var = ctk.StringVar(value="sum")
        self.chart_type_var = ctk.StringVar(value="bar_vertical")
        self.advanced_var = ctk.BooleanVar(value=False)

    def _build_ui(self):
        """Построение интерфейса"""
        self._build_header()
        self._build_input_frame()
        self._build_faces_frame()
        self._build_dice_table()
        self._build_action_buttons()

    def _build_header(self):
        """Построение шапки"""
        # Заголовок окна
        title_label = ctk.CTkLabel(self, text="Setting the basic parameters of a die roll", font=("Arial", 20))
        title_label.grid(row=0, column=0, columnspan=2, pady=10, padx=10, sticky="ew")

    def _build_input_frame(self):
        """Построение фрейма ввода"""
        # Создание фрейма для ввода данных
        input_frame = ctk.CTkFrame(self, fg_color="transparent")
        input_frame.grid(row=1, column=0, columnspan=2, pady=10, padx=10, sticky="ew")

        # Количество кубиков
        dice_label = ctk.CTkLabel(input_frame, text="Number of dice:")
        dice_label.grid(row=0, column=0, padx=7, pady=5)
        self.dice_entry = ctk.CTkEntry(input_frame, placeholder_text="1-10", width=60)
        self.dice_entry.grid(row=0, column=1, padx=7, pady=5, sticky="w")

        # Количество бросков
        rolls_label = ctk.CTkLabel(input_frame, text="Number of dice roll:")
        rolls_label.grid(row=0, column=2, padx=7, pady=5)
        self.rolls_entry = ctk.CTkEntry(input_frame, placeholder_text="1-10000", width=60)
        self.rolls_entry.grid(row=0, column=3, padx=7, pady=5, sticky="w")

        # Режим расчёта
        calc_mode_label = ctk.CTkLabel(input_frame, text="Calculate mode:")
        calc_mode_label.grid(row=1, column=0, padx=7, pady=5, sticky="w")
        # Создание переменной со значением по умолчанию
        self.calc_mode_var = ctk.StringVar(value="sum")
        # Создание радио-кнопок
        sum_radio = ctk.CTkRadioButton(input_frame, text="Summation", variable=self.calc_mode_var, value="sum")
        sum_radio.grid(row=1, column=1, padx=7, pady=5, sticky="w")
        product_radio = ctk.CTkRadioButton(input_frame, text="Composition", variable=self.calc_mode_var, value="product")
        product_radio.grid(row=1, column=2, padx=7, pady=5, sticky="w")

        # Тип диаграммы
        # Список типов диаграмм
        self.chart_type_list = ["bar_vertical", "bar_horizontal", "circle", "linear", "pie"]
        chart_type_label = ctk.CTkLabel(input_frame, text="Chart type:")
        chart_type_label.grid(row=2, column=0, padx=7, pady=10, sticky="w")
        # Тип диаграммы по умолчанию
        self.chart_type_var = ctk.StringVar(value="bar_vertical")
        # Создание выпадающего списка для выбора типа диаграммы
        chart_type_combobox = ctk.CTkComboBox(input_frame, variable=self.chart_type_var, values=self.chart_type_list, width=110)
        chart_type_combobox.grid(row=2, column=1, padx=7, pady=10, sticky="w")

    def _build_faces_frame(self):
        """Построение фрейма граней"""
        # Новый блок с выбором количества граней кубиков
        # Подзаголовок
        faces_header = ctk.CTkLabel(self, text="Select number of sides for each die", font=("Arial", 18))
        faces_header.grid(row=3, column=0, columnspan=2, pady=5, padx=10, sticky="ew")

        # Создание фрейма для виджетов кубиков
        faces_frame = ctk.CTkFrame(self, fg_color="transparent")
        faces_frame.grid(row=4, column=0, columnspan=4, pady=5, padx=10, sticky="w")

        # Переменная для чек-бокса "Uniform sides" со значением True по умолчанию
        self.uniform_faces_var = ctk.BooleanVar(value=True)
        # Чек-бокс для задания одинаковых граней всем кубикам
        unform_check = ctk.CTkCheckBox(faces_frame, text="Uniform sides", variable=self.uniform_faces_var, width=250)
        unform_check.grid(row=0, column=0, padx=7, pady=5, sticky="w")
        # Задание переменной с количеством граней для всех кубиков по умолчанию
        self.sides_var = ctk.StringVar(value="6")
        # Выпадающий список для выбора количества граней всем кубикам
        sides_label = ctk.CTkLabel(faces_frame, text="Number of sides:", width=60)
        sides_label.grid(row=0, column=2, padx=7, pady=5, sticky="w")
        sides_combobox = ctk.CTkComboBox(faces_frame, variable=self.sides_var, values=[str(i) for i in range(2, 13)],
                                         width=60)
        sides_combobox.grid(row=0, column=3, padx=7, pady=5, sticky="e")

    def _build_dice_table(self):
        """Построение таблицы кубиков"""
        self.dice_table = DiceTable(self, self.dice_images)
        self.dice_table.grid(row=5, column=0, columnspan=2, pady=10, padx=10, sticky="ew")
        self.dice_table.build(self.count_dices)

    def _build_action_buttons(self):
        """Построение кнопок действий"""
        # Чек-бокс для расширенных настроек
        self.advanced_check = ctk.CTkCheckBox(self, text="Advanced settings", variable=self.advanced_var,
                                         command=self.on_advanced_toggle)
        self.advanced_check.grid(row=7, column=0, pady=5, padx=18, sticky="w")

        # Кнопка для анализа/расширенных настроек
        self.action_button = ctk.CTkButton(self, text="Analyze", width=100, command=self.on_action_button)
        self.action_button.grid(row=8, column=0, columnspan=2, pady=10, padx=10)

    def on_advanced_toggle(self):
        """Обработчик чек-бокса расширенных настроек"""
        self.action_button.configure(text="Next" if self.advanced_var.get() else "Analyze")

    def on_action_button(self):
        """Обработчик кнопки действия"""
        # Если выбран чек-бокс "Advanced settings", то при нажатии на кнопку открывается окно расширенных настроек
        if self.advanced_var.get():
            self.open_advanced_window()
            # action_button.configure(state="disabled")
            # advanced_check.configure(state="disabled")
        # Если не выбран чек-бокс, то при нажатии кнопки происходит анализ
        else:
            print("Analyze button clicked")

    def open_advanced_window(self):
            """Открытие окна расширенных настроек"""
            if self.advanced_window is None:
                pass
                #self.advanced_window = AdvancedWindow(self)