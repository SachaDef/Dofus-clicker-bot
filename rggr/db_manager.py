import sqlite3 as sql
from tkinter import *
from pynput.keyboard import Listener, Key


class MapManager:
    print("test")
    def __init__(self, db_file="maps.db"):
        self.db = db_file
        self.connection = sql.connect(self.db)
        self.cursor = self.connection.cursor()

    def interface(self):
        root = Tk()
        root.after(1, lambda: root.focus_force())
        root.title("MapDatabase Manager")
        root.geometry("900x600+330+100")
        root.minsize(900, 600)
        root.maxsize(900, 600)
        root['bg'] = 'white'
        root.bind("<Escape>", lambda event: root.destroy())
        entries_frame = Frame(root)
        label = Label(entries_frame)
        label.pack()
        entries_frame.pack(side=LEFT)
        root.mainloop()

    def add_map(self, x_pos, y_pos, sleep_time, click_coords):
        with self.connection:
            self.cursor.execute(
                """insert into maps values (NULL, ?, ?, ?, ?)""", (x_pos, y_pos, click_coords, sleep_time)
            )

manager = MapManager()
manager.interface()