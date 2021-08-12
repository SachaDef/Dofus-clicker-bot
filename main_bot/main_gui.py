from mttkinter.mtTkinter import *
from main_bot.main_bot import find_window

class DofusBotInterface(Tk):
    def __init__(self, mode="travel"):
        super().__init__()
        self.width = 800
        self.height = 450
        self.data = []
        self.mode = mode
        self.after(1, lambda: self.focus_force())
        self.title("DofusBot")
        self.geometry(f"{self.width}x{self.height}+{int(self.winfo_screenwidth()/2 - self.width/2)}+{int(self.winfo_screenheight()/2 - self.height/2)}")
        self.minsize(self.width, self.height)
        self.maxsize(self.width, self.height)
        self.iconbitmap(r'img\icon.ico')

        self.bg_img = PhotoImage(file=r"img\bg_img.gif").subsample(3)
        self.bg_canvas = Canvas(self, width=self.width, height=self.height)
        self.bg_canvas.create_image(self.width/2, self.height/2, image=self.bg_img)

        if self.mode == "init":
            self.bg_canvas.create_text(400, 87, text="Character name", font=("Calibri", 36), fill="black")
            self.name_entry = Entry(self.bg_canvas, font=("Calibri", 20), bg="white", width=10, justify="center")
            self.bg_canvas.create_window(400, 162, window=self.name_entry)
            self.bg_canvas.create_text(237, 237, text="X position", font=("Calibri", 36), fill="black")
            self.bg_canvas.create_text(562, 237, text="Y position", font=("Calibri", 36), fill="black")
            self.x_entry = Entry(self.bg_canvas, font=("Calibri", 20), bg="white", width=10, justify="center")
            self.y_entry = Entry(self.bg_canvas, font=("Calibri", 20), bg="white", width=10, justify="center")
            self.bg_canvas.create_window(237, 312, window=self.x_entry)
            self.bg_canvas.create_window(562, 312, window=self.y_entry)
            self.bg_canvas.pack()
            self.name_entry.focus_set()

        elif self.mode == "travel":
            self.bg_canvas.create_text(237, 175, text="X destination", font=("Calibri", 32), fill="black")
            self.bg_canvas.create_text(562, 175, text="Y destination", font=("Calibri", 32), fill="black")
            self.x_entry = Entry(self.bg_canvas, font=("Calibri", 20), bg="white", width=10, justify="center")
            self.y_entry = Entry(self.bg_canvas, font=("Calibri", 20), bg="white", width=10, justify="center")
            self.bg_canvas.create_window(237, 275, window=self.x_entry)
            self.bg_canvas.create_window(562, 275, window=self.y_entry)
            self.bg_canvas.pack()
            self.x_entry.focus_set()

        elif self.mode == "update":
            self.bg_canvas.create_text(237, 175, text="X position", font=("Calibri", 32), fill="black")
            self.bg_canvas.create_text(562, 175, text="Y position", font=("Calibri", 32), fill="black")
            self.x_entry = Entry(self.bg_canvas, font=("Calibri", 20), bg="white", width=10, justify="center")
            self.y_entry = Entry(self.bg_canvas, font=("Calibri", 20), bg="white", width=10, justify="center")
            self.bg_canvas.create_window(237, 275, window=self.x_entry)
            self.bg_canvas.create_window(562, 275, window=self.y_entry)
            self.bg_canvas.pack()
            self.x_entry.focus_set()


        self.bind("<Return>", lambda event: self.retrieve_data())
        self.bind("<Escape>", lambda event: self.destroy())

    def retrieve_data(self):
        if self.mode == "init":
            if len(self.name_entry.get()) >= 3 and find_window(self.name_entry.get()) != False:
                if 1 <= len(self.x_entry.get()) <= 4 and 1 <= len(self.y_entry.get()) <= 4\
                and self.x_entry.get().replace("-", "").isdigit() and self.y_entry.get().replace("-", "").isdigit():
                    self.data.append(self.name_entry.get())
                    self.data.append(self.x_entry.get())
                    self.data.append(self.y_entry.get())
                else:
                    del self.data[:]
                    self.x_entry.delete(0, END)
                    self.y_entry.delete(0, END)
                    self.x_entry.focus_set()
                    temp = self.bg_canvas.create_text(400, 375, text="Coordonnées invalides", font=("Calibri", 24), fill="black")
                    self.after(2000, lambda: self.bg_canvas.delete(temp))
            else:
                del self.data[:]
                self.name_entry.delete(0, END)
                self.x_entry.delete(0, END)
                self.y_entry.delete(0, END)
                self.name_entry.focus_set()
                temp = self.bg_canvas.create_text(400, 375, text="Nom de personnage invalide", font=("Calibri", 24), fill="black")
                self.after(2000, lambda: self.bg_canvas.delete(temp))

        elif self.mode == "update" or self.mode == "travel":
            if 1 <= len(self.x_entry.get()) <= 4 and 1 <= len(self.y_entry.get()) <= 4\
            and self.x_entry.get().replace("-", "").isdigit() and self.y_entry.get().replace("-", "").isdigit():
                self.data.append(self.x_entry.get())
                self.data.append(self.y_entry.get())
            else:
                del self.data[:]
                self.x_entry.delete(0, END)
                self.y_entry.delete(0, END)
                self.x_entry.focus_set()
                temp = self.bg_canvas.create_text(400, 350, text="Coordonnées invalides", font=("Calibri", 24), fill="black")
                self.after(2000, lambda: self.bg_canvas.delete(temp))

        if self.mode == "init" and len(self.data) == 3:
            return_value = (self.data[0], self.data[1], self.data[2])
            self.destroy()
            return return_value
        elif (self.mode == "travel" or self.mode == "update") and len(self.data) == 2:
            return_value = (self.data[0], self.data[1])
            self.destroy()
            return return_value
