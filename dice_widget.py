import customtkinter as ctk

class DieWidget(ctk.CTkFrame):
    """A widget for displaying a die"""
    def __init__(self, parent, dice_images, sides="6"):
        super().__init__(parent, corner_radius=10, width=140, height=170)
        self.grid_propagate(False)

        self.dice_images = dice_images
        self.sides_var = ctk.StringVar(value=sides)

        self.image_label = ctk.CTkLabel(self, image=dice_images[sides], text='')
        self.image_label.pack(pady=(8,4))

        self.sides_box = ctk.CTkComboBox(self, values=[str(i) for i in range(2, 13)], variable=self.sides_var, width=70, command=self._on_sides_change)
        self.sides_box.pack(pady=(0,8))

    def _on_sides_change(self, value):
        """Callback for when the sides are changed"""
        self.image_label.configure(image=self.dice_images[value])

    def get_sides(self):
        return int(self.sides_var.get())