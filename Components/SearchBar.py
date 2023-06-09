import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from scripts.valid_cities import get_valid_cities
from scripts.get_weather import get_weather


# colors 
BLUE_GREEN = '#08B6CE'
RED_STONE = "#e46b71"
BALTIC_SEA = "#3A3B3C"

class SearchBar(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.configure(bg="")
        self.style = ttk.Style()  # Define the style attribute
        self.style.configure("Custom.TFrame", bordercolor="white", relief="flat", background="white")

        self.parent = parent

        # Entry Frame
        self.entry_frame = tk.Frame(self, bg="gray")
        self.entry_frame.pack(side=tk.TOP, anchor='w', pady=(0, 0))
        self.configure_search_entry()

        # Suggestion Frame
        self.suggestion_frame = tk.Frame(self, bg="", width=50, padx=0, pady=0)
        self.configure_listbox()  # Add this line to initialize the listbox


    def configure_search_entry(self):
        """
            Configure the search entry widget.

            Search entry box is where the user types into the search bar field.
        """
        # Style for the search entry
        self.style.configure(
            "Custom.TEntry",
            fieldbackground=BALTIC_SEA,
            foreground="white",
            borderwidth=1,
            relief="flat",
            width=30,
            insertcolor="white",
            selectforeground="white",
            highlightthickness=0,
        )
        self.style.map(
            "Custom.TEntry",
            bordercolor=[("focus", "#3A3B3C")],
            relief=[("focus", "flat")],
            selectbackground=[("focus", "dark blue"), ("!focus", "light blue")],
        )
        self.style.configure(
            "CustomButton1.TButton",
            background=BLUE_GREEN,
            font=("Arial", 15, "bold")
        )
        self.style.configure(
            "CustomButton2.TButton",
            background=RED_STONE,
            font=("Arial", 15, "bold")
        )
        self.style.configure(
            "Custom_search_button.TButton",
            background=BALTIC_SEA,
            relief="flat",
        )
        self.style.map(
            "Custom_search_button.TButton",
            background=[('hover', BALTIC_SEA)],
        )

        self.default_text = "Search for a city"

        # Default text and cloud image
        self.load_and_resize_cloud()
        self.image_label.pack(side=tk.LEFT, padx=(10, 5), pady=(5, 5))

        # Search Bar Frame
        self.search_bar_frame = tk.Frame(self.entry_frame, bg="#3A3B3C")
        self.search_bar_frame.pack(side=tk.LEFT, anchor='w', pady=(0, 0), padx=(0, 5))

        # Search Entry
        self.search_entry = ttk.Entry(self.search_bar_frame, style="Custom.TEntry")
        self.search_entry.pack(side=tk.LEFT, padx=(1, 5), pady=(5, 0))
        self.search_entry.configure(width=57, font=("Arial", 24))
        self.search_entry.insert(0, self.default_text)

        # Search Button
        search_image = Image.open("Images/search.png").resize((20, 20))
        self.search_photo = ImageTk.PhotoImage(search_image)
        search_button = ttk.Button(
            self.search_bar_frame,
            image=self.search_photo, 
            command=self.on_search_button, 
            style="Custom_search_button.TButton",
        )
        self.style.configure("Custom.TButton", padding=(0, 0))
        search_button.pack(side=tk.LEFT, 
                           pady=(5, 5), 
                           padx=(0, 5))

        # Celsius Button
        celsius_button = ttk.Button(
            self.entry_frame,
            text="°C",
            command=self.switch_to_celsius,
            style="CustomButton1.TButton",
            padding=8,
            width=3,
        )
        celsius_button.pack(side=tk.LEFT, 
                            pady=(5, 5), 
                            padx=(0, 5))
        # Fahrenheit Button
        fahrenheit_button = ttk.Button(
            self.entry_frame,
            text="°F",
            command=self.switch_to_fahrenheit,
            padding=8,
            width=3,
            style="CustomButton2.TButton",
        )
        fahrenheit_button.pack(side=tk.LEFT,
                                pady=(5, 5),
                                padx=(0, 5))

        # Bind events
        self.search_entry.bind("<FocusIn>", self.on_entry_focus_in)
        self.search_entry.bind("<FocusOut>", self.on_entry_focus_out)
        self.search_entry.bind("<Return>", self.on_return_key)
        self.search_entry.bind("<KeyRelease>", self.check_listbox)

    def configure_listbox(self):
        """
            Configure the listbox widget.

            Listbox is a list of cities that the user may type in searchbar. The list contains very few cities so far, but
            the user may type any valid city and try to see if there is a weather API for that city.
        """
        if hasattr(self, "listbox"):
            self.listbox.destroy()

        self.listbox = tk.Listbox(
            self.suggestion_frame, 
            bg="#3A3B3C", 
            fg="white", 
            font=("Arial", 22), 
            width=62, 
            borderwidth=0, 
            height=3
        )
        self.listbox.pack(pady=0, side=tk.LEFT, padx=(80, 0))

        self.cities = get_valid_cities()
        self.cities.sort()
        self.update_listbox(self.cities)
        self.listbox.bind("<<ListboxSelect>>", self.fillout)
    
    def switch_to_celsius(self):
        pass

    def switch_to_fahrenheit(self):
        pass

    def fillout(self, e):
        """
            Allows us to click on cities in listbox and fill out search bar
        """
        self.search_entry.delete(0, tk.END)
        selected_item = self.listbox.get(self.listbox.curselection())
        self.search_entry.insert(0, selected_item.strip())

        search_query = self.search_entry.get()
        if (
            search_query.lower() != self.default_text.lower()
            and search_query.lower() != ""
        ):
            result = get_weather(search_query)
            if result:
                print(result)
            else:
                print("City weather not found")
                self.city_not_found()

        self.focus_set()

    def update_listbox(self, cities):
        """
            Updates listbox with passed in cities
        """
        self.listbox.delete(0, tk.END)
        for city in cities:
            padding = ""
            self.listbox.insert(tk.END, padding + city)

    def check_listbox(self, e):
        """
            updates listbox with cities that have the characters user has typed.
        """
        user_typed = self.search_entry.get()
        if user_typed == "":
            data = self.cities
        else:
            data = []
            for city in self.cities:
                if city.lower().startswith(user_typed.lower()):
                    data.append(city)
        self.update_listbox(data)

    def load_and_resize_cloud(self):
        """
            Load and resize the image for the search bar.
        """
        style = ttk.Style()
        style.configure("Custom.TLabel", relief="solid", bordercolor="light gray")

        image = Image.open("Images/cloud.png").resize((65, 39))
        photo = ImageTk.PhotoImage(image)
        self.image_label = ttk.Label(
            self.entry_frame,
            image=photo, 
            background="dark blue", 
            style="Custom.TLabel", 
            borderwidth=0
        )
        self.image_label.image = photo
        self.image_label.pack(padx=(5, 0))

    def on_entry_focus_in(self, event):
        """
            Handle the focus in event of the search entry.
        """
        if self.search_entry.get() == self.default_text:
            self.search_entry.configure(foreground="#FFFFFF")
            self.search_entry.delete(0, tk.END)
        
        self.suggestion_frame.pack(pady=(0, 5), anchor="w", padx=0)

        self.configure_listbox()

        self.style.configure("Custom.TLabel", bordercolor="#3A3B3C", relief="solid")
        self.image_label.configure(style="Custom.TLabel")

        if hasattr(self, "error_frame"):
            self.error_frame.destroy()
        

    def on_entry_focus_out(self, event):
        """
            Handle the focus out event of the search entry.
        """
        if not self.search_entry.get():
            self.search_entry.configure(foreground="#B0B3B8")
            self.search_entry.insert(0, self.default_text)

        self.suggestion_frame.pack_forget()

        style = ttk.Style()
        style.configure("Custom.TLabel", bordercolor="#3A3B3C", relief="solid")
        self.image_label.configure(style="Custom.TLabel")

    def on_return_key(self, event):
        """
            Handle the return key event of the search entry.
        """
        search_query = self.search_entry.get()
        if (
            search_query.lower() != self.default_text.lower()
            and search_query.lower() != ""
        ):
            result = get_weather(search_query)
            if result:
                print(result)
            else:
                print("City weather not found")
                self.city_not_found()

        self.focus_set()

    def on_search_button(self):
        """
            Handle the click event of the search button.
        """
        search_query = self.search_entry.get()
        if (
            search_query.lower() != self.default_text.lower()
            and search_query.lower() != ""
        ):
            result = get_weather(search_query)
            if result:
                print(result)
            else:
                print("City weather not found")
                self.city_not_found()

        self.focus_set()

    def city_not_found(self):
        """
            Display an error message when city weather is not found.
        """
        if hasattr(self, "error_frame"):
            self.error_frame.destroy()

        self.error_frame = ttk.Frame(self.parent, style="Custom.TFrame")
        self.error_frame.pack(pady=(30, 0), padx=(250, 0))

        self.add_sad_cloud()

        error_label = ttk.Label(
            self.error_frame,
            text="City weather not found.",
            background="black",
            foreground="light gray",
            borderwidth=0, 
            relief="flat",
            font=("Arial", 22, "bold")
        )
        error_label.pack()

    def add_sad_cloud(self):
        """
            Load and resize the image for the search bar.
        """
        style = ttk.Style()
        style.configure("Custom.TLabel", relief="flat", borderwidth=0, background="black")

        image = Image.open("Images/sadcloudsprite.png").resize((420, 300))
        photo = ImageTk.PhotoImage(image)

        if hasattr(self.error_frame, "image_label"):
            self.error_frame.image_label.destroy()

        self.error_frame.image_label = ttk.Label(self.error_frame, image=photo, style="Custom.TLabel")
        self.error_frame.image_label.image = photo
        self.error_frame.image_label.pack()

# Define the custom style after the SearchBar class definition


def main():
    root = tk.Tk()
    root.title("Weather App")
    root.configure(background="#000000")

    search_bar = SearchBar(root, bg="#000000")
    search_bar.pack(pady=(20, 10))

    root.mainloop()


if __name__ == "__main__":
    main()
