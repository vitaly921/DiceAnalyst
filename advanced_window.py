import customtkinter as ctk

class AdvancedWindow(ctk.CTkToplevel):
    """Класс для расширенного окна настроек"""
    def __init__(self, parent, mode):
        """Инициализация окна"""
        super().__init__(parent)
        self.parent = parent
        self.mode = mode
        self.title("Advanced settings")
        self.geometry("500x600")
        self.resizable(False, False)

        # Сделать окно модальным
        self.transient(parent)  # Окно будет модальным относительно родителя
        self.grab_set()         # Блокировка родительского окна

        # Список статистических характеристик
        self.stats_options = ["Mean", "Most frequent result", "Least frequent result",  "Median", "Range", "Variance", "St deviation", "95% confidence int",
                     "Kurtosis", "Skewness", "Distribution error", "Theoretical mean"]
        # Словарь для хранения переменных состояния чекбоксов
        self.stats_vars = {}

        # Создание интерфейса окна
        self._build_ui()

        # Перехват системного события закрытия окна
        self.protocol("WM_DELETE_WINDOW", self.on_close)

    def _build_ui(self):
        """Создание интерфейса окна"""
        # Растягиваем окно на всю доступную ширину
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # Заголовок окна
        header = ctk.CTkLabel(self, text="Advanced settings", font=("Arial", 20), anchor="center")
        header.grid(row=0, column=0, columnspan=2, pady=10, padx=10, sticky="ew")

        self._build_statistics_frame()      # Создание фреймов для статистических характеристик
        self._build_probability_frame()     # Создание фрейма для вероятностных характеристик

    def _build_statistics_frame(self):
        """Создание фрейма для статистических характеристик"""
        # Подзаголовок для статистических характеристик
        stats_label = ctk.CTkLabel(self, text="Statistical characteristics calculation", font=("Arial", 12),
                                   width=60)
        stats_label.grid(row=1, column=0, padx=10, pady=0, sticky="w")

        # Создание контейнера для прокручиваемого фрейма с чекбоксами статистических характеристик
        container = ctk.CTkFrame(self, fg_color="transparent", height=110, width=450)
        container.grid(row=2, column=0, columnspan=2, pady=0, padx=10, sticky="ew")
        container.grid_propagate(False)

        # Настраиваем grid внутри контейнера
        container.grid_columnconfigure(0, weight=1)
        container.grid_rowconfigure(0, weight=1)

        # Создание прокручиваемого фрейма внутри контейнера
        self.stats_frame = ctk.CTkScrollableFrame(container, corner_radius=10, fg_color="#2b2b2b")
        self.stats_frame.grid(row=0, column=0, sticky="nsew")

        # Создание чекбоксов для статистических характеристик
        self._build_checkboxes(self.stats_frame)

    def _build_checkboxes(self, parent):
        """Создание чекбоксов для статистических характеристик"""
        # Задание количества столбцов для чекбоксов
        columns = 3
        # Создание чекбоксов для каждой статистической характеристики
        for i, name in enumerate(self.stats_options):
            # Создание переменной для текущего чекбокса
            var = ctk.BooleanVar(value=False)
            # Добавление переменной в словарь
            self.stats_vars[name] = var
            # Создание чекбокса для текущей характеристики
            checkbox = ctk.CTkCheckBox(self.stats_frame, text=name, variable=var)

            # Задание позиции чекбокса
            row = i // columns
            column = i % columns
            checkbox.grid(row=row, column=column, padx=8, pady=(5, 0), sticky="w")

    def _build_probability_frame(self):
        """Создание фрейма для вероятностных характеристик"""
        # Подзаголовок для фрейма
        prob_label = ctk.CTkLabel(self, text="Probability analysis", font=("Arial", 12))
        prob_label.grid(row=3, column=0, padx=10, pady=(5,0), sticky="w")

        # Создание фрейма для вероятностных характеристик
        prob_frame = ctk.CTkFrame(self, corner_radius=10 ,fg_color="#2b2b2b")
        prob_frame.grid(row=4, column=0, columnspan=2, padx=10, pady=0, sticky="ew")
        prob_frame.grid_columnconfigure(1, weight=1)

        # Создание полей для ввода вероятностных характеристик
        self.probability_result_var = ctk.StringVar()
        probability_result_label = ctk.CTkLabel(prob_frame, text="Probability of specific result: ")
        probability_result_label.grid(row=0, column=0, padx=10, pady=(5,0), sticky="w")
        self.probability_result_entry = ctk.CTkEntry(prob_frame, width=60, textvariable=self.probability_result_var)
        self.probability_result_entry.grid(row=0, column=1, padx=10, pady=(5,0), sticky="w")

        # Создание подписи и поля для ввода числа для текущей вероятностной характеристики
        self.exact_value_var = ctk.StringVar()

        # Проверка режима (сумма или произведение) и изменение надписи
        if self.mode.get() == "sum":
            exact_label = ctk.CTkLabel(prob_frame, text="Probability of the specified sum: ")
        else:
            exact_label = ctk.CTkLabel(prob_frame, text="Probability of the specified product: ")
        exact_label.grid(row=1, column=0, padx=10, pady=(5,0), sticky="w")

        # Создание поля для ввода конкретной суммы или произведения
        self.exact_entry =ctk.CTkEntry(prob_frame, width=60, textvariable=self.exact_value_var)
        self.exact_entry.grid(row=1, column=1, padx=10, pady=(5,0), sticky="w")

        # Создание подписи и поля для ввода числа для текущей вероятностной характеристики
        self.compare_value_var = ctk.StringVar()
        compare_label = ctk.CTkLabel(prob_frame, text="The probability of a number falling out is greater / less than: ")
        compare_label.grid(row=2, column=0, padx=10, pady=(5,0), sticky="w")
        # Создание поля для ввода конкретного числа
        self.compare_entry = ctk.CTkEntry(prob_frame, width=60, textvariable=self.compare_value_var)
        self.compare_entry.grid(row=2, column=1, padx=10, pady=(5,5), sticky="w")

    def get_selected_stats(self):
        """Возвращает список выбранных статистических характеристик"""
        return [name for name, var in self.stats_vars.items() if var.get()]

    def on_close(self):
        """Обработчик закрытия окна"""
        # Разблокировка родительского окна
        self.grab_release()
        # Закрытие окна расширенных настроек
        self.destroy()
        # Очистка ссылки на окно расширенных настроек в родительском окне
        self.parent.advanced_window = None