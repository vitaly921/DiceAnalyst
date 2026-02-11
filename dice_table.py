import customtkinter as ctk
from die_widget import DieWidget

class DiceTable(ctk.CTkFrame):
    """A scrollable frame that contains dice widgets."""
    def __init__(self, parent, dice_images, columns=3, **kwargs):
        """Initialise the DiceTable widget."""
        super().__init__(parent, fg_color= "transparent", **kwargs)

        self.columns = columns
        self.dice_images = dice_images
        self.dice_widgets = []

        self.scroll_frame = ctk.CTkScrollableFrame(self, width=460, height=200)
        self.scroll_frame.grid(row=0, column=0,  sticky="nsew")

        # Каждую колонку с изображениями кубиков растягиваем по ширине
        for col in range(self.columns):
            self.scroll_frame.columnconfigure(col, weight=1)

    def build(self, count):
        # Удаление существующих виджетов
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()
        # Очистка списка виджетов
        self.dice_widgets.clear()

        # Создаем виджеты кубиков
        for i in range(count):
            # Создание экземпляра виджета кубика с количеством граней по умолчанию
            die = DieWidget(self.scroll_frame, self.dice_images)

            # Задание расположения виджета с учетом допустимого количества кубиков в ряду
            row = i // self.columns  # Задание номера ряда
            col = i % self.columns  # Задание номера столбца

            # Размещение виджета кубика в окне
            die.grid(row=row, column=col, padx=5, pady=5, sticky="ew")
            # Добавление виджета в список
            self.dice_widgets.append(die)

