from ctypes import *
from pynput.mouse import Controller, Button
from win32gui import GetWindowText, GetForegroundWindow, SetForegroundWindow, SetActiveWindow, BringWindowToTop
from time import sleep
from Utilities.utilities_message_boxes import ConfirmBox
from threading import Thread, Lock


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
        if title in item[1]:
            return item
    return False


# ==== BRING WINDOW TO TOP ==== #
def to_top(hwnd):
    SetActiveWindow(hwnd)
    SetForegroundWindow(hwnd)
    BringWindowToTop(hwnd)


# ==== BOT INITIALIZATION ==== #
class DofusBot:
    def __init__(self, x_pos, y_pos):
        self.traveling = False
        self.creating = False
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.x_dest = 0
        self.y_dest = 0
        self.previous_map = None
        self.cancel_flag = False
        self.window_id = find_window("Dofus")[0]
        self.window_name = find_window("Dofus")[1]
        self.window_class = find_window("Dofus")[2]
        self.mouse = Controller()
        self.click_coords = []
        self.maps_file = "..\\Maps_Paths\\farming_maps.txt"


# ==== START/STOP METHODS ==== #
    def travel_start(self):
        self.traveling = True

    def travel_stop(self):
        self.traveling = False

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
        sleep(0.07)
        prev_coords = self.mouse.position
        self.mouse.position = (round(100/125*x), round(100/125*y))
        self.mouse.click(Button.left)
        self.mouse.position = prev_coords
        sleep(0.07)

# ==== MOVEMENT BY CLICK METHODS ==== #
    def move_right(self):
        self.x_pos += 1
        prev_window = find_window(GetWindowText(GetForegroundWindow()))
        to_top(self.window_id)
        self.click(1720, 560)
        to_top(prev_window[0])
        self.previous_map = 'r'

    def move_left(self):
        self.x_pos -= 1
        prev_window = find_window(GetWindowText(GetForegroundWindow()))
        to_top(self.window_id)
        self.click(200, 560)
        to_top(prev_window[0])
        self.previous_map = 'l'

    def move_up(self):
        self.y_pos -= 1
        prev_window = find_window(GetWindowText(GetForegroundWindow()))
        to_top(self.window_id)
        self.click(1050, 40)
        to_top(prev_window[0])
        self.previous_map = 'u'

    def move_down(self):
        self.y_pos += 1
        prev_window = find_window(GetWindowText(GetForegroundWindow()))
        to_top(self.window_id)
        self.click(950, 910)
        to_top(prev_window[0])
        self.previous_map = 'd'

    def reset(self):
        if self.cancel_flag:
            prev_window = find_window(GetWindowText(GetForegroundWindow()))
            to_top(self.window_id)
            self.click(960, 480)
            to_top(prev_window[0])
            if self.previous_map == 'u':
                self.y_pos += 1
            if self.previous_map == 'd':
                self.y_pos -= 1
            if self.previous_map == 'l':
                self.x_pos += 1
            if self.previous_map == 'r':
                self.x_pos -= 1
            self.previous_map = None
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
                sleep(8)
        else:
            for i in range(value):
                if not self.traveling:
                    return
                self.move_down()
                sleep(8)

    def travel_horizontal(self, value):
        if value == 0:
            return
        if value < 0:
            for i in range(abs(value)):
                if not self.traveling:
                    return
                self.move_left()
                sleep(8)
        else:
            for i in range(value):
                if not self.traveling:
                    return
                self.move_right()
                sleep(8)

    def travel_final(self):
        if self.traveling:
            self.travel_vertical(self.y_dest - self.y_pos)
            self.travel_horizontal(self.x_dest - self.x_pos)
            return

    def automate_travel(self):
        travel_thread = Thread(target=self.travel_final)
        travel_thread.start()
        travel_thread.join()

    def append_map_clicks(self):
        confirm_append = ConfirmBox()
        confirm_append.mainloop()
        if confirm_append.value:
            with open(self.maps_file, 'a') as f:
                to_append = str((self.x_pos, self.y_pos)) + " : " + str(self.click_coords) + "\n"
                f.write(to_append)
        self.click_coords = []
        return confirm_append.value
