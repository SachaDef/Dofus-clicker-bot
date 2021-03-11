from time import sleep
from ahk import AHK
from Utilities.utilities_message_boxes import AutoCloseMessageBox, ConfirmBox


##### BOT INITIALIZATION #####
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

##### START/STOP METHODS #####
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

#### POSITION/DESTINATION MODIFICATION METHODS #####
    def xP(self):
        self.x_pos += 1
    def xM(self):
        self.x_pos -= 1
    def yP(self):
        self.y_pos += 1
    def yM(self):
        self.y_pos -= 1

    def set_pos(self, coords):
        self.x_pos = coords[0]
        self.y_pos = coords[1]
    def set_dest(self, coords):
        self.x_dest = coords[0]
        self.y_dest = coords[1]

##### MOVEMENT BY CLICK METHODS #####
    def move_right(self):
        self.xP()
        current_window = self.clicker.active_window
        self.window.click(x=1720, y=560)
        current_window.activate()
        current_window.to_top()
        current_window.maximize()
        current_window.show()
        self.previous = 'r'
    def move_left(self):
        self.xM()
        current_window = self.clicker.active_window
        self.window.click(x=200, y=560)
        current_window.activate()
        current_window.to_top()
        current_window.maximize()
        current_window.show()
        self.previous = 'l'
    def move_up(self):
        self.yM()
        current_window = self.clicker.active_window
        if self.previous == 'd':
            self.window.click(x=1120, y=40)
        else:
            self.window.click(x=960, y=40)
        current_window.activate()
        current_window.to_top()
        current_window.maximize()
        current_window.show()
        self.previous = 'u'
    def move_down(self):
        self.yP()
        current_window = self.clicker.active_window
        if self.previous == 'u':
            self.window.click(x=1040, y=910)
        else:
            self.window.click(x=960, y=910)
        current_window.activate()
        current_window.to_top()
        current_window.maximize()
        current_window.show()
        self.previous = 'd'
    def reset(self):
        current_window = self.clicker.active_window
        self.window.click(x=960, y=540)
        current_window.activate()
        current_window.to_top()
        current_window.maximize()
        current_window.show()
        if self.previous == 'u':
            self.yP()
        if self.previous == 'd':
            self.yM()
        if self.previous == 'l':
            self.xP()
        if self.previous == 'r':
            self.xM()
        self.previous = None
        self.travel_stop()

##### MOVEMENT AUTOMATION METHODS #####
    def travel_vertical(self, value):
        if value == 0:
            return
        if value < 0:
            for i in range(abs(value)):
                if not self.travel_running:
                    break
                self.move_up()
                sleep(8)
        else:
            for i in range(value):
                if not self.travel_running:
                    break
                self.move_down()
                sleep(8)
    def travel_horizontal(self, value):
        if value == 0:
            return
        if value < 0:
            for i in range(abs(value)):
                if not self.travel_running:
                    break
                self.move_left()
                sleep(8)
        else:
            for i in range(value):
                if not self.travel_running:
                    break
                self.move_right()
                sleep(8)

    def automate_travel(self):
        if self.travel_running:
            self.travel_vertical(self.y_dest - self.y_pos)
            self.travel_horizontal(self.x_dest - self.x_pos)

    def append_map_clicks(self):
        confirm_append = ConfirmBox()
        confirm_append.mainloop()
        if confirm_append.value:
            with open(self.maps_file, 'a') as f:
                to_append = str((self.x_pos, self.y_pos)) + " : " + str(self.mouse_coords) + "\n"
                f.write(to_append)
        self.mouse_coords = []
        return confirm_append.value