# tkinter and picture imports
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
# application classes
from Components.SearchBar import SearchBar


class MainApplication(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Isaacs Weather Application")
        self.geometry("1039x700")
        self.configure(bg="#000000")

        self.style = ttk.Style()
        self.style.theme_use("default")

        self.notebook = ttk.Notebook(self, style="Custom.TNotebook")
        self.notebook.pack(fill=tk.BOTH, expand=True)

        self.screen1 = tk.Frame(self.notebook, bg="black", padx=0, pady=0)
        self.screen2 = tk.Frame(self.notebook, bg="black")

        self.notebook.add(self.screen1, text="Weather")
        self.notebook.add(self.screen2, text="Crime")

        self.modify_weather_screen()
        self.modify_screen2()

    def modify_weather_screen(self):
        """
            Modify the content of Screen 1.
        """
        search_bar = SearchBar(self.screen1)
        search_bar.pack(padx=0, pady=0)

    def modify_screen2(self):
        """
            Modify the content of Screen 2.
        """
        label2 = tk.Label(self.screen2, text="Crime", bg="#000000", fg="#FFFFFF")
        label2.pack(pady=20)


if __name__ == "__main__":
    app = MainApplication()
    app.mainloop()
