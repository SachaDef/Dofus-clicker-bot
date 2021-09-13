from ctypes import *
from win32gui import PostMessage
from win32api import MAKELONG
from win32con import WM_LBUTTONDOWN, WM_LBUTTONUP, MK_LBUTTON
from threading import Thread
from time import sleep
import globals as gl

# ==== ALLOW PARTIAL MATCHES WHILE FINDING WINDOW ==== #
EnumWindows = windll.user32.EnumWindows
EnumWindowsProc = WINFUNCTYPE(c_bool, c_int, POINTER(c_int))
GetWindowTextW = windll.user32.GetWindowTextW
GetWindowTextLength = windll.user32.GetWindowTextLengthW
IsWindowVisible = windll.user32.IsWindowVisible
GetClassName = windll.user32.GetClassNameW

titles = []

def foreach_window(hwnd, _):
    if IsWindowVisible(hwnd):
        classname = create_unicode_buffer(100 + 1)
        GetClassName(hwnd, classname, 100 + 1)
        length = GetWindowTextLength(hwnd)
        buff = create_unicode_buffer(length + 1)
        GetWindowTextW(hwnd, buff, length + 1)
        titles.append((hwnd, buff.value, classname.value))
    return True

def refresh_wins():
    del titles[:]
    # noinspection PyTypeChecker
    EnumWindows(EnumWindowsProc(foreach_window), 0)
    return titles

def find_window(title):
    newest_titles = refresh_wins()
    for item in newest_titles:
        if title.lower() in item[1].lower():
            return item
    return False


# ==== BOT INITIALIZATION ==== #
class DofusBot:
    def __init__(self, x_pos, y_pos, char_name):
        self.traveling = False
        self.creating = False
        self.character_name = char_name
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.x_dest = 0
        self.y_dest = 0
        self.previous_map = None
        self.travel_thread = None
        self.cancel_flag = False
        self.cancel_thread = None
        self.window_hwnd = find_window(char_name)[0]
        self.window_name = find_window(char_name)[1]
        self.window_class = find_window(char_name)[2]
        self.character_name = self.window_name.split(" - ")[0]
        self.click_coords = []
        self.maps_file = "..\\Maps_Paths\\farming_maps.txt"


# ==== START/STOP METHODS ==== #
    def travel_start(self):
        self.traveling = True
        self.travel_thread = Thread(target=self.travel_complete)

    def travel_stop(self):
        self.traveling = False
        self.travel_thread = None

    def creation_start(self):
        self.creating = True

    def creation_stop(self):
        self.creating = False

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
        lParam = MAKELONG(x, y)
        PostMessage(self.window_hwnd, WM_LBUTTONDOWN, MK_LBUTTON, lParam)
        sleep(0.05)
        PostMessage(self.window_hwnd, WM_LBUTTONUP, MK_LBUTTON, lParam)

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
        self.click(1400, 430)
        self.previous_map = 'r'

    def move_left(self):
        if self.cancel_flag and self.previous_map != 'l':
            self.wrong_movement_modif()
        self.x_pos -= 1
        self.cancel_thread = Thread(target=self.wait_3_sec)
        self.cancel_thread.start()
        self.click(150, 430)
        self.previous_map = 'l'

    def move_up(self):
        if self.cancel_flag and self.previous_map != 'u':
            self.wrong_movement_modif()
        self.y_pos -= 1
        self.cancel_thread = Thread(target=self.wait_3_sec)
        self.cancel_thread.start()
        self.click(750, 10)
        self.previous_map = 'u'

    def move_down(self):
        if self.cancel_flag and self.previous_map != 'd':
            self.wrong_movement_modif()
        self.y_pos += 1
        self.cancel_thread = Thread(target=self.wait_3_sec)
        self.cancel_thread.start()
        self.click(800, 710)
        self.previous_map = 'd'

    def reset(self):
        if self.cancel_flag:
            self.wrong_movement_modif()
            self.click(960, 480)            
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
                    gl.popQ.MyPut("endTr")
                    gl.popQ.open = False
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
                    gl.popQ.MyPut("endTr")
                    gl.popQ.open = False
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
                    gl.popQ.MyPut("endTr")
                    gl.popQ.open = False
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
                    gl.popQ.MyPut("endTr")
                    gl.popQ.open = False
                if self.traveling:
                    sleep(5)
                self.cancel_thread = None

    def travel_complete(self):
        if self.traveling:
            self.travel_vertical(self.y_dest - self.y_pos)
            self.travel_horizontal(self.x_dest - self.x_pos)
            self.travel_stop()
            return

    def automate_travel(self):
        if self.travel_thread is not None:
            self.travel_thread.start()
