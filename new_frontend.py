import customtkinter as ctk
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("dark-blue")
from new_globals import *
import new_backend as backend



# ==== Main GUI window ==== #
class MainApplication(ctk.CTk):

    def __init__(self):
        super().__init__()

        # Global variables
        self.width  = self.winfo_screenwidth()
        self.height = self.winfo_screenheight()
        
        # Initialization
        self.geometry(f"{self.width}x{self.height}")
        self.state("zoomed")
        self.title("DofusBot")
        self.iconbitmap(r'img\icon.ico')

        # Tabs initialization
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.tabs = ctk.CTkTabview(master=self)
        self.general_tab = self.tabs.add("General")
        self.settings_tab = self.tabs.add("Settings")
        self.tracked_characters = []          # List of (character_name, character_tab, character_bot)
        self.tabs.set("General")
        self.tabs.grid(column=0, row=0, sticky='nsew')

        # Tabs creation
        GeneralTabConstructor(self, self.general_tab)


class GeneralTabConstructor():

    def __init__(self, main_app: MainApplication, tab: ctk.CTkFrame):
        # Variables
        self.main_app = main_app
        self.tab = tab
        self.windows = []
        self.character_names = []
        self.path_files = []
        self.path_names = []

        # Initialization
        self.tab.grid_columnconfigure(0, weight=1)
        self.tab.grid_rowconfigure(0, weight=1)
        self.tab.grid_rowconfigure((1, 2), weight=2)
        self.character_frame = ctk.CTkFrame(master=self.tab)
        self.map_frame = ctk.CTkFrame(master=self.tab)
        self.path_frame = ctk.CTkFrame(master=self.tab)


        #### Character frame
        self.character_frame.grid_columnconfigure((0, 2), weight=10)
        self.character_frame.grid_columnconfigure(1, weight=16)
        self.character_frame.grid_rowconfigure(0, weight=1)

        ####### Methods
        def refresh_windows():
            self.windows, self.character_names = backend.window_filtering()
            if len(self.character_names) == 0:
                self.character_window.configure(values=self.character_names,
                                                fg_color=dark_red,
                                                button_color=clear_red)
                self.tab.after(1000, lambda: self.character_window.configure(fg_color=entry_gray,
                                                                             button_color=border_gray))
            else:
                self.character_window.set(self.character_names[0])
                self.character_window.configure(values=self.character_names,
                                                fg_color=dark_green,
                                                button_color=clear_green)
                self.tab.after(1000, lambda: self.character_window.configure(fg_color=entry_gray,
                                                                             button_color=border_gray))

        def validate_character():
            if self.character_window_variable.get() in self.character_names:
                self.add_character_button.configure(state='normal')
            else:
                self.add_character_button.configure(state='disabled')
           
        def add_character(): #TODO
            character_name = self.character_window_variable.get()
            if character_name not in self.character_names:
                return
            xy_popup = XYPopUp(f"{character_name} - Position")
            xy_popup.grab_set()
            self.main_app.wait_window(xy_popup)
            x, y = xy_popup.x_value, xy_popup.y_value
            if x is None or y is None:
                return
            current_window = ()
            for window in self.windows:
                if window[1].startswith(character_name):
                    current_window = window
            if not current_window:
                return
            character_bot = backend.CharacterBot(character_name, x, y, current_window[0])
            self.main_app.tracked_characters.append((character_name, self.main_app.tabs.add(character_name), character_bot))
            CharacterTabConstructor(self.main_app, character_name)
            
        ####### Content
        ########## 1st column
        self.character_window_variable = ctk.StringVar(value="Character name")
        self.character_window = ctk.CTkOptionMenu(master=self.character_frame,
                                                  values=[],
                                                  variable=self.character_window_variable)
        self.character_window_variable.trace_add("write",
                                                 lambda *_: validate_character())
        
        ########## 2nd column
        self.refresh_windows_button = ctk.CTkButton(master=self.character_frame,
                                                    text="Refresh list",
                                                    command=refresh_windows)

        ########## 3rd column
        self.add_character_button = ctk.CTkButton(master=self.character_frame,
                                                  text="Add character",
                                                  command=add_character,
                                                  state='disabled')

        ####### Placement
        ########## 1st column
        self.character_window.grid(column=0, row=0, pady=5)

        ########## 2nd column
        self.refresh_windows_button.grid(column=1, row=0, pady=5)

        ########## 3rd column
        self.add_character_button.grid(column=2, row=0, pady=5)

        ########## Character frame
        self.character_frame.grid(column=0, row=0, sticky='nsew', pady=5)

        ####### Post actions
        refresh_windows()


        #### Map frame
        self.map_frame.grid_columnconfigure((0, 2), weight=2)
        self.map_frame.grid_columnconfigure(1, weight=3)
        self.map_frame.grid_rowconfigure(0, weight=1)
        self.map_frame.grid_rowconfigure(1, weight=4)

        ####### Methods
        def show_map():#TODO
            pass

        def new_map():#TODO
            pass

        def delete_map():#TODO
            pass
        
        def save_map_changes():#TODO
            pass

        def discard_map_changes():#TODO
            pass

        ####### Content
        ########## 1st column
        self.map_coordinates_label = ctk.CTkLabel(master=self.map_frame,
                                                  text="Map coordinates")
        self.map_coordinates_container = ctk.CTkFrame(master=self.map_frame,
                                                  bg_color=secondary_background_gray,
                                                  fg_color=secondary_background_gray)
        self.map_xcoord_label = ctk.CTkLabel(master=self.map_coordinates_container,
                                             text="X = ",
                                             bg_color=secondary_background_gray)
        self.map_xcoord_entry = ctk.CTkEntry(master=self.map_coordinates_container,
                                             bg_color=secondary_background_gray)
        self.map_ycoord_label = ctk.CTkLabel(master=self.map_coordinates_container,
                                             text="Y = ",
                                             bg_color=secondary_background_gray)
        self.map_ycoord_entry = ctk.CTkEntry(master=self.map_coordinates_container,
                                             bg_color=secondary_background_gray)
        self.show_map_button = ctk.CTkButton(master=self.map_coordinates_container,
                                               text="Show map",
                                               command=show_map)

        ########## 2nd column
        self.map_click_coordinates_label = ctk.CTkLabel(master=self.map_frame,
                                                        text="Associated click coordinates")
        self.map_click_coordinates_textbox = ctk.CTkTextbox(master=self.map_frame,
                                                            height=100)

        ########## 3rd column
        self.map_buttons_label = ctk.CTkLabel(master=self.map_frame,
                                              text="Map commands")
        self.map_buttons_container = ctk.CTkFrame(master=self.map_frame,
                                                  bg_color=secondary_background_gray,
                                                  fg_color=secondary_background_gray)
        self.add_map_button = ctk.CTkButton(master=self.map_buttons_container,
                                            text="New map",
                                            command=new_map)
        self.remove_map_button = ctk.CTkButton(master=self.map_buttons_container,
                                               text="Delete map",
                                               command=delete_map)
        self.save_map_changes_button = ctk.CTkButton(master=self.map_buttons_container,
                                             text="Save changes",
                                             command=save_map_changes)
        self.discard_map_changes_button = ctk.CTkButton(master=self.map_buttons_container,
                                                     text="Discard changes",
                                                     command=discard_map_changes)

        ####### Placement
        ########## 1st column
        self.map_coordinates_label.grid(column=0, row=0)
        self.map_xcoord_label.grid(column=0, row=0)
        self.map_xcoord_entry.grid(column=1, row=0)
        self.map_ycoord_label.grid(column=0, row=1)
        self.map_ycoord_entry.grid(column=1, row=1, pady=15)
        self.show_map_button.grid(column=0, row=2, pady=15, columnspan=2, sticky='e')
        self.map_coordinates_container.grid(column=0, row=1)

        ########## 2nd column
        self.map_click_coordinates_label.grid(column=1, row=0)
        self.map_click_coordinates_textbox.grid(column=1, row=1, pady=10, sticky='nsew')
        
        ########## 3rd column
        self.map_buttons_label.grid(column=2, row=0)
        self.add_map_button.grid(column=0, row=0, padx=10)
        self.remove_map_button.grid(column=0, row=1, pady=10)
        self.save_map_changes_button.grid(column=0, row=2, pady=10)
        self.discard_map_changes_button.grid(column=0, row=3)
        self.map_buttons_container.grid(column=2, row=1)

        ########## Map frame
        self.map_frame.grid(column=0, row=1, sticky='nsew', pady=5)


        #### Path frame
        self.path_frame.grid_columnconfigure((0, 2), weight=2)
        self.path_frame.grid_columnconfigure(1, weight=3)
        self.path_frame.grid_rowconfigure(0, weight=1)
        self.path_frame.grid_rowconfigure(1, weight=4)

        ####### Methods
        def refresh_paths():
            self.path_files = backend.get_all_paths(self.farming_path_variable.get())
            self.path_names = []
            for path in self.path_files:
                self.path_names.append(path.split("\\")[-1])
            
            if len(self.path_names) == 0:
                self.farming_path.configure(values=self.path_names,
                                            fg_color=dark_red,
                                            border_color=clear_red,
                                            button_color=clear_red)
                self.tab.after(1000, lambda: self.farming_path.configure(fg_color=entry_gray,
                                                                         border_color=border_gray,
                                                                         button_color=border_gray))
            else:
                self.farming_path.set(self.path_names[0])
                self.farming_path.configure(values=self.path_names,
                                            fg_color=dark_green,
                                            border_color=clear_green,
                                            button_color=clear_green)
                self.tab.after(1000, lambda: self.farming_path.configure(fg_color=entry_gray,
                                                                         border_color=border_gray,
                                                                         button_color=border_gray))

        def show_path():#TODO
            pass

        def new_path():#TODO
            pass

        def delete_path():#TODO
            pass

        def save_path_changes():#TODO
            pass

        def discard_path_changes():#TODO
            pass

        ####### Content
        ########## 1st column
        self.farming_path_label = ctk.CTkLabel(master=self.path_frame,
                                               text="Farming path name")
        self.farming_path_container = ctk.CTkFrame(master=self.path_frame,
                                                   bg_color=secondary_background_gray,
                                                   fg_color=secondary_background_gray)
        self.farming_path_variable = ctk.StringVar(value="Farming path")
        self.farming_path = ctk.CTkComboBox(master=self.farming_path_container,
                                            values=[],
                                            variable=self.farming_path_variable)
        self.refresh_paths_button = ctk.CTkButton(master=self.farming_path_container,
                                                  text="Refresh list",
                                                  command=refresh_paths)
        self.show_path_button = ctk.CTkButton(master=self.farming_path_container,
                                              text="Show path",
                                              command=show_path)

        ########## 2nd column
        self.path_map_coordinates_label = ctk.CTkLabel(master=self.path_frame,
                                                       text="Associated map coordinates")
        self.path_map_coordinates_textbox = ctk.CTkTextbox(master=self.path_frame,
                                                           height=100)

        ########## 3rd column
        self.path_buttons_label = ctk.CTkLabel(master=self.path_frame,
                                               text="Path commands")
        self.path_buttons_container = ctk.CTkFrame(master=self.path_frame,
                                                   bg_color=secondary_background_gray,
                                                   fg_color=secondary_background_gray)
        self.add_path_button = ctk.CTkButton(master=self.path_buttons_container,
                                             text="New path",
                                             command=new_path)
        self.remove_path_button = ctk.CTkButton(master=self.path_buttons_container,
                                                text="Delete path",
                                                command=delete_path)
        self.save_path_changes_button = ctk.CTkButton(master=self.path_buttons_container,
                                                      text="Save changes",
                                                      command=save_path_changes)
        self.discard_path_changes_button = ctk.CTkButton(master=self.path_buttons_container,
                                                         text="Discard changes",
                                                         command=discard_path_changes)

        ####### Placement
        ########## 1st column
        self.farming_path_label.grid(column=0, row=0)
        self.farming_path.grid(column=0, row=0, pady=15, padx=10)
        self.refresh_paths_button.grid(column=0, row=1, pady=15)
        self.show_path_button.grid(column=0, row=2)
        self.farming_path_container.grid(column=0, row=1)

        ########## 2nd column
        self.path_map_coordinates_label.grid(column=1, row=0)
        self.path_map_coordinates_textbox.grid(column=1, row=1, pady=10, sticky='nsew')

        ########## 3rd column
        self.path_buttons_label.grid(column=2, row=0)
        self.add_path_button.grid(column=0, row=0, padx=10)
        self.remove_path_button.grid(column=0, row=1, pady=10)
        self.save_path_changes_button.grid(column=0, row=2, pady=10)
        self.discard_path_changes_button.grid(column=0, row=3)
        self.path_buttons_container.grid(column=2, row=1)

        ########## Path frame
        self.path_frame.grid(column=0, row=2, sticky='nsew', pady=5)



class CharacterTabConstructor():

    def __init__(self, main_app: MainApplication, character_name: str):
        self.main_app = main_app


        

class PopUp(ctk.CTkToplevel):
    
    def __init__(self, title, width=300, height=200, duration=0):
        super().__init__()
        self.title(title)
        self.geometry(f"{width}x{height}")
        if duration:
            self.after(duration, self.destroy)
        self.bind("<Return>", lambda _: self.confirm())
        self.bind("<Escape>", lambda _: self.infirm)
    
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
        self.x_entry.grid(column=1, row=0)
        ctk.CTkLabel(container, text="Character Y = ").grid(column=0, row=1)
        self.y_entry = ctk.CTkEntry(container)
        self.y_entry.grid(column=1, row=1, pady=15)
        ctk.CTkButton(container, text="Validate", command=self.confirm).grid(column=0, row=2, columnspan=2, pady=(15, 0), sticky='e')
        self.error_label = ctk.CTkLabel(container, text="Unvalid coordinates")
        container.grid()


    def confirm(self):
        if 1 <= len(self.x_entry.get()) <= 4 and 1 <= len(self.y_entry.get()) <= 4\
        and self.x_entry.get().replace("-", "").isdigit() and self.y_entry.get().replace("-", "").isdigit():
            self.x_value = int(self.x_entry.get())
            self.y_value = int(self.y_entry.get())
            self.destroy()
        else:
            self.error_label.grid(row=3, column=0, columnspan=2)
            self.after(1000, lambda: self.error_label.grid_remove())

        

app = MainApplication()
app.mainloop()



