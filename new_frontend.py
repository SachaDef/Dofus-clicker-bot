import customtkinter as ctk
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("dark-blue")
from CTkMessagebox import CTkMessagebox

import new_globals as globals
import new_backend as backend

import pynput.mouse as mouse

# ==== Main GUI window ==== #
class MainApplication(ctk.CTk):

    def __init__(self):
        super().__init__()

        # Global variables
        self.width  = 800
        self.height = 600
        
        # Initialization
        self.geometry(f"{self.width}x{self.height}")
        self.title("DofusBot")
        self.iconbitmap(r'img\icon.ico')
        self.minsize(self.width, self.height)
        backend.save_backup("open")
        self.protocol("WM_DELETE_WINDOW", self.clean_exit)
        self.after(5, lambda: self.state("zoomed"))

        # Tabs initialization
        self.tabs = ctk.CTkTabview(master=self)
        self.general_tab = self.tabs.add("General")
        self.settings_tab = self.tabs.add("Settings")
        self.tabs.set("General")
        self.tabs.pack(side=ctk.TOP, fill=ctk.BOTH, expand=True)

        # Tabs creation
        self.general_constructor = GeneralTabConstructor(self, self.general_tab)
        self.settings_constructor = SettingsTabConstructor(self, self.settings_tab)

        # Bindings
        self.bind("<Control-q>", lambda event: self.clean_exit())
        self.bind("<Button-1>", self.remove_focus)
        self.bind("<Escape>", lambda _: self.focus_set())
        self.bind("<Control-Return>", self.enter)
        self.bind("<Control-Left>", self.left)
        self.bind("<Control-Right>", self.right)
        self.bind("<Control-Up>", self.up)
        self.bind("<Control-Down>", self.down)
        self.bind("<Control-n>", self.n)
        self.bind("<Control-d>", self.d)
        self.bind("<Control-Shift-KeyPress-N>", self.N)
        self.bind("<Control-p>", self.print_sizes)

    # Methods
    def clean_exit(self):
        backend.save_backup("close")
        self.destroy()

    def print_sizes(self, _):
        map_frame = self.general_constructor.map_frame
        path_frame = self.general_constructor.path_frame
        print(map_frame.winfo_width(), map_frame.winfo_height())
        print(path_frame.winfo_width(), path_frame.winfo_height())

    def remove_focus(self, event):
        if event.widget not in (self.general_constructor.map_click_coordinates_textbox._textbox,
                                self.general_constructor.path_map_coordinates_textbox._textbox,
                                self.general_constructor.farming_path._entry,
                                self.general_constructor.map_xcoord_entry.entry._entry,
                                self.general_constructor.map_ycoord_entry.entry._entry):
            self.focus_set()

    def enter(self, event):
        match self.tabs.get():
            case "General":
                if event.widget not in (self.general_constructor.map_click_coordinates_textbox._textbox,
                                        self.general_constructor.path_map_coordinates_textbox._textbox)\
                and self.general_constructor.add_character_button._state == "normal":
                    self.general_constructor.add_character_button._command()
            

    def left(self, event):
        match self.tabs.get():
            case "General":
                if event.widget in (self.general_constructor.map_click_coordinates_textbox._textbox,
                                        self.general_constructor.path_map_coordinates_textbox._textbox,
                                        self.general_constructor.farming_path._entry):
                    return
                if globals.map_textbox_changed:
                    confirm_popup = ConfirmPopUp("Show map - Conflict", f"Discard edits made for map ({globals.displayed_map[0]}, {globals.displayed_map[1]}) ?")
                    confirm_popup.grab_set()
                    self.wait_window(confirm_popup)
                    if not confirm_popup.value:
                        return
                self.general_constructor.map_xcoord_entry.subtract()

    def right(self, event):
        match self.tabs.get():
            case "General":
                if event.widget in (self.general_constructor.map_click_coordinates_textbox._textbox,
                                        self.general_constructor.path_map_coordinates_textbox._textbox,
                                        self.general_constructor.farming_path._entry):
                    return
                if globals.map_textbox_changed:
                    confirm_popup = ConfirmPopUp("Show map - Conflict", f"Discard edits made for map ({globals.displayed_map[0]}, {globals.displayed_map[1]}) ?")
                    confirm_popup.grab_set()
                    self.wait_window(confirm_popup)
                    if not confirm_popup.value:
                        return
                self.general_constructor.map_xcoord_entry.add()

    def up(self, event):
        match self.tabs.get():
            case "General":
                if event.widget in (self.general_constructor.map_click_coordinates_textbox._textbox,
                                        self.general_constructor.path_map_coordinates_textbox._textbox,
                                        self.general_constructor.farming_path._entry):
                    return
                if globals.map_textbox_changed:
                    confirm_popup = ConfirmPopUp("Show map - Conflict", f"Discard edits made for map ({globals.displayed_map[0]}, {globals.displayed_map[1]}) ?")
                    confirm_popup.grab_set()
                    self.wait_window(confirm_popup)
                    if not confirm_popup.value:
                        return
                self.general_constructor.map_ycoord_entry.subtract()

    def down(self, event):
        match self.tabs.get():
            case "General":
                if event.widget in (self.general_constructor.map_click_coordinates_textbox._textbox,
                                        self.general_constructor.path_map_coordinates_textbox._textbox,
                                        self.general_constructor.farming_path._entry):
                    return
                if globals.map_textbox_changed:
                    confirm_popup = ConfirmPopUp("Show map - Conflict", f"Discard edits made for map ({globals.displayed_map[0]}, {globals.displayed_map[1]}) ?")
                    confirm_popup.grab_set()
                    self.wait_window(confirm_popup)
                    if not confirm_popup.value:
                        return
                self.general_constructor.map_ycoord_entry.add()

    def n(self, event):
        match self.tabs.get():
            case "General":
                self.general_constructor.add_map_button._command()
            case _:
                return

    def d(self, event):
        match self.tabs.get():
            case "General":
                self.general_constructor.remove_map_button._command()
            case _:
                return

    def N(self, event):
        match self.tabs.get():
            case "General":
                self.general_constructor.add_path_button._command()
            case _:
                return
            
    def set_button_freeze(self, button: str, value: bool):
        match button:
            case "refresh":
                globals.refresh_freeze = value
            case _:
                return
            
    def get_button_freeze(self, button: str) -> bool:
        match button:
            case "refresh":
                return globals.refresh_freeze
            case _:
                return False



class GeneralTabConstructor():

    def __init__(self, main_app: MainApplication, tab: ctk.CTkFrame):
        # Variables
        self.main_app = main_app
        self.tab = tab

        # Initialization
        self.tab.grid_columnconfigure(0, weight=1)
        self.tab.grid_rowconfigure(0, weight=1)
        self.tab.grid_rowconfigure(1, weight=2)
        self.tab.grid_rowconfigure(2, weight=2)
        # WARNING : the configuration doesn't split the rows' sizes according to the weight, it only splits the 
        # REMAINING EMPTY SPACE between them. Before the frames did not have the same dimensions, now fixed, so the
        # (1,2,2) ratio works normally
        self.character_frame = ctk.CTkFrame(master=self.tab)
        self.map_frame = ctk.CTkFrame(master=self.tab)
        self.path_frame = ctk.CTkFrame(master=self.tab)
        
        #### Character frame
        self.character_frame.grid_columnconfigure((0, 2), weight=10)
        self.character_frame.grid_columnconfigure(1, weight=16)
        self.character_frame.grid_rowconfigure(0, weight=1)

        ####### Methods
        def refresh_windows():
            if self.main_app.get_button_freeze("refresh"):
                return
            self.main_app.set_button_freeze("refresh", True)
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
            self.tab.after(1100, lambda: self.main_app.set_button_freeze("refresh", False))

        def validate_character():
            character_name = self.character_window_variable.get()
            if character_name in globals.active_character_names and\
            character_name not in backend.get_all_nth_from_list(globals.tracked_characters, 0):
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
            character_tab = self.main_app.tabs.add(character_name)
            character_info = (character_name, character_tab, character_bot)
            globals.tracked_characters.append(character_info)
            CharacterTabConstructor(self.main_app, character_info)
            validate_character()
            
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
        def get_xy() -> tuple[int, int] | None:
            if self.map_xcoord_entry.get() in ("", "-") or self.map_ycoord_entry.get() in ("", "-"):
                return
            try:
                map_x, map_y = int(self.map_xcoord_entry.get()), int(self.map_ycoord_entry.get())
                return map_x, map_y
            except ValueError:
                self.map_coord_value_error_label.configure(text="Invalid coordinates")
                self.main_app.after(1000, lambda: self.map_coord_value_error_label.configure(text=""))
                self.map_xcoord_entry.set("0")
                self.map_ycoord_entry.set("0")
                self.map_xcoord_entry.focus_set()
                return

        def show_map(x=None, y=None):
            if x is not None and y is not None:
                map_x, map_y = x, y
            else:
                try:
                    map_x, map_y = get_xy()
                except TypeError:
                    return
            # if globals.map_textbox_changed:
            #     confirm_popup = ConfirmPopUp("Show map - Conflict", f"Discard edits made for map ({globals.displayed_map[0]}, {globals.displayed_map[1]}) ?")
            #     confirm_popup.grab_set()
            #     self.main_app.wait_window(confirm_popup)
            #     if not confirm_popup.value:
            #         return
            backend.set_user_changing(False)
            self.map_click_coordinates_textbox.delete("1.0", 'end')
            self.map_click_coordinates_textbox.insert("1.0", backend.load_click_coordinates(map_x, map_y))
            self.map_click_coordinates_textbox.edit_modified(False)
            globals.map_textbox_changed = False
            self.main_app.after(100, lambda: backend.set_user_changing(True))
            globals.displayed_map = (map_x, map_y)
            self.map_click_coordinates_label.configure(text="Associated click coordinates")

        def new_map():
            try:
                map_x, map_y = get_xy()
            except TypeError:
                return
            if backend.click_coordinates_exist(map_x, map_y):
                confirm_popup2 = ConfirmPopUp("New map", "Already existing coordinates. Overwrite them ?")
                confirm_popup2.grab_set()
                self.main_app.wait_window(confirm_popup2)
                if not confirm_popup2.value:
                    return
            self.main_app.after(200, backend.new_map_foreground)
            click_popup = StartStopClickListening("Click Listener", self.main_app)
            click_popup.grab_set()
            self.main_app.wait_window(click_popup)
            if not click_popup.click_coordinates:
                return
            backend.save_click_coordinates(map_x, map_y, click_popup.click_coordinates)
            if (map_x, map_y) == globals.displayed_map:
                backend.set_user_changing(False)
                self.map_click_coordinates_textbox.edit_modified(False)
                globals.map_textbox_changed = False
                self.main_app.after(100, lambda: backend.set_user_changing(True))
                show_map(map_x, map_y)
            elif not globals.map_textbox_changed:
                show_map(map_x, map_y)

        def delete_map():
            try:
                map_x, map_y = get_xy()
            except TypeError:
                return
            if not backend.click_coordinates_exist(map_x, map_y):
                self.map_buttons_error_label.configure(text=f"No clicks for map ({map_x}, {map_y})")
                self.main_app.after(1000, lambda: self.map_buttons_error_label.configure(text=""))
                return
            confirm_popup = ConfirmPopUp("Delete map", f"Delete click coordinates for map ({map_x}, {map_y}) ?")
            confirm_popup.grab_set()
            self.main_app.wait_window(confirm_popup)
            if not confirm_popup.value:
                return
            backend.delete_click_coordinates(map_x, map_y)
            if (map_x, map_y) == globals.displayed_map:
                backend.set_user_changing(False)
                self.map_click_coordinates_textbox.edit_modified(False)
                globals.map_textbox_changed = False
                self.main_app.after(100, lambda: backend.set_user_changing(True))
                show_map(map_x, map_y)
        
        def save_map_edits():
            try:
                map_x, map_y = globals.displayed_map
            except ValueError:
                self.map_buttons_error_label.configure(text="No map displayed")
                self.main_app.after(1000, lambda: self.map_buttons_error_label.configure(text=""))
                return
            if not globals.map_textbox_changed:
                self.map_buttons_error_label.configure(text="No edits made")
                self.main_app.after(1000, lambda: self.map_buttons_error_label.configure(text=""))
                return
            textbox_click_coordinates = backend.str_to_list_coordinates(self.map_click_coordinates_textbox.get("1.0", "end"))
            if textbox_click_coordinates is None:
                self.map_buttons_error_label.configure(text=f"Invalid edits made")
                self.main_app.after(1000, lambda: self.map_buttons_error_label.configure(text=""))
                return
            confirm_popup = ConfirmPopUp("Edit map", f"Edit click coordinates for map ({map_x}, {map_y}) ?")
            confirm_popup.grab_set()
            self.main_app.wait_window(confirm_popup)
            if not confirm_popup.value:
                return
            backend.edit_click_coordinates(map_x, map_y, textbox_click_coordinates)
            backend.set_user_changing(False)
            self.map_click_coordinates_textbox.edit_modified(False)
            globals.map_textbox_changed = False
            self.main_app.after(100, lambda: backend.set_user_changing(True))
            self.map_click_coordinates_label.configure(text="Associated click coordinates")

        def reset_map_edits():
            try:
                map_x, map_y = globals.displayed_map
            except ValueError:
                self.map_buttons_error_label.configure(text="No map displayed")
                self.main_app.after(1000, lambda: self.map_buttons_error_label.configure(text=""))
                return
            if not globals.map_textbox_changed:
                self.map_buttons_error_label.configure(text="No edits made")
                self.main_app.after(1000, lambda: self.map_buttons_error_label.configure(text=""))
                return
            confirm_popup = ConfirmPopUp("Reset map", f"Discard edits made for map ({map_x}, {map_y}) ?")
            confirm_popup.grab_set()
            self.main_app.wait_window(confirm_popup)
            if not confirm_popup.value:
                return
            backend.set_user_changing(False)
            self.map_click_coordinates_textbox.edit_modified(False)
            globals.map_textbox_changed = False
            self.main_app.after(100, lambda: backend.set_user_changing(True))
            show_map(map_x, map_y)
        
        def textbox_modification():
            if globals.user_changing:
                globals.map_textbox_changed = True
                self.map_click_coordinates_label.configure(text="Associated click coordinates (*)")

            

        ####### Content
        ########## 1st column
        self.map_coordinates_label = ctk.CTkLabel(master=self.map_frame,
                                                  text="Map coordinates")
        self.map_coordinates_container = ctk.CTkFrame(master=self.map_frame,
                                                      bg_color=globals.SECONDARY_BACKGROUND_GRAY,
                                                      fg_color=globals.SECONDARY_BACKGROUND_GRAY)
        self.map_xcoord_label = ctk.CTkLabel(master=self.map_coordinates_container,
                                             text="X :   ",
                                             bg_color=globals.SECONDARY_BACKGROUND_GRAY)
        self.map_ycoord_label = ctk.CTkLabel(master=self.map_coordinates_container,
                                             text="Y :   ",
                                             bg_color=globals.SECONDARY_BACKGROUND_GRAY)
        # Legacy
        # self.map_xcoord_entry = ctk.CTkEntry(master=self.map_coordinates_container,
        #                                      bg_color=globals.SECONDARY_BACKGROUND_GRAY)
        # self.map_ycoord_entry = ctk.CTkEntry(master=self.map_coordinates_container,
        #                                      bg_color=globals.SECONDARY_BACKGROUND_GRAY)
        self.map_xcoord_entry = PlusMinusEntry(master=self.map_coordinates_container,
                                               bg_color=globals.SECONDARY_BACKGROUND_GRAY,
                                               fg_color=globals.SECONDARY_BACKGROUND_GRAY)
        self.map_ycoord_entry = PlusMinusEntry(master=self.map_coordinates_container,
                                               bg_color=globals.SECONDARY_BACKGROUND_GRAY,
                                               fg_color=globals.SECONDARY_BACKGROUND_GRAY)
        self.map_xcoord_entry.entry_variable.trace_add("write",
                                                       lambda *_: show_map())
        self.map_ycoord_entry.entry_variable.trace_add("write",
                                                       lambda *_: show_map())
        self.map_coord_value_error_label = ctk.CTkLabel(master=self.map_coordinates_container,
                                                        text="")

        ########## 2nd column
        self.map_click_coordinates_label = ctk.CTkLabel(master=self.map_frame,
                                                        text="Associated click coordinates")
        self.map_click_coordinates_textbox = ctk.CTkTextbox(master=self.map_frame,
                                                            height=100)
        self.map_click_coordinates_textbox.bind("<<Modified>>",
                                                lambda _: textbox_modification())
        self.map_click_coordinates_textbox.bind("<Control-s>", lambda _: save_map_edits())
        self.map_click_coordinates_textbox.bind("<Control-r>", lambda _: reset_map_edits())

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
        self.save_map_edits_button = ctk.CTkButton(master=self.map_buttons_container,
                                                     text="Save edits",
                                                     command=save_map_edits)
        self.reset_map_edits_button = ctk.CTkButton(master=self.map_buttons_container,
                                                      text="Reset edits",
                                                      command=reset_map_edits)
        self.map_buttons_error_label = ctk.CTkLabel(master=self.map_buttons_container,
                                                    text="",
                                                    width=100,
                                                    height=30,
                                                    wraplength=100,
                                                    justify=ctk.CENTER)        
        ####### Placement
        ########## 1st column
        self.map_coordinates_label.grid(column=0, row=0)
        self.map_xcoord_label.grid(column=0, row=0, pady=(50, 15))
        self.map_xcoord_entry.grid(column=1, row=0, pady=(50, 15))
        self.map_ycoord_label.grid(column=0, row=1)
        self.map_ycoord_entry.grid(column=1, row=1)
        self.map_coord_value_error_label.grid(column=0, row=2, pady=15, columnspan=2)
        self.map_coordinates_container.grid(column=0, row=1)

        ########## 2nd column
        self.map_click_coordinates_label.grid(column=1, row=0)
        self.map_click_coordinates_textbox.grid(column=1, row=1, pady=10, sticky='nsew')
        
        ########## 3rd column
        self.map_buttons_label.grid(column=2, row=0)
        self.add_map_button.grid(column=0, row=0, padx=17, pady=(30, 0))
        self.remove_map_button.grid(column=0, row=1, pady=10)
        self.save_map_edits_button.grid(column=0, row=2, pady=10)
        self.reset_map_edits_button.grid(column=0, row=3)
        self.map_buttons_error_label.grid(column=0, row=4, pady=(15, 0), sticky="s")
        self.map_buttons_container.grid(column=2, row=1)

        ########## Map frame
        self.map_frame.grid(column=0, row=1, sticky='nsew', pady=5)

        ####### Post actions
        # self.main_app.after(1000, lambda: print(f"container (0, 1) has width {self.map_coordinates_container.winfo_width()}"))
        # self.main_app.after(1000, lambda: print(f"container (2, 1) has width {self.map_buttons_container.winfo_width()}"))
        self.main_app.after(100, self.map_xcoord_entry.focus_set)
        show_map()


        #### Path frame
        self.path_frame.grid_columnconfigure((0, 2), weight=2)
        self.path_frame.grid_columnconfigure(1, weight=3)
        self.path_frame.grid_rowconfigure(0, weight=1)
        self.path_frame.grid_rowconfigure(1, weight=4)

        ####### Methods
        def refresh_paths():
            path_files = backend.get_all_paths(self.farming_path_variable.get())
            path_names = []
            for path in path_files:
                path_names.append(path.split("\\")[-1])
            
            if len(path_names) == 0:
                self.farming_path.configure(values=path_names,
                                            fg_color=globals.DARK_RED,
                                            border_color=globals.CLEAR_RED,
                                            button_color=globals.CLEAR_RED)
                self.tab.after(1000, lambda: self.farming_path.configure(fg_color=globals.ENTRY_GRAY,
                                                                         border_color=globals.BORDER_GRAY,
                                                                         button_color=globals.BORDER_GRAY))
            else:
                self.farming_path.set(path_names[0])
                self.farming_path.configure(values=path_names,
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

        def save_path_edits():#TODO
            pass

        def reset_path_edits():#TODO
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
        self.save_path_edits_button = ctk.CTkButton(master=self.path_buttons_container,
                                                      text="Save edits",
                                                      command=save_path_edits)
        self.reset_path_edits_button = ctk.CTkButton(master=self.path_buttons_container,
                                                         text="Reset edits",
                                                         command=reset_path_edits)
        self.path_buttons_error_label = ctk.CTkLabel(master=self.path_buttons_container,
                                                     text="",
                                                     width=100,
                                                     height=30,
                                                     wraplength=100,
                                                     justify=ctk.CENTER)

        ####### Placement
        ########## 1st column
        self.farming_path_label.grid(column=0, row=0)
        self.farming_path.grid(column=0, row=0, pady=15, padx=17)
        self.refresh_paths_button.grid(column=0, row=1, pady=15)
        self.show_path_button.grid(column=0, row=2)
        self.farming_path_container.grid(column=0, row=1)

        ########## 2nd column
        self.path_map_coordinates_label.grid(column=1, row=0)
        self.path_map_coordinates_textbox.grid(column=1, row=1, pady=10, sticky='nsew')

        ########## 3rd column
        self.path_buttons_label.grid(column=2, row=0)
        self.add_path_button.grid(column=0, row=0, padx=17, pady=(30, 0))
        self.remove_path_button.grid(column=0, row=1, pady=10)
        self.save_path_edits_button.grid(column=0, row=2, pady=10)
        self.reset_path_edits_button.grid(column=0, row=3)
        self.path_buttons_error_label.grid(column=0, row=4, pady=(15, 0), sticky="s")
        self.path_buttons_container.grid(column=2, row=1)

        ########## Path frame
        self.path_frame.grid(column=0, row=2, sticky='nsew', pady=5)

        ####### Post actions
        # self.main_app.after(1000, lambda: print(f"container (0, 2) has width {self.farming_path_container.winfo_width()}"))
        # self.main_app.after(1000, lambda: print(f"container (2, 1) has width {self.path_buttons_container.winfo_width()}"))



class SettingsTabConstructor():

    def __init__(self, main_app: MainApplication, tab: ctk.CTkFrame):
        pass
        



class CharacterTabConstructor():

    def __init__(self, main_app: MainApplication, character_info):
        self.main_app = main_app
        self.character_name = character_info[0]
        self.character_tab = character_info[1]
        self.character_bot = character_info[2]



class PlusMinusEntry(ctk.CTkFrame):

    def __init__(self, master, **kwargs):
        super().__init__(master=master, **kwargs)
        self.minus = ctk.CTkButton(master=self, text="-", width=30, command=self.subtract)
        self.entry_variable = ctk.StringVar(value="0")
        self.entry = ctk.CTkEntry(master=self, width=80, justify=ctk.CENTER, textvariable=self.entry_variable)
        self.plus = ctk.CTkButton(master=self, text="+", width=30, command=self.add)
        self.minus.grid(row=0, column=0)
        self.entry.grid(row=0, column=1, padx=5)
        self.plus.grid(row=0, column=2)
    
    def subtract(self):
        try:
            self.minus.focus_set()
            new_value = int(self.entry.get()) - 1
            self.entry_variable.set(str(new_value))
        except ValueError:
            raise ValueError
    
    def add(self):
        try:
            self.plus.focus_set()
            new_value = int(self.entry.get()) + 1
            self.entry_variable.set(str(new_value))
        except ValueError:
            raise ValueError
    
    def set(self, text):
        self.entry_variable.set(text)
        
    def get(self):
        return self.entry_variable.get()
    
    def focus_set(self):
        self.entry.focus_set()



        

class PopUp(ctk.CTkToplevel):
    
    def __init__(self, title, width=300, height=200, duration=0):
        super().__init__()
        screenw = self.winfo_screenwidth()
        screenh = self.winfo_screenheight()
        self.title(title)
        self.geometry(f"{width}x{height}+{int(screenw/2-width/2)-40}+{int(screenh/2-height/2)-80}")
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
        self.after(5, self.x_entry.focus_set)
        ctk.CTkLabel(container, text=f"{target} Y = ").grid(column=0, row=1)
        self.y_entry = ctk.CTkEntry(container)
        self.y_entry.grid(column=1, row=1, pady=(15, 0))
        ctk.CTkButton(container, text="Validate", command=self.confirm).grid(column=0, row=2, columnspan=2, pady=(15, 0), sticky='e')
        self.error_label = ctk.CTkLabel(container, text="")
        self.error_label.grid(row=3, column=0, columnspan=2)
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
        self.protocol("WM_DELETE_WINDOW", self.infirm)
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
        ctk.CTkButton(self, text="Validate coordinates", command=self.confirm).grid(column=0, row=2, columnspan=2, pady=10)

        self.click_coordinates = ""
        self.pause = False

        self.listener = mouse.Listener(on_click=self.on_click)
        self.listener.start()

# Legacy
# clean close with a pop-up asking before giving coordinates up, may be useful
    # def clean_close(self):
    #     previous_pause = self.pause
    #     self.pause_click_listening()
    #     confirm_popup = ConfirmPopUp("Coordinates", "Give up coordinates ?")
    #     confirm_popup.attributes("-topmost", True)
    #     confirm_popup.grab_set()
    #     self.main_app.wait_window(confirm_popup)
    #     if confirm_popup.value:
    #         self.click_coordinates = ""
    #         self.listener.stop()
    #         self.destroy()
    #         return
    #     if not previous_pause:
    #         self.after(100, self.resume_click_listening)

# Current
# clean close without asking beofre giving up
    def infirm(self):
        self.click_coordinates = ""
        self.listener.stop()
        self.destroy()
        return
    
# Legacy
# validate with a pop-up asking before adding, may be useful
    # def validate_click_coordinates(self):
    #     previous_pause = self.pause
    #     self.pause_click_listening()
    #     confirm_popup = ConfirmPopUp("Coordinates", "Add click coordinates to current map ?")
    #     confirm_popup.attributes("-topmost", True)
    #     confirm_popup.grab_set()
    #     self.main_app.wait_window(confirm_popup)
    #     if confirm_popup.value:
    #         self.listener.stop()
    #         self.destroy()
    #         return
    #     if not previous_pause:
    #         self.after(100, self.resume_click_listening)

# Current    
# validate without asking beofre adding
    def confirm(self):
        self.listener.stop()
        self.destroy()
        return

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
        self.after(50, lambda: self.register_click(x, y, pressed))

    def resume_click_listening(self):
        self.resume_button.configure(state="disabled")
        self.pause_button.configure(state="normal")
        self.pause = False

    def pause_click_listening(self):
        self.resume_button.configure(state="normal")
        self.pause_button.configure(state="disabled")
        self.pause = True

        
if __name__ == "__main__":
    app = MainApplication()
    app.mainloop()



