import customtkinter as ctk
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("dark-blue")

import new_globals as globals
import new_backend as backend

import pynput.mouse as mouse
import pickle

# ==== Main GUI window ==== #
class MainApplication(ctk.CTk):

    def __init__(self):
        super().__init__()

        # Global variables
        self.width  = self.winfo_screenwidth()
        self.height = self.winfo_screenheight()
        
        # Initialization
        self.geometry(f"{self.width}x{self.height}")
        self.title("DofusBot")
        self.iconbitmap(r'img\icon.ico')
        self.minsize(800, 600)

        # Tabs initialization
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.tabs = ctk.CTkTabview(master=self)
        self.general_tab = self.tabs.add("General")
        self.settings_tab = self.tabs.add("Settings")
        self.tabs.set("General")
        self.tabs.grid(column=0, row=0, sticky='nsew')

        # Tabs creation
        GeneralTabConstructor(self, self.general_tab)
        SettingsTabConstructor(self, self.settings_tab)
        self.after(5, self.state, "zoomed")


class GeneralTabConstructor():

    def __init__(self, main_app: MainApplication, tab: ctk.CTkFrame):
        # Variables
        self.main_app = main_app
        self.tab = tab

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
            backend.window_filtering()
            if len(globals.active_character_names) == 0:
                self.character_window_variable.set("Character name")
                self.character_window.configure(values=globals.active_character_names,
                                                fg_color=globals.DARK_RED,
                                                button_color=globals.CLEAR_RED)
                self.tab.after(1000, lambda: self.character_window.configure(fg_color=globals.ENTRY_GRAY,
                                                                             button_color=globals.BORDER_GRAY))
            else:
                self.character_window_variable.set(globals.active_character_names[0])
                self.character_window.configure(values=globals.active_character_names,
                                                fg_color=globals.DARK_GREEN,
                                                button_color=globals.CLEAR_GREEN)
                self.tab.after(1000, lambda: self.character_window.configure(fg_color=globals.ENTRY_GRAY,
                                                                             button_color=globals.BORDER_GRAY))

        def validate_character():
            if self.character_window_variable.get() in globals.active_character_names:
                self.add_character_button.configure(state='normal')
            else:
                self.add_character_button.configure(state='disabled')
           
        def add_character():
            character_name = self.character_window_variable.get()
            xy_popup = XYPopUp(f"{character_name} - Position", "Character")
            xy_popup.grab_set()
            self.main_app.wait_window(xy_popup)
            character_x, character_y = xy_popup.x_value, xy_popup.y_value
            character_window = backend.get_character_window(character_name)
            if character_name not in globals.active_character_names or\
               character_x is None or\
               character_y is None or\
               not character_window:
                return

            character_bot = backend.CharacterBot(character_name, character_x, character_y, character_window[0])
            character_info = (character_name, self.main_app.tabs.add(character_name), character_bot)
            globals.tracked_characters.append(character_info)
            CharacterTabConstructor(self.main_app, character_info)
            
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
        def show_map():
            try:
                map_x, map_y = int(self.map_xcoord_entry.get()), int(self.map_ycoord_entry.get())
            except ValueError:
                self.map_coord_value_error_label.configure(text="Invalid coordinates")
                self.main_app.after(1000, lambda: self.map_coord_value_error_label.configure(text=""))
                self.map_xcoord_entry.delete(0, 'end')
                self.map_ycoord_entry.delete(0, 'end')
                self.map_xcoord_entry.focus_set()
                return
            if globals.map_textbox_changed:
                confirm_popup = ConfirmPopUp("Show map - Conflict", "Drop changes made to the map click coordinates ?")
                confirm_popup.grab_set()
                self.main_app.wait_window(confirm_popup)
                if not confirm_popup.value:
                    return
            self.map_click_coordinates_textbox.delete("1.0", 'end')
            self.map_click_coordinates_textbox.insert("1.0", backend.map_get_click_coordinates(map_x, map_y))
            globals.map_textbox_changed = False

        def new_map():#TODO
            try:
                x, y = int(self.map_xcoord_entry.get()), int(self.map_ycoord_entry.get())
            except ValueError:
                self.map_coord_value_error_label.configure(text="Invalid coordinates")
                self.main_app.after(1000, lambda: self.map_coord_value_error_label.configure(text=""))
                self.map_xcoord_entry.delete(0, 'end')
                self.map_ycoord_entry.delete(0, 'end')
                self.map_xcoord_entry.focus_set()
                return
            confirm_popup = ConfirmPopUp("New map", f"Create new click coordinates for map ({x}, {y}) ?")
            confirm_popup.grab_set()
            self.main_app.wait_window(confirm_popup)
            if not confirm_popup.value:
                return
            click_popup = StartStopClickListening("Click Listener", self.main_app)
            self.main_app.wait_window(click_popup)
            if click_popup.click_coordinates:
                with open("data/maps.bin", "rb") as file:
                    try:
                        click_coordinates = pickle.load(file)
                    except EOFError:
                        click_coordinates = {}
            

        def delete_map():#TODO
            pass
        
        def save_map_changes():#TODO
            pass

        def reset_map_changes():#TODO /!\ map_textbox_changed variable !
            pass

        ####### Content
        ########## 1st column
        self.map_coordinates_label = ctk.CTkLabel(master=self.map_frame,
                                                  text="Map coordinates")
        self.map_coordinates_container = ctk.CTkFrame(master=self.map_frame,
                                                  bg_color=globals.SECONDARY_BACKGROUND_GRAY,
                                                  fg_color=globals.SECONDARY_BACKGROUND_GRAY)
        self.map_xcoord_label = ctk.CTkLabel(master=self.map_coordinates_container,
                                             text="X = ",
                                             bg_color=globals.SECONDARY_BACKGROUND_GRAY)
        self.map_xcoord_entry = ctk.CTkEntry(master=self.map_coordinates_container,
                                             bg_color=globals.SECONDARY_BACKGROUND_GRAY)
        self.map_ycoord_label = ctk.CTkLabel(master=self.map_coordinates_container,
                                             text="Y = ",
                                             bg_color=globals.SECONDARY_BACKGROUND_GRAY)
        self.map_ycoord_entry = ctk.CTkEntry(master=self.map_coordinates_container,
                                             bg_color=globals.SECONDARY_BACKGROUND_GRAY)
        self.map_coord_value_error_label = ctk.CTkLabel(master=self.map_coordinates_container,
                                                        text="")
        self.show_map_button = ctk.CTkButton(master=self.map_coordinates_container,
                                               text="Show map",
                                               command=show_map)

        ########## 2nd column
        self.map_click_coordinates_label = ctk.CTkLabel(master=self.map_frame,
                                                        text="Associated click coordinates")
        self.map_click_coordinates_textbox = ctk.CTkTextbox(master=self.map_frame,
                                                            height=100)
        # self.map_click_coordinates_textbox.trace_add("write",
        #                                              lambda *_: backend.set_map_textbox_changed(True))

        ########## 3rd column
        self.map_buttons_label = ctk.CTkLabel(master=self.map_frame,
                                              text="Map commands")
        self.map_buttons_container = ctk.CTkFrame(master=self.map_frame,
                                                  bg_color=globals.SECONDARY_BACKGROUND_GRAY,
                                                  fg_color=globals.SECONDARY_BACKGROUND_GRAY)
        self.add_map_button = ctk.CTkButton(master=self.map_buttons_container,
                                            text="New map",
                                            command=new_map)
        self.remove_map_button = ctk.CTkButton(master=self.map_buttons_container,
                                               text="Delete map",
                                               command=delete_map)
        self.save_map_changes_button = ctk.CTkButton(master=self.map_buttons_container,
                                             text="Save changes",
                                             command=save_map_changes)
        self.reset_map_changes_button = ctk.CTkButton(master=self.map_buttons_container,
                                                     text="Reset changes",
                                                     command=reset_map_changes)

        ####### Placement
        ########## 1st column
        self.map_coordinates_label.grid(column=0, row=0)
        self.map_xcoord_label.grid(column=0, row=0)
        self.map_xcoord_entry.grid(column=1, row=0)
        self.map_ycoord_label.grid(column=0, row=1)
        self.map_ycoord_entry.grid(column=1, row=1, pady=15)
        self.show_map_button.grid(column=0, row=2, pady=15, columnspan=2, sticky='e')
        self.map_coord_value_error_label.grid(column=0, row=3, pady=15, columnspan=2)
        self.map_coordinates_container.grid(column=0, row=1)

        ########## 2nd column
        self.map_click_coordinates_label.grid(column=1, row=0)
        self.map_click_coordinates_textbox.grid(column=1, row=1, pady=10, sticky='nsew')
        
        ########## 3rd column
        self.map_buttons_label.grid(column=2, row=0)
        self.add_map_button.grid(column=0, row=0, padx=10)
        self.remove_map_button.grid(column=0, row=1, pady=10)
        self.save_map_changes_button.grid(column=0, row=2, pady=10)
        self.reset_map_changes_button.grid(column=0, row=3)
        self.map_buttons_container.grid(column=2, row=1)

        ########## Map frame
        self.map_frame.grid(column=0, row=1, sticky='nsew', pady=5)

        ####### Post actions
        self.map_xcoord_entry.focus_set()


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
                                            fg_color=globals.DARK_RED,
                                            border_color=globals.CLEAR_RED,
                                            button_color=globals.CLEAR_RED)
                self.tab.after(1000, lambda: self.farming_path.configure(fg_color=globals.ENTRY_GRAY,
                                                                         border_color=globals.BORDER_GRAY,
                                                                         button_color=globals.BORDER_GRAY))
            else:
                self.farming_path.set(self.path_names[0])
                self.farming_path.configure(values=self.path_names,
                                            fg_color=globals.DARK_GREEN,
                                            border_color=globals.CLEAR_GREEN,
                                            button_color=globals.CLEAR_GREEN)
                self.tab.after(1000, lambda: self.farming_path.configure(fg_color=globals.ENTRY_GRAY,
                                                                         border_color=globals.BORDER_GRAY,
                                                                         button_color=globals.BORDER_GRAY))

        def show_path():#TODO
            pass

        def new_path():#TODO
            pass

        def delete_path():#TODO
            pass

        def save_path_changes():#TODO
            pass

        def reset_path_changes():#TODO
            pass

        ####### Content
        ########## 1st column
        self.farming_path_label = ctk.CTkLabel(master=self.path_frame,
                                               text="Farming path name")
        self.farming_path_container = ctk.CTkFrame(master=self.path_frame,
                                                   bg_color=globals.SECONDARY_BACKGROUND_GRAY,
                                                   fg_color=globals.SECONDARY_BACKGROUND_GRAY)
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
                                                   bg_color=globals.SECONDARY_BACKGROUND_GRAY,
                                                   fg_color=globals.SECONDARY_BACKGROUND_GRAY)
        self.add_path_button = ctk.CTkButton(master=self.path_buttons_container,
                                             text="New path",
                                             command=new_path)
        self.remove_path_button = ctk.CTkButton(master=self.path_buttons_container,
                                                text="Delete path",
                                                command=delete_path)
        self.save_path_changes_button = ctk.CTkButton(master=self.path_buttons_container,
                                                      text="Save changes",
                                                      command=save_path_changes)
        self.reset_path_changes_button = ctk.CTkButton(master=self.path_buttons_container,
                                                         text="Reset changes",
                                                         command=reset_path_changes)

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
        self.reset_path_changes_button.grid(column=0, row=3)
        self.path_buttons_container.grid(column=2, row=1)

        ########## Path frame
        self.path_frame.grid(column=0, row=2, sticky='nsew', pady=5)



class SettingsTabConstructor():

    def __init__(self, main_app: MainApplication, tab: ctk.CTkFrame):
        pass
        



class CharacterTabConstructor():

    def __init__(self, main_app: MainApplication, character_info):
        self.main_app = main_app
        self.character_name = character_info[0]
        self.character_tab = character_info[1]
        self.character_bot = character_info[2]


        

class PopUp(ctk.CTkToplevel):
    
    def __init__(self, title, width=300, height=200, duration=0):
        super().__init__()
        self.title(title)
        self.geometry(f"{width}x{height}")
        if duration:
            self.after(duration, self.destroy)
        self.bind("<Return>", lambda _: self.confirm())
        self.bind("<Escape>", lambda _: self.infirm())
    
    def confirm(self):
        self.destroy()

    def infirm(self):
        self.destroy()


class XYPopUp(PopUp):

    def __init__(self, title, target):
        super().__init__(title)
        self.x_value=None
        self.y_value=None
        self.configure(bg_color=globals.MAIN_BACKGROUND_GRAY, fg_color=globals.MAIN_BACKGROUND_GRAY)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        container = ctk.CTkFrame(self, fg_color=globals.MAIN_BACKGROUND_GRAY)
        ctk.CTkLabel(container, text=f"{target} X = ").grid(column=0, row=0, pady=(25, 0))
        self.x_entry = ctk.CTkEntry(container)
        self.x_entry.grid(column=1, row=0, pady=(25, 0))
        self.x_entry.focus_set()
        ctk.CTkLabel(container, text=f"{target} Y = ").grid(column=0, row=1)
        self.y_entry = ctk.CTkEntry(container)
        self.y_entry.grid(column=1, row=1, pady=15)
        ctk.CTkButton(container, text="Validate", command=self.confirm).grid(column=0, row=2, columnspan=2, pady=(15, 0), sticky='e')
        self.error_label = ctk.CTkLabel(container, text="")
        self.error_label.grid(row=3, column=0, columnspan=2, pady=10)
        container.grid()


    def confirm(self):
        if 1 <= len(self.x_entry.get()) <= 4 and 1 <= len(self.y_entry.get()) <= 4\
        and self.x_entry.get().replace("-", "").isdigit() and self.y_entry.get().replace("-", "").isdigit():
            self.x_value = int(self.x_entry.get())
            self.y_value = int(self.y_entry.get())
            self.destroy()
        else:
            self.x_entry.delete(0, 'end')
            self.y_entry.delete(0, 'end')
            self.x_entry.focus_set()
            self.error_label.configure(text="Invalid coordinates")
            self.after(1000, lambda: self.error_label.configure(text=""))


class ConfirmPopUp(PopUp):

    def __init__(self, title, text):
        super().__init__(title)
        self.value = None
        self.protocol("WM_DELETE_WINDOW", self.infirm)
        self.configure(bg_color=globals.MAIN_BACKGROUND_GRAY, fg_color=globals.MAIN_BACKGROUND_GRAY)
        self.grid_columnconfigure((0, 1), weight=1)
        self.grid_rowconfigure((0, 1), weight=1)
        ctk.CTkLabel(self, text=text).grid(column=0, row=0, columnspan=2)
        ctk.CTkButton(self, text="OK", command=self.confirm).grid(column=0, row=1, padx=10)
        ctk.CTkButton(self, text="Cancel", command=self.infirm).grid(column=1, row=1, padx=10)

    def confirm(self):
        self.value = True
        self.destroy()

    def infirm(self):
        self.value = False
        self.destroy()



class StartStopClickListening(PopUp):

    def __init__(self, title, main_app: MainApplication):
        super().__init__(title)
        self.geometry("400x300+-10+0")
        self.resizable(False, False)
        self.protocol("WM_DELETE_WINDOW", self.clean_close)
        self.main_app = main_app
        self.attributes("-topmost", True)
        self.configure(bg_color=globals.MAIN_BACKGROUND_GRAY, fg_color=globals.MAIN_BACKGROUND_GRAY)
        self.grid_columnconfigure((0, 1), weight=1)
        self.grid_rowconfigure(0, weight=2)
        self.grid_rowconfigure((1, 2), weight=1)
        self.click_coordinates_textbox = ctk.CTkTextbox(self, state="disabled")
        self.click_coordinates_textbox.grid(column=0, row=0, columnspan=2, pady=5, sticky="new")
        self.resume_button = ctk.CTkButton(self, text="Resume listening", state="disabled", command=lambda: self.after(100, self.resume_click_listening))
        self.resume_button.grid(column=0, row=1, pady=5, padx=5)
        self.pause_button = ctk.CTkButton(self, text="Pause listening", command=self.pause_click_listening)
        self.pause_button.grid(column=1, row=1, pady=5, padx=5)
        ctk.CTkButton(self, text="Validate coordinates", command=self.validate_click_coordinates).grid(column=0, row=2, columnspan=2, pady=10)

        self.click_coordinates = ""
        self.pause = False

        self.listener = mouse.Listener(on_click=self.on_click)
        self.listener.start()

    def clean_close(self):
        previous_pause = self.pause
        self.pause_click_listening()
        confirm_popup = ConfirmPopUp("Coordinates", "Give up coordinates ?")
        confirm_popup.attributes("-topmost", True)
        confirm_popup.grab_set()
        self.main_app.wait_window(confirm_popup)
        if confirm_popup.value:
            self.click_coordinates = ""
            self.listener.stop()
            self.destroy()
            return
        if not previous_pause:
            self.after(100, self.resume_click_listening)

    def register_click(self, x, y, pressed):
        if not self.pause:
            if pressed:
                x, y = int(x), int(y)
                coords = f"({x},{y});"
                self.click_coordinates += coords
                self.click_coordinates_textbox.configure(state="normal")
                self.click_coordinates_textbox.insert('end', coords+"\n")
                self.click_coordinates_textbox.configure(state="disabled")

    def on_click(self, x, y, _, pressed):
        self.after(50, self.register_click, x, y, pressed)

    def resume_click_listening(self):
        self.resume_button.configure(state="disabled")
        self.pause_button.configure(state="normal")
        self.pause = False

    def pause_click_listening(self):
        self.resume_button.configure(state="normal")
        self.pause_button.configure(state="disabled")
        self.pause = True

    def validate_click_coordinates(self):
        previous_pause = self.pause
        self.pause_click_listening()
        confirm_popup = ConfirmPopUp("Coordinates", "Add click coordinates to current map ?")
        confirm_popup.attributes("-topmost", True)
        confirm_popup.grab_set()
        self.main_app.wait_window(confirm_popup)
        if confirm_popup.value:
            self.listener.stop()
            self.destroy()
            return
        if not previous_pause:
            self.after(100, self.resume_click_listening)

        
        


        

app = MainApplication()
app.mainloop()



