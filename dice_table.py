import customtkinter as ctk
from die_widget import DieWidget

class DiceTable(ctk.CTkFrame):
    """Класс для создания прокручиваемого фрейма с виджетами кубиков"""
    def __init__(self, parent, dice_images, columns=3, **kwargs):
        """Инициализация класса"""
        super().__init__(parent, fg_color= "transparent", **kwargs)
        # Сохранение переданных параметров
        self.columns = columns
        self.dice_images = dice_images

        # Создание пустого списка для хранения виджетов кубиков
        self.dice_widgets = []

        # Создание прокручиваемого фрейма (контейнера) для хранения виджетов кубиков
        self.scroll_frame = ctk.CTkScrollableFrame(self, width=460, height=200)
        self.scroll_frame.grid(row=0, column=0,  sticky="nsew")

        # Каждую колонку с изображениями кубиков растягиваем по ширине контейнера
        for col in range(self.columns):
            self.scroll_frame.columnconfigure(col, weight=1)

    def build(self, count):
        """Создание виджетов кубиков внутри прокручиваемого фрейма"""
        # Удаление существующих виджетов
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()
        # Очистка списка виджетов
        self.dice_widgets.clear()

        # Создание и размещение заданного количества виджетов кубиков
        for i in range(count):
            # Создание экземпляра виджета кубика с количеством граней по умолчанию
            die = DieWidget(self.scroll_frame, self.dice_images)

            # Задание расположения виджета с учетом допустимого количества кубиков в ряду
            row = i // self.columns     # Задание номера ряда
            col = i % self.columns      # Задание номера столбца

            # Размещение виджета кубика в контейнере
            die.grid(row=row, column=col, padx=5, pady=5, sticky="ew")
            # Добавление виджета в список
            self.dice_widgets.append(die)

