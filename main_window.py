import customtkinter as ctk
from PIL import Image
from advanced_window import AdvancedWindow

from dice_table import DiceTable

class MainWindow(ctk.CTk):
    """Создание главного окна"""
    def __init__(self, count_dices=3, count_rolls=3000):
        super().__init__()
        # Заголовок окна
        self.title("Die_Test")
        # Размеры окна
        self.geometry("500x600")
        # Запрет изменения размеров окна
        self.resizable(False, False)
        # Сохранение количества кубиков и бросков
        self.count_dices = count_dices
        self.count_rolls = count_rolls
        # Создание булевой переменной для перехода в расширенное окно настроек со значением False (окно не открыто)
        self.advanced_window = None

        # Инициализация ключевых методов окна
        self._load_images()
        self._create_variables()
        self._build_ui()

    def _load_images(self):
        """Загрузка всех изображений кубиков"""
        self.dice_images = {}
        # Для изображений с гранями в заданном диапазоне
        for sides in range(2, 13):
            # Открытие изображения с текущими гранями
            img = Image.open(f"images/dice/d{sides}.png")
            # Сохранение изображения с текущими гранями размером 100x100
            self.dice_images[str(sides)] = ctk.CTkImage(img, size=(100, 100))

    def _create_variables(self):
        """Создание переменных для интерфейса главного окна"""
        # Создание переменной режима расчёта (по умолчанию - суммирование)
        self.calc_mode_var = ctk.StringVar(value="sum")
        # Создание переменной типа диаграммы (по умолчанию - вертикальная диаграмма)
        self.chart_type_var = ctk.StringVar(value="bar_vertical")
        # Создание булевой переменной для перехода в расширенное окно настроек (по умолчанию - False)
        self.advanced_var = ctk.BooleanVar(value=False)

    def _build_ui(self):
        """Построение интерфейса главного окна с помощью UI методов"""
        # Метод для создания шапки главного окна
        self._build_header()
        # Метод для создания фрейма ввода основных параметров броска
        self._build_input_frame()
        # Метод для создания фрейма с выбором количества граней для всех кубиков
        self._build_faces_frame()
        # Метод для создания таблицы изображений кубиков с выбором граней для каждого кубика
        self._build_dice_table()
        # Метод для создания кнопок перехода в расширенное окно настроек или начала броска
        self._build_action_buttons()

    def _build_header(self):
        """Создание шапки главного окна"""
        # Заголовок окна
        title_label = ctk.CTkLabel(self, text="Setting the basic parameters of a die roll", font=("Arial", 20))
        title_label.grid(row=0, column=0, columnspan=2, pady=10, padx=10, sticky="ew")

    def _build_input_frame(self):
        """Создание фрейма для ввода основных параметров броска"""
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
        """Создание фрейма с выбором граней для всех кубиков"""
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
        uniform_check = ctk.CTkCheckBox(faces_frame, text="Uniform sides", variable=self.uniform_faces_var,
                                       command=self._on_uniform_toggle, width=250)
        uniform_check.grid(row=0, column=0, padx=7, pady=5, sticky="w")

        # Задание переменной с количеством граней для всех кубиков по умолчанию
        self.sides_var = ctk.StringVar(value="6")
        # Выпадающий список для выбора количества граней всем кубикам
        self.sides_label = ctk.CTkLabel(faces_frame, text="Number of sides:", width=60)
        self.sides_label.grid(row=0, column=2, padx=7, pady=5, sticky="w")
        self.sides_combobox = ctk.CTkComboBox(faces_frame, variable=self.sides_var, values=[str(i) for i in range(2, 13)],
                                         width=60, state="normal", command=self._on_sides_change)
        self.sides_combobox.grid(row=0, column=3, padx=7, pady=5, sticky="e")

    def _build_dice_table(self):
        """Построение таблицы изображений кубиков"""
        # Создание объекта включающего в себя контейнер со скроллингом и с таблицей изображений кубиков
        self.dice_table = DiceTable(self, self.dice_images)
        # Задание расположения объекта-контейнера
        self.dice_table.grid(row=5, column=0, columnspan=2, pady=10, padx=10, sticky="ew")
        # Построение таблицы изображений кубиков в объекте-контейнере
        self.dice_table.build(self.count_dices)

    def _build_action_buttons(self):
        """Построение кнопок действий в конце окна"""
        # Чек-бокс для выбора окна расширенных настроек
        self.advanced_check = ctk.CTkCheckBox(self, text="Advanced settings", variable=self.advanced_var,
                                         command=self.on_advanced_toggle)
        # Задание расположения чек-бокса
        self.advanced_check.grid(row=7, column=0, pady=5, padx=18, sticky="w")

        # Кнопка для начала анализа/расширенных настроек (в зависимости от чек-бокса)
        self.action_button = ctk.CTkButton(self, text="Analyze", width=100, command=self.on_action_button)
        # Задание расположения кнопки
        self.action_button.grid(row=8, column=0, columnspan=2, pady=10, padx=10)

    def on_advanced_toggle(self):
        """Обработчик чек-бокса расширенных настроек"""
        # Если чек-бокс выбран, то кнопка меняет текст на "Next", иначе текст на кнопке - "Analyze"
        self.action_button.configure(text="Next" if self.advanced_var.get() else "Analyze")

    def on_action_button(self):
        """Обработчик кнопки действия в зависимости от чек-бокса"""
        # Если чек-бокс выбран, то при нажатии на кнопку "Next" открывается окно расширенных настроек
        if self.advanced_var.get():
            # Вызов функции открытия окна расширенных настроек
            self.open_advanced_window()
            # action_button.configure(state="disabled")
            # advanced_check.configure(state="disabled")

        # Если чек-бокс не отмечен, то при нажатии кнопки "Analyze" начинается анализ бросков
        else:
            print("Analyze button clicked")

    def _on_uniform_toggle(self):
        """Обработчик чек-бокса "Uniform sides"""
        # Сохранение состояния чек-бокса для изменения количества граней всех кубиков одновременно
        is_uniform = self.uniform_faces_var.get()
        # Изменение состояния выпадающего списка (включено/выключено) в зависимости от состояния чек-бокса
        self.sides_combobox.configure(state="normal" if is_uniform else "disabled")
        self.sides_label.configure(state="normal" if is_uniform else "disabled")

        # Изменение состояния выпадающего списка каждого кубика в зависимости от состояния чек-бокса
        for dice_widget in self.dice_table.dice_widgets:
            # Если чек-бокс выбран, то выпадающий список каждого кубика выключен, иначе - включен
            dice_widget.sides_box.configure(state="disabled" if is_uniform else "normal")
        # Если чек-бокс выбран, то вызывается функция изменения количества граней всех кубиков одновременно
        if is_uniform:
            self._on_sides_change(self.sides_var.get())

    def _on_sides_change(self, value):
        """Обработчик изменения количества граней кубиков"""
        if not hasattr(self, "dice_table"):
            return
        # Сохранение нового количества граней при выборе чек-бокса "Uniform sides"
        new_sides = self.sides_var.get()
        # Изменение количества граней каждого кубика
        for dice_widget in self.dice_table.dice_widgets:
            dice_widget.sides_var.set(new_sides)


    def open_advanced_window(self):
            """Открытие окна расширенных настроек"""
            if self.advanced_window is None:
                self.advanced_window = AdvancedWindow(self, self.calc_mode_var)