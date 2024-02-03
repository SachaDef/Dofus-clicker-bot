import new_globals as globals
import win32gui, win32api, win32con
import os
import time
import pyautogui as pag
import threading
import pynput.mouse as m
import pickle

# ==== GLOBAL UTILS ==== #
def get_all_nth_from_list(iterable, index):
    return [subiterable[index] for subiterable in iterable]

# Button freeze functionalities
def set_button_freeze(button: str, value: bool):
    match button:
        case "refresh":
            globals.refresh_freeze = value
        case "map_xy":
            globals.map_xy_freeze = value
        case "popup_xy":
            globals.popup_xy_freeze = value
        case _:
            return
        
def get_button_freeze(button: str) -> bool:
    match button:
        case "refresh":
            return globals.refresh_freeze
        case "map_xy":
            return globals.map_xy_freeze
        case "popup_xy":
            return globals.popup_xy_freeze
        case _:
            return False

# ==== WINDOW HANDLING ==== #
# Get active windows
def winEnumHandler(window_handle: int, _) -> None:      # Copied from https://stackoverflow.com/questions/61865399/win32gui-shows-some-windows-that-are-not-open
    if win32gui.IsWindowVisible(window_handle) and win32gui.GetWindowText(window_handle) != '':
        globals.DwmGetWindowAttribute(globals.HWND(window_handle),
                                     globals.DWORD(globals.DWMWA_CLOAKED),
                                     globals.byref(globals.isCloacked),
                                     globals.sizeof(globals.isCloacked))
        title: str = win32gui.GetWindowText(window_handle)
        if (globals.isCloacked.value == 0):
            globals.active_windows.append((window_handle, title))

# Filter out non-dofus windows
def window_filtering() -> None:
    globals.active_windows = []
    win32gui.EnumWindows(winEnumHandler, None)
    globals.active_windows = [window for window in globals.active_windows if "Dofus 2" in window[1]]
    globals.active_character_names = [window[1].split(" - ")[0] for window in globals.active_windows]

# Get window handle from given character name
Window = tuple[()] | tuple[int, str]
def get_character_window(character_name: str) -> Window:
    for window in globals.active_windows:
        if window[1].startswith(character_name):
            return window
    return ()

# Set dofus as foreground window
def new_map_foreground():
    window_filtering()
    if not globals.active_windows:
        return
    win = globals.active_windows[0][0]
    win32gui.SetForegroundWindow(win)


# ==== MAP & CLICKS ==== #
MapCoords = tuple[int, int]
ScreenCoords = tuple[int, int]
Clicks = list[ScreenCoords]

# Get click coordinates associated to map coordinates from file
def load_click_coordinates(x: int, y: int) -> str:
    with open("data/maps.bin", "rb") as file:
        try:
            click_coordinates: dict[MapCoords, Clicks] = pickle.load(file)   #TODO cache ?
        except EOFError:
            return "No click coordinates for this map yet !"
    click_coordinates = click_coordinates.get((x, y))
    if click_coordinates is None:
        return "No click coordinates for this map yet !"
    click_coordinates_as_text = ["("+str(a)+", "+str(b)+")" for a, b in click_coordinates]
    return '\n'.join(click_coordinates_as_text)

# Check if click coordinates exist for given map in file
def click_coordinates_exist(x: int, y: int) -> bool:
    with open("data/maps.bin", "rb") as file:
        try:
            click_coordinates: dict[MapCoords, Clicks] = pickle.load(file)   #TODO cache ?
        except EOFError:
            return False
        return (x, y) in click_coordinates.keys()

# Save click coordinates for given map in file
def save_click_coordinates(x: int, y: int, coordinates: str) -> None:
    with open("data/maps.bin", "rb") as file:
        try:
            click_coordinates: dict[MapCoords, Clicks] = pickle.load(file)
        except EOFError:
            click_coordinates: dict[MapCoords, Clicks] = {}

    coordinates = coordinates.split(";")[:-1]
    coordinates_list = []
    for coordinate in coordinates:
        x_click, y_click = coordinate.replace("(", "").replace(")", "").split(",")
        coordinates_list.append((int(x_click), int(y_click)))
    click_coordinates[(x, y)] = coordinates_list

    with open("data/maps.bin", "wb") as file:
        pickle.dump(click_coordinates, file)

# Delete click coordinates for given map in file
def delete_click_coordinates(x: int, y: int) -> None:
    with open("data/maps.bin", "rb") as file:
        try:
            click_coordinates: dict[MapCoords, Clicks] = pickle.load(file)
        except EOFError:
            click_coordinates: dict[MapCoords, Clicks] = {}

    try:
        del click_coordinates[(x, y)]
    except KeyError:
        return

    with open("data/maps.bin", "wb") as file:
        pickle.dump(click_coordinates, file)

# Get click coordinates as list from textbox string
def str_to_list_coordinates(click_text: str) -> Clicks | None:
    try:
        return [(int(coord.replace("(", "").replace(")", "").split(",")[0].strip()),\
                 int(coord.replace("(", "").replace(")", "").split(",")[1].strip()))\
                for coord in click_text.strip().split("\n")]    
    except (IndexError, ValueError):
        return None
    
def set_user_changing(value: bool) -> None:
    globals.user_changing = value

# Legacy
# Now using the modified flag of the textbox widget
# Check wether the clicks have been modified or not
# def map_textbox_content_changed(x: int, y: int, textbox_click_coordinates: Clicks) -> bool:    
#     with open("data/maps.bin", "rb") as file:
#         try:
#             file_click_coordinates: dict[MapCoords, Clicks] = pickle.load(file)
#         except EOFError:
#             file_click_coordinates: dict[MapCoords, Clicks] = {}

#     print(file_click_coordinates[(x, y)])
#     print(textbox_click_coordinates)
#     print(file_click_coordinates[(x, y)] == textbox_click_coordinates)
#     return file_click_coordinates[(x, y)] == textbox_click_coordinates

def edit_click_coordinates(x: int, y: int, textbox_click_coordinates: Clicks) -> None:
    with open("data/maps.bin", "rb") as file:
        try:
            click_coordinates: dict[MapCoords, Clicks] = pickle.load(file)
        except EOFError:
            click_coordinates: dict[MapCoords, Clicks] = {}

    click_coordinates[(x, y)] = textbox_click_coordinates

    with open("data/maps.bin", "wb") as file:
        pickle.dump(click_coordinates, file)


# ==== PATHS & MAPS ==== #
# Get all path files
def get_all_paths(string_filter: str) -> list[str]:
    orig_dir = os.getcwd()
    os.chdir("data/paths")
    root_dir = os.getcwd()
    path_files = os.listdir()
    os.chdir(orig_dir)
    return [root_dir+"\\"+path_file.replace(".bin", "") for path_file in path_files if (".bin" in path_file and
                                                                    (path_file.startswith(string_filter) or string_filter == "Farming path"))]


# ==== SAFE EXIT ==== #
# Save backup data before app closing
def save_backup(type: str) -> None:
    program_root = os.getcwd()

    for root, _, files in os.walk("data"):
        if root == "data":
            for filename in files:
                data_filename = os.path.join(program_root, "data", filename)
                backup_filename = os.path.join(program_root, f"backup_{type}", filename)
                with open(data_filename, "rb") as data_file:
                    try:
                        data = pickle.load(data_file)
                    except EOFError:
                        continue
                with open(backup_filename, "wb") as backup_file:
                    pickle.dump(data, backup_file)
        elif root == "data\\paths":
            for filename in files:
                data_filename = os.path.join(program_root, "data\\paths", filename)
                backup_filename = os.path.join(program_root, f"backup_{type}\\paths", filename)
                with open(data_filename, "rb") as data_file:
                    try:
                        data = pickle.load(data_file)
                    except EOFError:
                        continue
                with open(backup_filename, "wb") as backup_file:
                    pickle.dump(data, backup_file)
    



# Automatisation bot
class CharacterBot():

    def __init__(self, char_name, x_pos, y_pos, window_handle):
        self.traveling = False
        self.creating = False
        self.mapfarming = False
        self.pathfarming = False
        self.character_name = char_name
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.x_dest = 0
        self.y_dest = 0
        self.previous_map = None
        self.travel_thread = None
        self.mapfarm_thread = None
        self.pathfarm_thread = None
        self.cancel_thread = None
        self.cancel_flag = False
        self.window_hwnd = window_handle
        self.click_coords = ""
        self.maps_file = r"data\maps.bin"


# ==== START/STOP METHODS ==== #
    def travel_start(self):
        self.traveling = True
        self.travel_thread = threading.Thread(target=self.travel_complete)
        self.travel_thread.start()

    def travel_stop(self):
        self.traveling = False
        self.travel_thread = None

    def creation_start(self):
        self.creating = True
        self.click_listener()

    def creation_stop(self):
        self.creating = False

    def mapfarming_start(self):
        self.mapfarming = True
        self.mapfarm_thread = threading.Thread(target=self.farm_map)
        self.mapfarm_thread.start()

    def mapfarming_stop(self):
        self.mapfarming = False
        self.mapfarm_thread = None

    def pathfarming_start(self, arg):
        self.pathfarming = True
        self.pathfarm_thread = threading.Thread(target=self.farm_path, args=(arg,))
        self.pathfarm_thread.start()

    def pathfarming_stop(self):
        self.pathfarming = False
        self.pathfarm_thread = None

    def exit(self):
        self.travel_stop()
        self.creation_stop()


# ==== POSITION/DESTINATION MODIFICATION METHODS ==== #
    def set_pos(self, coords):
        self.x_pos = coords[0]
        self.y_pos = coords[1]

    def set_dest(self, coords):
        self.x_dest = coords[0]
        self.y_dest = coords[1]


# ==== CLICKING METHOD ==== #
    def click(self, x, y):
        lParam = win32api.MAKELONG(x, y-28)
        win32gui.PostMessage(self.window_hwnd, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, lParam)
        time.sleep(0.05)
        win32gui.PostMessage(self.window_hwnd, win32con.WM_LBUTTONUP, win32con.MK_LBUTTON, lParam)

# ==== MOVEMENT BY CLICK METHODS ==== #
    def wrong_movement_modif(self):
        if self.previous_map == 'u':
            self.y_pos += 1
        if self.previous_map == 'd':
            self.y_pos -= 1
        if self.previous_map == 'l':
            self.x_pos += 1
        if self.previous_map == 'r':
            self.x_pos -= 1
        self.previous_map = None

    def wait_3_sec(self):
        self.cancel_flag = True
        time.sleep(3)
        self.cancel_flag = False

    def move_right(self):
        if self.cancel_flag and self.previous_map != 'r':
            self.wrong_movement_modif()
        self.x_pos += 1
        self.cancel_thread = threading.Thread(target=self.wait_3_sec)
        self.cancel_thread.start()
        self.click(1650, 410)
        self.previous_map = 'r'

    def move_left(self):
        if self.cancel_flag and self.previous_map != 'l':
            self.wrong_movement_modif()
        self.x_pos -= 1
        self.cancel_thread = threading.Thread(target=self.wait_3_sec)
        self.cancel_thread.start()
        self.click(300, 530)
        self.previous_map = 'l'

    def move_up(self):
        if self.cancel_flag and self.previous_map != 'u':
            self.wrong_movement_modif()
        self.y_pos -= 1
        self.cancel_thread = threading.Thread(target=self.wait_3_sec)
        self.cancel_thread.start()
        self.click(1020, 40)
        self.previous_map = 'u'

    def move_down(self):
        if self.cancel_flag and self.previous_map != 'd':
            self.wrong_movement_modif()
        self.y_pos += 1
        self.cancel_thread = threading.Thread(target=self.wait_3_sec)
        self.cancel_thread.start()
        self.click(900, 900)
        self.previous_map = 'd'

    def reset(self):
        if self.cancel_flag:
            self.wrong_movement_modif()
            self.click(960, 470)
            self.travel_stop()

# ==== MOVEMENT AUTOMATION METHODS ==== #
    def travel_vertical(self, value):
        if value == 0:
            return
        if value < 0:
            for i in range(abs(value)):
                if not self.traveling:
                    return
                self.move_up()
                time.sleep(3)
                if self.x_pos == self.x_dest and self.y_pos == self.y_dest:
                    pass
                    # gl.popQ.MyPut("endTr")
                    # gl.popQ.open = False
                if self.traveling:
                    time.sleep(5)
                self.cancel_thread = None
        else:
            for i in range(value):
                if not self.traveling:
                    return
                self.move_down()
                time.sleep(3)
                if self.x_pos == self.x_dest and self.y_pos == self.y_dest:
                    pass
                    # gl.popQ.MyPut("endTr")
                    # gl.popQ.open = False
                if self.traveling:
                    time.sleep(5)
                self.cancel_thread = None

    def travel_horizontal(self, value):
        if value == 0:
            return
        if value < 0:
            for i in range(abs(value)):
                if not self.traveling:
                    return
                self.move_left()
                time.sleep(3)
                if self.x_pos == self.x_dest and self.y_pos == self.y_dest:
                    pass
                    # gl.popQ.MyPut("endTr")
                    # gl.popQ.open = False
                if self.traveling:
                    time.sleep(5)
                self.cancel_thread = None
        else:
            for i in range(value):
                if not self.traveling:
                    return
                self.move_right()
                time.sleep(3)
                if self.x_pos == self.x_dest and self.y_pos == self.y_dest:
                    pass
                    # gl.popQ.MyPut("endTr")
                    # gl.popQ.open = False
                if self.traveling:
                    time.sleep(5)
                self.cancel_thread = None

    def travel_complete(self):
        if self.traveling:
            self.travel_vertical(self.y_dest - self.y_pos)
            self.travel_horizontal(self.x_dest - self.x_pos)
            self.travel_stop()
            return

# ==== MAP CREATION METHODS ==== #
    def click_listener(self):

        def on_click(x, y, _, pressed):
            if self.creating:
                if pressed:
                    x, y = int(x), int(y)
                    self.click_coords += f"({x},{y});"
            else:
                return False

        def on_move(x, y):
            if not self.creating:
                return False
        listener =  m.Listener(on_click=on_click, on_move=on_move)
        listener.start()

# ==== AUTOMATE FARMING METHODS ==== #
    def farm_map(self):
        flag = False
        with open(self.maps_file, "r") as f:
            for line in f.readlines():
                map, coords = line.split(":")
                if map == str((self.x_pos, self.y_pos)):
                    flag = True
                    coords = coords.split(";")[:-1]
                    pag.keyDown("shift")
                    for coord in coords:
                        x, y = int(coord.split(",")[0][1:]), int(coord.split(",")[1][:-1])
                        self.click(x, y)
                        time.sleep(0.1)
                    pag.keyUp("shift")
                    break
                else:
                    continue
            if not flag:
                pass
                # gl.popQ.MyPut("noMap")
        return len(coords)
        
    def farm_path(self, path_file):
        path_file = "data\\paths\\"+path_file+".bin"
        with open(path_file, "r") as f:
            for line in f.readlines():
                line = line.strip()
                mapx, mapy = line.split(',')
                mapx, mapy = int(mapx), int(mapy)
                print(mapx, mapy)
                if (mapx, mapy) != (self.x_pos, self.y_pos):
                    print("traveling")
                    self.set_dest((mapx, mapy))
                    self.travel_start()
                    while self.traveling:
                        time.sleep(1)
                count = self.farm_map()
                time.sleep(7 + count*3)
