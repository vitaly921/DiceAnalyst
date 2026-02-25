import customtkinter as ctk

class AdvancedWindow(ctk.CTkToplevel):
    """Advanced window class."""
    def __init__(self, parent):
        """"""
        super().__init__(parent)
        self.title("Advanced settings")
        self.geometry("500x600")
        self.resizable(False, False)
        self.grab_set()