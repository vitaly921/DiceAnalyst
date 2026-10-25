import customtkinter as ctk
from pathlib import Path
from PIL import Image
from customtkinter import CTkLabel
from charts_types import CHARTS_TYPES, CHART_PREVIEW_IMAGES


class AdvancedWindow(ctk.CTkToplevel):
    """Класс для расширенного окна настроек"""
    def __init__(self, parent, mode):
        """Инициализация окна"""
        super().__init__(parent)
        self.main_chart_type = None
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
        self._build_chart_frame()           # Создание фрейма с выбором диаграмм


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

    def get_selected_stats(self):
        """Возвращает список выбранных статистических характеристик"""
        return [name for name, var in self.stats_vars.items() if var.get()]

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

    def _build_chart_frame(self):
        """Создание фрейма с диаграммами"""
        # Подзаголовок для фрейма
        chart_label = ctk.CTkLabel(self, text="Chart selection", font=("Arial", 12))
        chart_label.grid(row=5, column=0, padx=10, pady=(5, 0), sticky='w')
        # Создание фрейма для диаграмм
        chart_frame = ctk.CTkFrame(self, corner_radius=10)
        chart_frame.grid(row=6, column=0, columnspan=2, padx=10, pady=0, sticky='ew')
        chart_frame.grid_columnconfigure(1, weight=1)

        # Список доступных типов диаграмм
        self.chart_types = CHARTS_TYPES
        # Текущий индекс выбранной диаграммы
        self.current_chart_index = 0

        # Словарь для хранения состояний (выбрана или нет) каждой из диаграмм
        self.chart_selected = {chart: False for chart in self.chart_types}

        # Тип основного графика из главного окна
        self.main_chart_type = None

        # Название для текущей диаграммы
        self.chart_title_label = CTkLabel(chart_frame, text="")
        self.chart_title_label.grid(row=0, column=0, columnspan=3, pady=5)

        # Кнопки для переключения диаграмм
        prev_button = ctk.CTkButton(chart_frame, text="<",font=('Arial',32),width=60, height=120, command=self._prev_chart)
        prev_button.grid(row=1, column=0, padx=5, pady=5, sticky="w")
        next_button = ctk.CTkButton(chart_frame, text=">", font=('Arial',32), width=60, height=120, command=self._next_chart)
        next_button.grid(row=1, column=2, padx=5, pady=5, sticky="w")

        # Предварительный просмотр (сейчас текст)
        self.chart_preview = ctk.CTkLabel(chart_frame, text="Chart preview", width=200, height=120)
        self.chart_preview.grid(row=1, column=1, padx=10, pady=5, sticky="w")

        # Состояние чек-бокса выбора текущей диаграммы (есть у всех диаграмм)
        self.chart_selected_var = ctk.BooleanVar(value=False)
        self.selected_checkbox = ctk.CTkCheckBox(chart_frame, text="Use this chart", variable=self.chart_selected_var,
                                                 command=self._save_current_chart_selection)
        self.selected_checkbox.grid(row=2, column=0, padx=10, pady=5, sticky="w")

        self._update_chart_view()


    def _update_chart_view(self):
        """Обновление интерфейса с диграммами"""
        # Выбор текущей диаграммы
        chart_name = self.chart_types[self.current_chart_index]
        # Получение пути к изображению выбранной диаграммы
        image_path = CHART_PREVIEW_IMAGES.get(chart_name)

        # Подсчет общего количества диаграмм
        total =  len(self.chart_types)

        # Отрисовка названия диаграммы и её позиции
        self.chart_title_label.configure(text=f"{chart_name} ({self.current_chart_index + 1}/{total})")

        # Отрисовка предварительного просмотра изображения диаграмм
        # Если существует путь к выбранной диаграмме и файл по данному пути
        if image_path and Path(image_path).is_file():
            # Получение изображения по данному пути и сохранение его копии в превью
            with Image.open(image_path) as image:
                preview = image.copy()
            # Отрисовка превью и задание для него параметров
            self.chart_preview_image = ctk.CTkImage(light_image=preview, dark_image=preview, size=(220, 120))
            self.chart_preview.configure(image=self.chart_preview_image, text="")
        # Если путь или файл диаграммы недоступны
        else:
            # Отрисовка вместо превью текста об этом
            self.chart_preview.configure(image=None, text="Предпросмотр недоступен")

        # Превью в виде заглушки - текста
        #self.chart_preview.configure(text=chart_name)

        # Если текущая диаграмма является основной, блокируем чекбокс в состоянии True
        if chart_name == self.main_chart_type:
            self.chart_selected[chart_name] = True
            self.selected_checkbox.configure(state='disabled')
        else:
            # Если диаграмма не является основной, чек-бокс не блокируется и в любом состоянии
            #self.chart_selected_var.set(False)
            self.selected_checkbox.configure(state ='normal')

        # Для чекбокса выбранной диаграммы установить значение из словаря состояний
        self.chart_selected_var.set(self.chart_selected[chart_name])



    def _save_current_chart_selection(self):
        """Сохранение текущего состояния диаграмм в словаре состояний"""
        chart_name = self.chart_types[self.current_chart_index]
        # Если диаграмма является основной (выбрана на главном окне)
        if chart_name == self.main_chart_type:
            # В словарь состояний для главной диаграммы добавляем True (выбрана всегда)
            self.chart_selected[chart_name] = True
        else:
            # Для остальных диаграмм сохраняем текущее состояние чекбокса
            self.chart_selected[chart_name] = self.chart_selected_var.get()


    def _next_chart(self):
        """Переключение к следующей диаграмме"""
        # Сохранение состояния диаграмм
        self._save_current_chart_selection()
        # Если индекс диаграммы не максимальный, то происходит переход к следующей
        if self.current_chart_index < len(self.chart_types) - 1:
            self.current_chart_index += 1
        # Иначе возврат в начало списка
        else:
            self.current_chart_index = 0
        # Обновление интерфейса с диаграммой
        self._update_chart_view()

    def _prev_chart(self):
        """Переключение к предыдущей диаграмме"""
        # Сохранение состояния диаграмм
        self._save_current_chart_selection()
        # Если индекс диаграммы больше нуля, то можно перейти к предыдущей диаграмме
        if self.current_chart_index > 0:
            self.current_chart_index -= 1
        # Иначе возврат в конец списка
        else:
            self.current_chart_index = len(self.chart_types) - 1
        # Обновление интерфейса с диаграммой
        self._update_chart_view()


    def set_main_chart(self, chart_type):
        """Определение основной диаграммы"""
        # Проверка есть ли переданный тип диаграммы в списке диаграмм
        if chart_type not in self.chart_types:
            return
        # Переданная диаграмма обозначается основной
        self.main_chart_type = chart_type
        # Добавление главной диграммы в словарь и установка состояния True
        self.chart_selected[chart_type] = True
        # Получение индекса главной диаграммы
        self.current_chart_index = self.chart_types.index(chart_type)
        self._update_chart_view()
        print(self.current_chart_index)

    def get_selected_charts(self):
        """Возвращает список выбранных диаграмм"""
        self._save_current_chart_selection()
        # В словаре состояний диграмм выбираем выбранные пользователем
        return [chart for chart, selected in self.chart_selected.items() if selected]

    def on_close(self):
        """Обработчик закрытия окна"""
        # Разблокировка родительского окна
        self.grab_release()
        # Закрытие окна расширенных настроек
        self.destroy()
        # Очистка ссылки на окно расширенных настроек в родительском окне
        self.parent.advanced_window = None