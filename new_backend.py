import win32gui
import os
from time import sleep
import pyautogui as pag
from threading import Thread
from win32api import MAKELONG
from win32con import WM_LBUTTONDOWN, WM_LBUTTONUP, MK_LBUTTON
import pynput.mouse as m

from ctypes import c_int, WinDLL, byref, sizeof
from ctypes.wintypes import HWND, DWORD
dwmapi = WinDLL("dwmapi")
DWMWA_CLOAKED = 14 
isCloacked = c_int(0)


# Get active windows
def winEnumHandler(window_handle, _):      # Copied from https://stackoverflow.com/questions/61865399/win32gui-shows-some-windows-that-are-not-open
    if win32gui.IsWindowVisible(window_handle) and win32gui.GetWindowText(window_handle) != '':
        dwmapi.DwmGetWindowAttribute(HWND(window_handle),
                                        DWORD(DWMWA_CLOAKED),
                                        byref(isCloacked),
                                        sizeof(isCloacked))
        title = win32gui.GetWindowText(window_handle)
        if (isCloacked.value == 0):
            windows.append((window_handle, title))

# Filter active windows
def window_filtering():
    global windows
    windows = []
    win32gui.EnumWindows(winEnumHandler, None)
    windows = [window for window in windows if "Dofus 2" in window[1]]
    character_names = [window[1].split(" - ")[0] for window in windows]
    return windows, character_names

# Get all path files
def get_all_paths(string_filter):
    orig_dir = os.getcwd()
    os.chdir("data/paths")
    root_dir = os.getcwd()
    path_files = os.listdir()
    os.chdir(orig_dir)
    return [root_dir+"\\"+path_file.replace(".txt", "") for path_file in path_files if (".txt" in path_file and
                                                                    (path_file.startswith(string_filter) or string_filter == "Farming path"))]
    



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
        self.maps_file = r"data\maps.txt"


# ==== START/STOP METHODS ==== #
    def travel_start(self):
        self.traveling = True
        self.travel_thread = Thread(target=self.travel_complete)
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
        self.mapfarm_thread = Thread(target=self.farm_map)
        self.mapfarm_thread.start()

    def mapfarming_stop(self):
        self.mapfarming = False
        self.mapfarm_thread = None

    def pathfarming_start(self, arg):
        self.pathfarming = True
        self.pathfarm_thread = Thread(target=self.farm_path, args=(arg,))
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
        lParam = MAKELONG(x, y-28)
        win32gui.PostMessage(self.window_hwnd, WM_LBUTTONDOWN, MK_LBUTTON, lParam)
        sleep(0.05)
        win32gui.PostMessage(self.window_hwnd, WM_LBUTTONUP, MK_LBUTTON, lParam)

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
        sleep(3)
        self.cancel_flag = False

    def move_right(self):
        if self.cancel_flag and self.previous_map != 'r':
            self.wrong_movement_modif()
        self.x_pos += 1
        self.cancel_thread = Thread(target=self.wait_3_sec)
        self.cancel_thread.start()
        self.click(1650, 410)
        self.previous_map = 'r'

    def move_left(self):
        if self.cancel_flag and self.previous_map != 'l':
            self.wrong_movement_modif()
        self.x_pos -= 1
        self.cancel_thread = Thread(target=self.wait_3_sec)
        self.cancel_thread.start()
        self.click(300, 530)
        self.previous_map = 'l'

    def move_up(self):
        if self.cancel_flag and self.previous_map != 'u':
            self.wrong_movement_modif()
        self.y_pos -= 1
        self.cancel_thread = Thread(target=self.wait_3_sec)
        self.cancel_thread.start()
        self.click(1020, 40)
        self.previous_map = 'u'

    def move_down(self):
        if self.cancel_flag and self.previous_map != 'd':
            self.wrong_movement_modif()
        self.y_pos += 1
        self.cancel_thread = Thread(target=self.wait_3_sec)
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
                sleep(3)
                if self.x_pos == self.x_dest and self.y_pos == self.y_dest:
                    pass
                    # gl.popQ.MyPut("endTr")
                    # gl.popQ.open = False
                if self.traveling:
                    sleep(5)
                self.cancel_thread = None
        else:
            for i in range(value):
                if not self.traveling:
                    return
                self.move_down()
                sleep(3)
                if self.x_pos == self.x_dest and self.y_pos == self.y_dest:
                    pass
                    # gl.popQ.MyPut("endTr")
                    # gl.popQ.open = False
                if self.traveling:
                    sleep(5)
                self.cancel_thread = None

    def travel_horizontal(self, value):
        if value == 0:
            return
        if value < 0:
            for i in range(abs(value)):
                if not self.traveling:
                    return
                self.move_left()
                sleep(3)
                if self.x_pos == self.x_dest and self.y_pos == self.y_dest:
                    pass
                    # gl.popQ.MyPut("endTr")
                    # gl.popQ.open = False
                if self.traveling:
                    sleep(5)
                self.cancel_thread = None
        else:
            for i in range(value):
                if not self.traveling:
                    return
                self.move_right()
                sleep(3)
                if self.x_pos == self.x_dest and self.y_pos == self.y_dest:
                    pass
                    # gl.popQ.MyPut("endTr")
                    # gl.popQ.open = False
                if self.traveling:
                    sleep(5)
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
                        sleep(0.1)
                    pag.keyUp("shift")
                    break
                else:
                    continue
            if not flag:
                pass
                # gl.popQ.MyPut("noMap")
        return len(coords)
        
    def farm_path(self, path_file):
        path_file = "data\\paths\\"+path_file+".txt"
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
                        sleep(1)
                count = self.farm_map()
                sleep(7 + count*3)
