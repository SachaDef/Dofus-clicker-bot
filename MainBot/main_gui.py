from tkinter import *


class DofusBotInterface(Tk):
    def __init__(self, init=True):
        super().__init__()
        self.after(1, lambda: self.focus_force())
        self.init = init
        self.title("Dofus TravelBot")
        self.geometry("600x430+480+175")
        self.minsize(600, 430)
        self.maxsize(600, 430)
        self['bg'] = 'white'
        self.entries = []
        self.data = []
        self.window = Frame(self, bg="white", highlightbackground="black", highlightthickness=2)
        self.containers = [Frame(self.window, bg="white") for i in range(2)]
        self.useless = {
            0: "X",
            1: "Y"
        }
        for i in range(2):
            if self.init:
                label = Label(self.containers[i], text=self.useless[i] + " pos :", font=("Calibri", 24), bg="white",
                              fg="black")
                entry = Entry(self.containers[i], bg="black", fg="white", font=("Calibri", 24), width=10)
                self.entries.append(entry)
                label.pack(expand=YES)
                entry.pack(expand=YES)
            else:
                label = Label(self.containers[i], text=self.useless[i] + " destination :", font=("Calibri", 24), bg="white",
                              fg="black")
                entry = Entry(self.containers[i], bg="black", fg="white", font=("Calibri", 24), width=10)
                self.entries.append(entry)
                label.pack(expand=YES)
                entry.pack(expand=YES)
        self.entries[0].focus_set()
        for container in self.containers:
            container.pack(expand=YES, padx=50, pady=50)
        self.window.pack(expand=YES)
        self.bind("<Return>", lambda event: self.retrieve_data())
        self.bind("<Escape>", lambda event: self.destroy())

    def retrieve_data(self):
        for entry in self.entries:
            if 1 <= len(entry.get()) <= 4:
                self.data.append(entry.get())
            else:
                self.data = []
                for new_entry in self.entries:
                    new_entry.delete(0)
                break
        if len(self.data) == 2:
            self.data = (self.data[0], self.data[1])
            self.destroy()
            return self.data