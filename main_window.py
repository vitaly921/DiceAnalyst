import customtkinter as ctk
from PIL import Image


class MainWindow(ctk.CTk):
    """Создание главного окна"""
    def __init__(self):
        super().__init__()

        self.title("Die_Test")
        self.geometry("500x600")
        self.resizable(False, False)

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
        self._build_dice_table()
        self._build_action_buttons()
