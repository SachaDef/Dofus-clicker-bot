from time import sleep
from ahk import AHK
from Utilities.utilities_message_boxes import ConfirmBox


# ==== BOT INITIALIZATION ==== #
class DofusBot:
    def __init__(self, x_pos, y_pos):
        self.travel_running = False
        self.map_creation_running = False
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.x_dest = 0
        self.y_dest = 0
        self.previous = None
        self.clicker = AHK()
        self.window = self.clicker.find_window(title=b'Dofus')
        self.mouse_coords = []
        self.maps_file = "..\\Maps_Paths\\farming_maps.txt"

# ==== START/STOP METHODS ==== #
    def travel_start(self):
        self.travel_running = True

    def travel_stop(self):
        self.travel_running = False

    def map_creation_start(self):
        self.map_creation_running = True

    def map_creation_stop(self):
        self.map_creation_running = False

    def exit(self):
        self.travel_stop()
        self.map_creation_stop()

# ==== POSITION/DESTINATION MODIFICATION METHODS ==== #
    def xp(self):
        self.x_pos += 1

    def xm(self):
        self.x_pos -= 1

    def yp(self):
        self.y_pos += 1

    def ym(self):
        self.y_pos -= 1

    def set_pos(self, coords):
        self.x_pos = coords[0]
        self.y_pos = coords[1]

    def set_dest(self, coords):
        self.x_dest = coords[0]
        self.y_dest = coords[1]

# ==== MOVEMENT BY CLICK METHODS ==== #
    def move_right(self):
        self.xp()
        current_window = self.clicker.active_window
        current_pos = self.clicker.mouse_position
        self.window.activate()
        self.clicker.mouse_position = (1720, 560)
        self.clicker.click()
        current_window.activate()
        self.clicker.mouse_position = current_pos
        self.previous = 'r'

    def move_left(self):
        self.xm()
        current_window = self.clicker.active_window
        current_pos = self.clicker.mouse_position
        self.window.activate()
        self.clicker.mouse_position = (200, 560)
        self.clicker.click()
        current_window.activate()
        self.clicker.mouse_position = current_pos
        self.previous = 'l'

    def move_up(self):
        self.ym()
        current_window = self.clicker.active_window
        current_pos = self.clicker.mouse_position
        self.window.activate()
        if self.previous == 'd':
            self.clicker.mouse_position = (1120, 40)
            self.clicker.click()
        else:
            self.clicker.mouse_position = (960, 40)
            self.clicker.click()
        current_window.activate()
        self.clicker.mouse_position = current_pos
        self.previous = 'u'

    def move_down(self):
        self.yp()
        current_window = self.clicker.active_window
        current_pos = self.clicker.mouse_position
        self.window.activate()
        if self.previous == 'u':
            self.clicker.mouse_position = (1040, 910)
            self.clicker.click()
        else:
            self.clicker.mouse_position = (960, 910)
            self.clicker.click()
        current_window.activate()
        self.clicker.mouse_position = current_pos
        self.previous = 'd'

    def reset(self):
        current_window = self.clicker.active_window
        current_pos = self.clicker.mouse_position
        self.window.activate()
        self.clicker.mouse_position = (960, 540)
        self.clicker.click()
        current_window.activate()
        self.clicker.mouse_position = current_pos
        if self.previous == 'u':
            self.yp()
        if self.previous == 'd':
            self.ym()
        if self.previous == 'l':
            self.xp()
        if self.previous == 'r':
            self.xm()
        self.previous = None
        self.travel_stop()

# ==== MOVEMENT AUTOMATION METHODS ==== #
    def travel_vertical(self, value):
        if value == 0:
            return
        if value < 0:
            for i in range(abs(value)):
                if not self.travel_running:
                    return
                self.move_up()
                sleep(8)
        else:
            for i in range(value):
                if not self.travel_running:
                    return
                self.move_down()
                sleep(8)

    def travel_horizontal(self, value):
        if value == 0:
            return
        if value < 0:
            for i in range(abs(value)):
                if not self.travel_running:
                    return
                self.move_left()
                sleep(8)
        else:
            for i in range(value):
                if not self.travel_running:
                    return
                self.move_right()
                sleep(8)

    def automate_travel(self):
        if self.travel_running:
            self.travel_vertical(self.y_dest - self.y_pos)
            self.travel_horizontal(self.x_dest - self.x_pos)
            return

    def append_map_clicks(self):
        confirm_append = ConfirmBox()
        confirm_append.mainloop()
        if confirm_append.value:
            with open(self.maps_file, 'a') as f:
                to_append = str((self.x_pos, self.y_pos)) + " : " + str(self.mouse_coords) + "\n"
                f.write(to_append)
        self.mouse_coords = []
        return confirm_append.value
