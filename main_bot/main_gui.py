from tkinter import *


class DofusBotInterface(Tk):
    def __init__(self, mode="travel"):
        super().__init__()
        self.width = 640
        self.height = 360
        self.data = []
        self.mode = mode
        self.after(1, lambda: self.focus_force())
        self.title("DofusBot")
        self.geometry(f"{self.width}x{self.height}+{int(self.winfo_screenwidth()/2 - self.width/2)}+{int(self.winfo_screenheight()/2 - self.height/2)}")
        self.minsize(self.width, self.height)
        self.maxsize(self.width, self.height)
        self.iconbitmap(r'C:\Users\sacha\Desktop\Dofus Bot\img\icon.ico')

        self.bg_img = PhotoImage(file=r"C:\Users\sacha\Desktop\Dofus Bot\img\bg_img.gif").subsample(4)
        self.bg_canvas = Canvas(self, width=self.width, height=self.height)
        self.bg_canvas.create_image(self.width/2, self.height/2, image=self.bg_img)

        if self.mode == "init":
            self.bg_canvas.create_text(320, 100, text="Character name", font=("Calibri", 36), fill="black")
            self.name_entry = Entry(self.bg_canvas, font=("Calibri", 20), bg="white", width=10, justify="center")
            self.bg_canvas.create_window(320, 160, window=self.name_entry)
            self.bg_canvas.create_text(190, 220, text="X position", font=("Calibri", 36), fill="black")
            self.bg_canvas.create_text(450, 220, text="Y position", font=("Calibri", 36), fill="black")
            self.x_entry = Entry(self.bg_canvas, font=("Calibri", 20), bg="white", width=10, justify="center")
            self.y_entry = Entry(self.bg_canvas, font=("Calibri", 20), bg="white", width=10, justify="center")
            self.bg_canvas.create_window(190, 280, window=self.x_entry)
            self.bg_canvas.create_window(450, 280, window=self.y_entry)
            self.bg_canvas.pack()
            self.name_entry.focus_set()

        elif self.mode == "travel":
            self.bg_canvas.create_text(190, 140, text="X destination", font=("Calibri", 32), fill="black")
            self.bg_canvas.create_text(450, 140, text="Y destination", font=("Calibri", 32), fill="black")
            self.x_entry = Entry(self.bg_canvas, font=("Calibri", 20), bg="white", width=10, justify="center")
            self.y_entry = Entry(self.bg_canvas, font=("Calibri", 20), bg="white", width=10, justify="center")
            self.bg_canvas.create_window(190, 220, window=self.x_entry)
            self.bg_canvas.create_window(450, 220, window=self.y_entry)
            self.bg_canvas.pack()
            self.x_entry.focus_set()

        elif self.mode == "update":
            self.bg_canvas.create_text(190, 140, text="X position", font=("Calibri", 32), fill="black")
            self.bg_canvas.create_text(450, 140, text="Y position", font=("Calibri", 32), fill="black")
            self.x_entry = Entry(self.bg_canvas, font=("Calibri", 20), bg="white", width=10, justify="center")
            self.y_entry = Entry(self.bg_canvas, font=("Calibri", 20), bg="white", width=10, justify="center")
            self.bg_canvas.create_window(190, 220, window=self.x_entry)
            self.bg_canvas.create_window(450, 220, window=self.y_entry)
            self.bg_canvas.pack()
            self.x_entry.focus_set()


        self.bind("<Return>", lambda event: self.retrieve_data())
        self.bind("<Escape>", lambda event: self.destroy())

    def retrieve_data(self):
        if 1 <= len(self.x_entry.get()) <= 4 and 1 <= len(self.y_entry.get()) <= 4\
        and self.x_entry.get().replace("-", "").isdigit() and self.y_entry.get().replace("-", "").isdigit():
            if self.mode == "init":
                self.data.append(self.name_entry.get())
                self.data.append(self.x_entry.get())
                self.data.append(self.y_entry.get())
            else:
                self.data.append(self.x_entry.get())
                self.data.append(self.y_entry.get())
        
        else:
            del self.data[:]
            self.x_entry.delete(0, END)
            self.y_entry.delete(0, END)
            self.x_entry.focus_set()
            self.bg_canvas.create_text(320, 300, text="Coordonnées invalides", font=("Calibri", 24), fill="black")

        if self.mode == "init" and len(self.data) == 3:
            return_value = (self.data[0], self.data[1], self.data[2])
            self.destroy()
            return return_value
        elif (self.mode == "travel" or self.mode == "update") and len(self.data) == 2:
            return_value = (self.data[0], self.data[1])
            self.destroy()
            return return_value
