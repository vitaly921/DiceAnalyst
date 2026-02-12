import customtkinter as ctk

class DieWidget(ctk.CTkFrame):
    """Класс виджета для отображения кубика"""
    def __init__(self, parent, dice_images, sides="6"):
        # Инициализация базового класса CTkFrame
        # Установка радиуса углов и размеров виджета
        super().__init__(parent, corner_radius=10, width=140, height=170)
        # Установка фиксированного размера виджета
        self.grid_propagate(False)
        # Сохранение изображений кубиков
        self.dice_images = dice_images
        # Сохранение переданного значения количества граней
        self.sides_var = ctk.StringVar(value=sides)
        # Добавление изображения кубика в виджет с заданным количеством граней
        self.image_label = ctk.CTkLabel(self, image=dice_images[sides], text='')
        self.image_label.pack(pady=(8,4))
        # Добавление выпадающего списка для изменения количества граней
        self.sides_box = ctk.CTkComboBox(self, values=[str(i) for i in range(2, 13)], variable=self.sides_var, width=70, command=self._on_sides_change)
        self.sides_box.pack(pady=(0,8))

    def _on_sides_change(self, value):
        """Обработчик изменения количества граней"""
        # Обновление изображения кубика с новым количеством граней
        self.image_label.configure(image=self.dice_images[value])

    def get_sides(self):
        """Получение текущего количества граней"""
        return int(self.sides_var.get())