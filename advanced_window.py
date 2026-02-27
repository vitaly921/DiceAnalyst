import customtkinter as ctk

class AdvancedWindow(ctk.CTkToplevel):
    """Класс для расширенного окна настроек"""
    def __init__(self, parent):
        """Инициализация окна"""
        super().__init__(parent)
        self.parent = parent
        self.title("Advanced settings")
        self.geometry("500x600")
        self.resizable(False, False)

        # Сделать окно модальным
        self.transient(parent)  # Окно будет модальным относительно родителя
        self.grab_set()         # Блокировка родительского окна

        # Список статистических характеристик
        self.stats_options = ["variance", "mean", "mode", "Range", "Confidence interval", "Standard deviation", "Median",
                     "Kurtosis", "Skewness"]
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

        # Подзаголовок для статистических характеристик
        stats_label = ctk.CTkLabel(self, text="Statistical characteristics calculation", font=("Arial", 12),
                                   width=60)
        stats_label.grid(row=1, column=0, padx=10, pady=0, sticky="w")

        # Создание контейнера для прокручиваемого фрейма с чекбоксами статистических характеристик
        container = ctk.CTkFrame(self, fg_color="transparent", height=130, width=450)
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
            checkbox.grid(row=row, column=column, padx=10, pady=7, sticky="w")

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