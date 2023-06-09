import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from get_weather import get_weather
from valid_cities import get_valid_cities




class MainApplication(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Isaacs Weather Application")
        self.geometry("1000x650")
        self.configure(bg="#000000")

        self.style = ttk.Style()
        self.style.theme_use("clam")

        self.notebook = ttk.Notebook(self, style="Custom.TNotebook")
        self.notebook.pack(fill=tk.BOTH, expand=True)

        self.screen1 = tk.Frame(self.notebook, bg="#000000")
        self.screen2 = tk.Frame(self.notebook, bg="#000000")

        self.notebook.add(self.screen1, text="Weather")
        self.notebook.add(self.screen2, text="Crime")

        self.modify_screen1()
        self.modify_screen2()

    def modify_screen1(self):
        """
            Modify the content of Screen 1.
        """
        label1 = tk.Label(self.screen1, text="Weather", bg="#000000", fg="#FFFFFF", font=("Arial", 32, "bold"))
        label1.pack(pady=(20, 0), anchor="w", padx=20)

        self.create_search_bar()

    def modify_screen2(self):
        """
            Modify the content of Screen 2.
        """
        label2 = tk.Label(self.screen2, text="Crime", bg="#000000", fg="#FFFFFF")
        label2.pack(pady=20)

    def create_search_bar(self):
        """
        Create the search bar widget.
        """
        search_frame = tk.Frame(self.screen1, bg="#000000")
        search_frame.pack(pady=0, anchor="w", padx=(20, 0))  # Fill horizontally

        self.list_frame = tk.Frame(self.screen1, bg="#000000")
        self.list_frame.pack(pady=0, anchor="w", padx=(0, 0))

        self.configure_search_entry(search_frame)
        self.configure_listbox()

    def configure_search_entry(self, parent_frame):
        """
            Configure the search entry widget.

            Search entry box is where the user types into the search bar field.
        """
        self.style.configure("Custom.TEntry", 
                             fieldbackground="#3A3B3C", 
                             foreground="#B0B3B8", 
                             borderwidth=1,
                             bordercolor="black", 
                             relief="flat", 
                             width=100,
                             insertcolor= "white",
                             selectforeground= "black",
                             )
        self.style.map("Custom.TEntry",
                       bordercolor=[("focus", "#3A3B3C")],
                       relief=[("focus", "solid")],
                       selectbackground=[("focus", "white"), ("!focus", "lime green")],
                       )

        self.default_text = "Search for a city"

        self.load_and_resize_image(parent_frame)

        entry_frame = tk.Frame(parent_frame, bg="#000000")
        entry_frame.pack(side=tk.LEFT)

        self.search_entry = ttk.Entry(entry_frame, style="Custom.TEntry")
        self.search_entry.pack(side=tk.LEFT, padx=(0, 5))
        self.search_entry.configure(width=40)
        self.search_entry.insert(0, self.default_text)

        search_button = ttk.Button(entry_frame, text="Search", command=self.on_search_button, style="Custom.TButton")
        search_button.pack(side=tk.LEFT)

        self.search_entry.bind("<FocusIn>", self.on_entry_focus_in)
        self.search_entry.bind("<FocusOut>", self.on_entry_focus_out)
        self.search_entry.bind("<Return>", self.on_return_key)
        self.search_entry.bind("<KeyRelease>", self.check_listbox)
        self.search_entry.configure(font=("Arial", 20))

    def configure_listbox(self):
        """
            Configure the listbox widget.

            Listbox is a list of cities that the user may type in searchbar. The list contains very few cities so far, but
            the user may type any valid city and try to see if their is a weather api for that city.
        """
        if hasattr(self, "listbox"):
            self.listbox.destroy()

        self.listbox = tk.Listbox(self.list_frame, bg="#3A3B3C", fg="#B0B3B8", font=("Arial", 19), width=58)
        self.listbox.pack(pady=0, side=tk.LEFT, padx=(20, 0))

        self.cities = get_valid_cities()
        self.cities.sort()
        self.update_listbox(self.cities)
        self.listbox.bind("<<ListboxSelect>>", self.fillout)
        self.listbox.pack_forget()

    def fillout(self, e):
        """
            Allows us to click on cities in listbox and fill out search bar
        """
        # delete what is in the entry box
        self.search_entry.delete(0, tk.END)

        # add clicked city to search_entry
        selected_item = self.listbox.get(self.listbox.curselection())
        #clean the selected item
        item_array = selected_item.split("*")
        #print(item_array[1].strip())
        self.search_entry.insert(0, item_array[1].strip())

        search_query = self.search_entry.get()
        if search_query.lower() != self.default_text.lower() and search_query.lower() != "":
            # Search weather for city_name 
            result = get_weather(search_query)
            if result:
                print(result)
            else:
                print("City weather not found")
                self.city_not_found()

        self.screen1.focus_set()

    def update_listbox(self, cities):
        """
            Updates listbox with passed in cities
        """
        # clear the listbox
        self.listbox.delete(0, tk.END)
        for city in cities:
            padding = "  *  "
            self.listbox.insert(tk.END, padding + city)
    
    def check_listbox(self, e):
        """
            updates listbox with cities that have the characters user has typed.
        """
        user_typed = self.search_entry.get()
        if user_typed == '':
            data = self.cities
        else:
            data = []
            for city in self.cities:
                if user_typed.lower() in city.lower():
                    data.append(city)
        # update our listbox with selected cities
        self.update_listbox(data)

        
    def load_and_resize_image(self, parent_frame):
        """
            Load and resize the image for the search bar.
        """

        # add some style to the image label
        style = ttk.Style()
        style.configure("Custom.TLabel", bordercolor="#3A3B3C", relief="solid")

        # open image and put image in image label
        image = Image.open("Images/cloud.png").resize((30, 23))
        photo = ImageTk.PhotoImage(image)
        self.image_label = ttk.Label(parent_frame, image=photo, background="#3A3B3C", style="Custom.TLabel")
        self.image_label.image = photo
        self.image_label.pack(side=tk.LEFT, padx=(5, 0))

    def on_entry_focus_in(self, event):
        """
            Handle the focus in event of the search entry.
        """
        if self.search_entry.get() == self.default_text:
            self.search_entry.configure(foreground="#FFFFFF")
            self.search_entry.delete(0, tk.END)

        self.search_entry.configure(width=50)# CHANGES search bar SIZE
        self.list_frame.pack(pady=0, anchor="w", padx=5) # this prevents listbox from shfiting after refocusing
        self.configure_listbox()
        self.listbox.pack(padx=(20, 0))

        self.style.configure("Custom.TLabel", bordercolor="#3A3B3C", relief="solid")
        self.image_label.configure(style="Custom.TLabel")

        # Destroy the error frame if it exists
        if hasattr(self, "error_frame"):
            self.error_frame.destroy()

    def on_entry_focus_out(self, event):
        """
            Handle the focus out event of the search entry.
        """
        if not self.search_entry.get():
            self.search_entry.configure(foreground="#B0B3B8")
            self.search_entry.insert(0, self.default_text)

        self.search_entry.configure(width=40)# CHANGES search bar SIZE
        self.list_frame.pack_forget()

        style = ttk.Style()
        style.configure("Custom.TLabel", bordercolor="#3A3B3C", relief="solid")
        self.image_label.configure(style="Custom.TLabel")

    def on_return_key(self, event):
        """
            Handle the return key event of the search entry.
        """
        search_query = self.search_entry.get()
        if search_query.lower() != self.default_text.lower() and search_query.lower() != "":
            # Search weather for city_name 
            result = get_weather(search_query)
            if result:
                print(result)
            else:
                self.city_not_found()

        self.screen1.focus_set()

    def on_search_button(self):
        """
            Handle the search button click event.
        """
        search_query = self.search_entry.get()
        if search_query.lower() != self.default_text.lower() and search_query.lower() != "":
            # Search weather for city_name 
            weather_data = get_weather(search_query)
            if weather_data:
                print(weather_data)
            else:
                self.city_not_found()

        self.screen1.focus_set()
    
    def city_not_found(self):
        print("City weather not found")
        self.error_frame = tk.Frame(self.screen1, 
                                    bg="black", 
                                    width=700, height=500, 
                                    highlightthickness=0, 
                                    highlightbackground="black", 
                                    borderwidth=0)
        self.error_frame.pack(pady=50)

        self.add_sad_cloud()
        error_label = tk.Label(self.error_frame, text="No Results", font=("Arial", 55, "bold"), bg="#000000", fg="#FFFFFF")
        error_label.pack()

        entry = self.search_entry.get()
        error_message_label = tk.Label(self.error_frame, text=f'No results found for "{entry}"', font=("Arial", 22), bg="#000000", fg="light gray")
        error_message_label.pack()
    
    def add_sad_cloud(self):
        """
        Load and resize the image for the search bar.
        """
        # Add some style to the image label
        style = ttk.Style()
        style.configure("Custom.TLabel", relief="flat", bordercolor="red", borderwith=0)

        # Open image and put image in image label
        image = Image.open("Images/sadcloudsprite.png").resize((420, 300))
        photo = ImageTk.PhotoImage(image)

        # Destroy the existing image_label widget if it exists
        if hasattr(self.error_frame, "image_label"):
            image_label.destroy()

        # Create a new label with the updated style
        image_label = ttk.Label(self.error_frame, image=photo, background="black", style="Custom.TLabel")
        image_label.image = photo
        image_label.pack()



if __name__ == "__main__":
    app = MainApplication()
    app.mainloop()
