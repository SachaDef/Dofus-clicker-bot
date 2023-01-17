import customtkinter as ctk
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("dark-blue")

import new_backend as backend


# ==== Main GUI window ==== #
class MainApplication(ctk.CTk):

    def __init__(self):
        super().__init__()

        # Global variables
        self.width = 800
        self.height = 700
        self.clear_red = '#e60000'
        self.dark_red = '#800000'
        self.clear_green = '#009900'
        self.dark_green = '#004d00'
        self.border_gray = '#565B5E'
        self.secondary_background_gray = "#292929"
        self.main_background_gray = "#212121"
        self.entry_gray = '#343638'
        
        # Initialization
        self.geometry(f"{self.width}x{self.height}")
        self.title("DofusBot")
        self.iconbitmap(r'img\icon.ico')

        # Tabs creation
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.tabs = ctk.CTkTabview(master=self)
        self.general_tab = self.tabs.add("General")
        self.settings_tab = self.tabs.add("Settings")
        self.character_tabs = []
        self.tabs.set("General")
        self.tabs.grid(column=0, row=0, sticky='nsew')

        # General tab
        self.general_tab.grid_columnconfigure(0, weight=1)
        self.general_tab.grid_rowconfigure((0, 3), weight=1)
        self.general_tab.grid_rowconfigure((1, 2), weight=4)
        self.character_frame = ctk.CTkFrame(master=self.general_tab)
        self.map_frame = ctk.CTkFrame(master=self.general_tab)
        self.path_frame = ctk.CTkFrame(master=self.general_tab)
        self.quit_frame = ctk.CTkFrame(master=self.general_tab)

        #### Character frame
        self.character_frame.grid_columnconfigure((0, 1, 2), weight=1)
        self.character_frame.grid_rowconfigure(0, weight=1)
        ####### Methods
        self.windows = []
        self.character_names = []
        def refresh_windows():
            self.windows = backend.window_filtering(self.character_window_variable.get())
            self.character_names = []
            for window in self.windows:
                self.character_names.append(window[1].split(" - ")[0])
            if len(self.character_names) == 0:
                self.character_window.configure(values=self.character_names,
                                                fg_color=self.dark_red,
                                                button_color=self.clear_red,
                                                border_color=self.clear_red)
                self.after(1000, lambda: self.character_window.configure(fg_color=self.entry_gray,
                                                                         border_color=self.border_gray,
                                                                         button_color=self.border_gray))
            else:
                self.character_window.set(self.character_names[0])
                self.character_window.configure(values=self.character_names,
                                                fg_color=self.dark_green,
                                                button_color=self.clear_green,
                                                border_color=self.clear_green)
                self.after(1000, lambda: self.character_window.configure(fg_color=self.entry_gray,
                                                                         border_color=self.border_gray,
                                                                         button_color=self.border_gray))

        def validate_character():
            if self.character_window_variable.get() in self.character_names:
                self.add_character_button.configure(state='normal')
                return
            self.add_character_button.configure(state='disabled')
           
        def add_character(): #TODO
            character_name = self.character_window_variable.get()
            if character_name not in self.character_names:
                return
            current_window = ()
            for window in self.windows:
                if window[1].startswith(character_name):
                    current_window = window
            if not current_window:
                return
            self.new_character_tab(character_name)
            
        ####### Content
        self.character_window_variable = ctk.StringVar(value="Character name")
        self.character_window = ctk.CTkComboBox(master=self.character_frame,
                                                values=[],
                                                variable=self.character_window_variable)
        self.refresh_windows_button = ctk.CTkButton(master=self.character_frame,
                                                    text="Refresh list",
                                                    command=refresh_windows)
        self.add_character_button = ctk.CTkButton(master=self.character_frame,
                                                  text="Add character",
                                                  command=add_character,
                                                  state='disabled')
        self.character_window_variable.trace_add(("read", "write", "unset"),
                                                 lambda name, index, mode: validate_character())
        ####### Placement
        self.character_window.grid(column=0, row=0, padx=20, pady=5)
        self.refresh_windows_button.grid(column=1, row=0, padx=20, pady=5)
        self.add_character_button.grid(column=2, row=0, padx=20, pady=5)
        self.character_frame.grid(column=0, row=0, sticky='nsew', pady=5)
        ####### Post actions
        # refresh_windows()

        #### Map frame
        self.map_frame.grid_columnconfigure((0, 2), weight=1)
        self.map_frame.grid_columnconfigure(1, weight=3)
        self.map_frame.grid_rowconfigure(0, weight=1)
        self.map_frame.grid_rowconfigure(1, weight=4)
        ####### Methods
        def map_change():#TODO
            pass

        def add_map():#TODO
            pass

        def remove_map():#TODO
            pass
        
        def edit_map():#TODO
            pass
        ####### Content
        self.map_coordinates_label = ctk.CTkLabel(master=self.map_frame,
                                                  text="Map coordinates")
        self.map_coordinates_frame = ctk.CTkFrame(master=self.map_frame,
                                                  bg_color=self.secondary_background_gray,
                                                  fg_color=self.secondary_background_gray)
        self.map_xcoord_label = ctk.CTkLabel(master=self.map_coordinates_frame,
                                             text="X = ",
                                             bg_color=self.secondary_background_gray)
        self.map_xcoord_entry = ctk.CTkEntry(master=self.map_coordinates_frame,
                                             bg_color=self.secondary_background_gray)
        self.map_ycoord_label = ctk.CTkLabel(master=self.map_coordinates_frame,
                                             text="Y = ",
                                             bg_color=self.secondary_background_gray)
        self.map_ycoord_entry = ctk.CTkEntry(master=self.map_coordinates_frame,
                                             bg_color=self.secondary_background_gray)
        self.map_change_button = ctk.CTkButton(master=self.map_coordinates_frame,
                                               text="Check map",
                                               command=map_change)

        self.map_click_coordinates_label = ctk.CTkLabel(master=self.map_frame,
                                                        text="Associated click coordinates")
        self.click_coordinates_text = ctk.CTkTextbox(master=self.map_frame)

        self.map_buttons_label = ctk.CTkLabel(master=self.map_frame,
                                              text="Actions")
        self.map_buttons_frame = ctk.CTkFrame(master=self.map_frame,
                                              bg_color=self.secondary_background_gray,
                                              fg_color=self.secondary_background_gray)
        self.add_map_button = ctk.CTkButton(master=self.map_buttons_frame,
                                            text="Add map",
                                            command=add_map)
        self.remove_map_button = ctk.CTkButton(master=self.map_buttons_frame,
                                               text="Remove map",
                                               command=remove_map)
        self.edit_map_button = ctk.CTkButton(master=self.map_buttons_frame,
                                             text="Edit map",
                                             command=edit_map)
        ####### Placement
        self.map_coordinates_label.grid(column=0, row=0)
        self.map_xcoord_label.grid(column=0, row=0)
        self.map_xcoord_entry.grid(column=1, row=0, pady=5)
        self.map_ycoord_label.grid(column=0, row=1)
        self.map_ycoord_entry.grid(column=1, row=1, pady=5)
        self.map_change_button.grid(column=0, row=2, pady=5, columnspan=2)
        self.map_coordinates_frame.grid(column=0, row=1)

        self.map_click_coordinates_label.grid(column=1, row=0)
        self.click_coordinates_text.grid(column=1, row=1, pady=10, sticky='nsew')
        
        self.map_buttons_label.grid(column=2, row=0)
        self.add_map_button.grid(column=0, row=0, pady=5)
        self.remove_map_button.grid(column=0, row=1, pady=5)
        self.edit_map_button.grid(column=0, row=2, pady=5)
        self.map_buttons_frame.grid(column=2, row=1)
        self.map_frame.grid(column=0, row=1, sticky='nsew', pady=5)

        #### Path frame
        self.path_frame.grid_columnconfigure((0, 2, 3), weight=1)
        self.path_frame.grid_columnconfigure(1, weight=3)
        self.path_frame.grid_rowconfigure(0, weight=1)
        self.path_frame.grid_rowconfigure(1, weight=4)
        ####### Methods
        ####### Content
        self.farming_path_variable = ctk.StringVar(value="Farming path")
        self.farming_path = ctk.CTkComboBox(master=self.path_frame, values=[], variable=self.character_window_variable)
        ####### Placement
        test = XYPopUp("Test")
        test.wait_window()
        print(test.x, test.y)


    def new_character_tab(self, character_name):
        self.character_tabs.append(self.tabs.add(character_name))
        character_tab = self.character_tabs[-1]



class GeneralTab(ctk.CTkFrame):

    def __init__(self):
        super().__init__()

        

        

class PopUp(ctk.CTkToplevel):
    
    def __init__(self, title, width=300, height=200, duration=0):
        super().__init__()
        self.title(title)
        self.geometry(f"{width}x{height}")
        if duration:
            self.after(duration, self.destroy)
        self.bind("<Return>", self.confirm)
        self.bind("<Escape>", self.infirm)
    
    def confirm(self):
        self.destroy()

    def infirm(self):
        self.destroy()

class XYPopUp(PopUp):

    def __init__(self, title):
        super().__init__(title)
        bg = "#212121"
        self.x_value=None
        self.y_value=None
        self.configure(bg_color=bg, fg_color=bg)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        container = ctk.CTkFrame(self, fg_color=bg)
        ctk.CTkLabel(container, text="Character X = ").grid(column=0, row=0)
        self.x_entry = ctk.CTkEntry(container)
        self.x_entry.grid(column=1, row=0, pady=10)
        ctk.CTkLabel(container, text="Character y = ").grid(column=0, row=1)
        self.y_entry = ctk.CTkEntry(container)
        self.y_entry.grid(column=1, row=1, pady=10)
        ctk.CTkButton(container, text="Validate", command=self.confirm).grid(column=0, row=2, columnspan=2)
        self.error_label = ctk.CTkLabel(container, text="Unvalid coordinates")
        container.grid()
        self.mainloop()

    def confirm(self):
        if 1 <= len(self.x_entry.get()) <= 4 and 1 <= len(self.y_entry.get()) <= 4\
        and self.x_entry.get().replace("-", "").isdigit() and self.y_entry.get().replace("-", "").isdigit():
            self.x_value = int(self.x_entry.get())
        else:
            self.error_label.grid(row=3, column=0, columnspan=2)
            self.after(2000, lambda: self.error_label.grid_remove())
        self.destroy()

        

app = MainApplication()
app.mainloop()



