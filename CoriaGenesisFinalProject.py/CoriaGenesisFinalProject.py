import tkinter as tk
from tkinter import messagebox, ttk
from PIL import Image, ImageTk
import re

class PlaceholderEntry(tk.Entry):
    """
    Custom Entry widget with placeholder text.
    """
    def __init__(self, master=None, placeholder="PLACEHOLDER", color='grey', *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        
        # Initialize placeholder text and color
        self.placeholder = placeholder
        self.placeholder_color = color
        self.default_fg_color = self['fg']  # Default text color
        
        # Bind events to handle placeholder text
        self.bind("<FocusIn>", self._clear_placeholder)
        self.bind("<FocusOut>", self._add_placeholder)
        
        self._add_placeholder()  # Add placeholder initially

    def _clear_placeholder(self, e):
        """
        Clear the placeholder text when the entry gets focus.
        """
        if self['fg'] == self.placeholder_color:  # If placeholder color is set
            self.delete('0', 'end')  # Clear the entry
            self['fg'] = self.default_fg_color  # Reset to default text color

    def _add_placeholder(self, e=None):
        """
        Add the placeholder text when the entry loses focus.
        """
        if not self.get():  # If the entry is empty
            self.insert(0, self.placeholder)  # Insert placeholder text
            self['fg'] = self.placeholder_color  # Set placeholder color

class RecyclingApp(tk.Tk):
    """
    Main application class for the ReEarth Recycling App.
    """
    def __init__(self):
        super().__init__()
        self.title("ReEarth Recycling App")  # Set window title
        self.geometry("700x550")  # Set window size
        
        # Recycling information for each tab
        self.recycling_info = {
            "Plastics": "(HOW TO) Recycling instructions for plastics:\n\n"
                        "1. Rinse out all plastic containers.\n"
                        "2. Remove any labels, lids, or caps.\n"
                        "3. Take plastic bags to a grocery store that accepts them.\n"
                        "4. Check for recycling symbols and sort accordingly.\n"
                        "5. Avoid recycling items with food residue.\n\n"
                        "Do Not:\n"
                        "1. Do not recycle plastic bags in curbside bins.\n"
                        "2. Do not recycle plastic items with food contamination.\n"
                        "3. Do not recycle Styrofoam products.\n"
                        "4. Do not recycle plastic toys.",

            "Paper": "(HOW TO) Recycling instructions for paper:\n\n"
                     "1. Separate paper types (newspapers, office paper, cardboard).\n"
                     "2. Remove any staples, paper clips, or bindings.\n"
                     "3. Ensure paper is clean and dry.\n"
                     "4. Flatten cardboard boxes.\n"
                     "5. Make sure paper is not contaminated with food or grease.\n\n"
                     "Do Not:\n"
                     "1. Do not recycle paper towels or tissues.\n"
                     "2. Do not recycle paper with food contamination.\n"
                     "3. Do not recycle laminated paper.\n"
                     "4. Do not recycle wax-coated paper.",

            "Metals": "(HOW TO) Recycling instructions for metals:\n\n"
                      "1. Rinse out metal cans and containers.\n"
                      "2. Remove any labels, lids, or non-metal parts.\n"
                      "3. Check for recycling symbols and sort accordingly.\n"
                      "4. Crush cans to save space, if possible.\n\n"
                      "Do Not:\n"
                      "1. Do not recycle aerosol cans unless empty.\n"
                      "2. Do not recycle items with hazardous materials.\n"
                      "3. Do not recycle electronics or batteries.\n"
                      "4. Do not recycle metal items that are not containers.",

            "Glass": "(HOW TO) Recycling instructions for glass:\n\n"
                     "1. Rinse out glass bottles and jars.\n"
                     "2. Remove any labels, lids, or caps.\n"
                     "3. Separate by color (clear, green, brown).\n"
                     "4. Avoid mixing glass with other recyclables.\n\n"
                     "Do Not:\n"
                     "1. Do not recycle broken glass.\n"
                     "2. Do not recycle light bulbs or mirrors.\n"
                     "3. Do not recycle ceramics or Pyrex.\n"
                     "4. Do not recycle glass with food contamination."
        }
        
        # Initialize introduction screen
        self.show_intro_screen()

    def show_intro_screen(self):
        """
        Display the introduction screen with welcome message and Continue/exit buttons.
        """
        self.clear_screen()  # Clear existing widgets
        
        intro_label = tk.Label(self, text="Welcome to ReEarth", font=("Helvetica", 16))
        intro_label.pack(pady=20)  # Add padding
        
        description_label = tk.Label(self, text="Make recycling more informative!", font=("Helvetica", 12))
        description_label.pack(pady=10)

        continue_button = tk.Button(self, text="Continue", command=self.show_main_interface)
        continue_button.pack(pady=20)
        
        exit_button = tk.Button(self, text="Exit", command=self.quit_app)
        exit_button.pack(pady=10)
        
        # Store widgets to manage them later
        self.intro_widgets = [intro_label, description_label, continue_button, exit_button]

    def show_main_interface(self):
        """
        Display the main interface with search functionality and category tabs.
        """
        self.clear_screen()  # Clear existing widgets
        
        # Create search frame
        search_frame = tk.Frame(self)
        search_frame.pack(pady=20, padx=20, fill='x')
        
        search_label = tk.Label(search_frame, text="Generate a fun fact:")
        search_label.pack(side=tk.LEFT, padx=5)
        
        # Placeholder entry for search
        self.search_entry = PlaceholderEntry(search_frame, placeholder="Search here for plastic, paper, metal or glass ", width=30)
        self.search_entry.pack(side=tk.LEFT, padx=5)
        
        search_button = tk.Button(search_frame, text="Search", command=self.search_item)
        search_button.pack(side=tk.LEFT, padx=5)
        
        clear_button = tk.Button(search_frame, text="Clear", command=self.clear_search)
        clear_button.pack(side=tk.LEFT, padx=5)
        
        self.result_label = tk.Label(self, text="")
        self.result_label.pack(pady=10)
        
        # Create notebook for tabs
        notebook = ttk.Notebook(self)
        notebook.pack(expand=True, fill='both', padx=10, pady=10)
        
        # Add tabs with recycling information and a Back button
        for tab, instructions in self.recycling_info.items():
            frame = ttk.Frame(notebook)
            notebook.add(frame, text=tab)
            label = tk.Label(frame, text=instructions, justify=tk.LEFT, wraplength=500)
            label.pack(padx=10, pady=10)
            
            # Add the Recycling symbols button to each tab
            recycling_symbols_button = tk.Button(frame, text="Recycling symbols", command=self.open_second_window)
            recycling_symbols_button.pack(pady=10)
            
            back_button = tk.Button(frame, text="Back", command=self.show_intro_screen)
            back_button.pack(pady=10)
        
        # Store widgets to manage them later
        self.main_widgets = [search_frame, search_label, self.search_entry, search_button, clear_button, self.result_label, notebook]

    def search_item(self):
        """
        Handle search functionality and display search results.
        """
        item = self.search_entry.get().strip().lower()  # Get and strip search input and convert to lower case
        
        # Input validation: Check if entry is not empty and does not contain only placeholder text
        if not item or item == self.search_entry.placeholder.lower():
            messagebox.showerror("Input Error", "Please enter an item to search.")
            return
        
        # Input validation: Check if entry contains valid characters (letters, hyphens, spaces)
        if not re.match("^[A-Za-z\s\-]+$", item):
            messagebox.showerror("Input Error", "Please enter a valid item name (letters, hyphens, and spaces only).")
            return
        
        # Dictionary of fun facts
        fun_facts = {
            "plastic": "Did you know? Recycling plastic can save up to 88% of the energy needed to produce plastic from raw materials!",
            "paper": "Did you know? Recycling one ton of paper can save 17 trees and 7,000 gallons of water!",
            "metal": "Did you know? Recycling one aluminum can saves enough energy to power a TV for three hours!",
            "glass": "Did you know? Recycling glass reduces water pollution by 50% and air pollution by 20%!"
        }
        
        # Display fun fact if the item is in the dictionary
        if item in fun_facts:
            self.result_label.config(text=f"Fun fact for {item.capitalize()}:\n{fun_facts[item]}")
        else:
            self.result_label.config(text=f"No fun facts available for {item.capitalize()}.")

    def clear_search(self):
        """
        Clear the search input and results.
        """
        self.search_entry.delete(0, tk.END)  # Clear search entry
        self.result_label.config(text="")  # Clear result label
        self.search_entry._add_placeholder()  # Re-add placeholder text

    def quit_app(self):
        """
        Quit the application.
        """
        self.quit()  # Quit the app

    def clear_screen(self):
        """
        Clear all widgets from the screen.
        """
        for widget in self.winfo_children():
            widget.destroy()  # Destroy each widget

    def open_second_window(self):
        """
        Open a second window with additional information.
        """
        second_window = tk.Toplevel(self)
        second_window.title("Additional Information")
        second_window.geometry("900x900")
        
        info_label = tk.Label(second_window, text="Get to know the recycling symbols!", font=("Helvetica", 14))
        info_label.pack(pady=20)
        
     # Load and display an image1 
        image1 = Image.open('recycling1.png')
        #image1 = ImageTk.PhotoImage(image1)
        resized_image= image1.resize((800,450)) 
        image1= ImageTk.PhotoImage(resized_image)
    
    # Create a label to display the image1
        image_label1 = tk.Label(second_window, image=image1)
        image_label1.pack()
    
    # Load and display an image2
        image2 = Image.open('recycling2.png')
        #image2 = ImageTk.PhotoImage(image2)
        resized_image= image2.resize((650,250)) 
        image2= ImageTk.PhotoImage(resized_image)

     # Create a label to display the image2
        image_label2 = tk.Label(second_window, image=image2)
        image_label2.pack()

        back_button = tk.Button(second_window, text="Back", command=second_window.destroy)
        back_button.pack(pady=10)
        second_window.mainloop()

if __name__ == "__main__":
    app = RecyclingApp()
    app.mainloop()