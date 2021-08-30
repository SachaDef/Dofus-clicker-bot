from mttkinter.mtTkinter import *
from PIL import Image, ImageTk
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPDF, renderPM
from random import choice
import bot


# ===== Helper/secondary interface/tkinter classes ===== #

class AutoCloseMessageBox(Tk):

    def __init__(self, title, text, duration):
        super().__init__()
        self.window_title = title
        self.text = text
        self.duration = duration
        self.width = 400
        self.height = 200
        self.after(1, lambda: self.focus_force())
        self.title(self.window_title)
        self.geometry(f"{self.width}x{self.height}+{int(self.winfo_screenwidth()/2 - self.width/2)}+{int(self.winfo_screenheight()/2 - self.height/2)}")
        self.minsize(self.width, self.height)
        self.maxsize(self.width, self.height)
        self.iconbitmap(r'img\icon.ico')

        self.images = [(r'img\emeraude.gif', "#8ad31e", 'black'),
              (r'img\pourpre.gif', "#b83206", 'black'),
              (r'img\turquoise.gif', "#188089", 'black'),
              (r'img\ebene.gif', "#76694a", 'white'),
              (r'img\ivoire.gif', "#e2c18e", 'black'),
              (r'img\ocre.gif', "#f7c017", 'black')]
        
        self.activate()

    def activate(self):
        dofus = choice(self.images)
        self.bg_img = PhotoImage(file=dofus[0])
        self.bg_canvas = Canvas(self, width=self.width, height=self.height, bg=dofus[1])
        self.bg_canvas.create_image(int(self.width/2), int(self.height/2), image=self.bg_img)
        self.bg_canvas.create_text(int(self.width/2), int(self.height/2), text=self.text, font=("Calibri", int(self.width/15)), fill=dofus[2], width=int(self.width/1.3), justify="center")
        self.bg_canvas.pack()
        self.bg_canvas.focus_set()
        self.bind("<Escape>", lambda event: self.destroy())
        self.bind("<Return>", lambda event: self.destroy())
        self.after(int(self.duration*1000), lambda: self.destroy())
        self.mainloop()


class ConfirmBox(Tk):
    def __init__(self, title):
        super().__init__()
        self.width = 400
        self.height = 200
        self.window_title = title
        self.value = False
        self.after(1, lambda: self.focus_force())
        self.title(self.window_title)
        self.geometry(f"{self.width}x{self.height}+{int(self.winfo_screenwidth()/2 - self.width/2)}+{int(self.winfo_screenheight()/2 - self.height/2)}")
        self.minsize(self.width, self.height)
        self.maxsize(self.width, self.height)
        self.iconbitmap(r'img\icon.ico')

        self.bg_img = PhotoImage(file=r'img\6dofus.gif').subsample(4)
        self.bg_canvas = Canvas(self, width=self.width, height=self.height, bg="#ffffff")
        self.bg_canvas.create_image(self.width/2, self.height/2, image=self.bg_img)
        self.bg_canvas.create_text(self.width/2, self.height/2, text="Confirmer ?", font=("Calibri", int(self.width/15)), fill="black", width=int(self.width/1.3), justify="center")
        self.bg_canvas.pack()

        self.bind("<Return>", lambda event: self.confirm())
        self.bind("<Escape>", lambda event: self.infirm())

    def confirm(self):
        self.value = True
        self.destroy()

    def infirm(self):
        self.value = False
        self.destroy()


class ResizingCanvas(Canvas):   # Not used right now, but still useful code (https://stackoverflow.com/questions/22835289/how-to-get-tkinter-canvas-to-dynamically-resize-to-window-width/22835732)

    def __init__(self,parent, **kwargs):
        Canvas.__init__(self,parent, **kwargs)
        self.bind("<Configure>", self.on_resize)
        self.height = self.winfo_reqheight()
        self.width = self.winfo_reqwidth()

    def on_resize(self,event):
        # determine the ratio of old width/height to new width/height
        wscale = float(event.width)/self.width
        hscale = float(event.height)/self.height
        self.width = event.width
        self.height = event.height
        # resize the canvas 
        self.config(width=self.width, height=self.height)
        # rescale all the objects tagged with the "all" tag
        self.scale("all", 0, 0, wscale, hscale)



# ===== Main interface ===== #

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
        self.iconbitmap(r'img\icon.ico')

        # image = svg2rlg(r'img\bg_img.svg')                      => these 2 lines were used to create a clean resolution png from a svg
        # renderPM.drawToFile(image, r'img\temp.png', fmt="png")  => no longer needed since the png is now used
        self.bg_img = Image.open(r'img\bg_img.png')
        self.bg_img.thumbnail((self.width, self.height))
        self.bg_img = ImageTk.PhotoImage(self.bg_img)
        self.bg_canvas = Canvas(self, width=self.width, height=self.height)
        self.bg_canvas.create_image(int(self.width/2), int(self.height/2), image=self.bg_img)

        if self.mode == "init":
            self.bg_canvas.create_text(int(self.width/2), int(self.height/5), text="Character name", font=("Calibri", int(self.width/20)), fill="black")
            self.name_entry = Entry(self.bg_canvas, font=("Calibri", int(self.width/32)), bg="white", width=int(self.width/64), justify="center")
            self.bg_canvas.create_window(int(self.width/2), int(self.height/3), window=self.name_entry)
            self.bg_canvas.create_text(int(self.width/3.36), int(self.height/1.89), text="X position", font=("Calibri", int(self.width/20)), fill="black")
            self.bg_canvas.create_text(int(self.width/1.42), int(self.height/1.89), text="Y position", font=("Calibri", int(self.width/20)), fill="black")
            self.x_entry = Entry(self.bg_canvas, font=("Calibri", int(self.width/32)), bg="white", width=int(self.width/64), justify="center")
            self.y_entry = Entry(self.bg_canvas, font=("Calibri", int(self.width/32)), bg="white", width=int(self.width/64), justify="center")
            self.bg_canvas.create_window(int(self.width/3.36), int(self.height/1.44), window=self.x_entry)
            self.bg_canvas.create_window(int(self.width/1.42), int(self.height/1.44), window=self.y_entry)
            self.bg_canvas.pack()
            self.name_entry.focus_set()

        elif self.mode == "travel":
            self.bg_canvas.create_text(int(self.width/3.36), int(self.height/2.57), text="X destination", font=("Calibri", int(self.width/20)), fill="black")
            self.bg_canvas.create_text(int(self.width/1.42), int(self.height/2.57), text="Y destination", font=("Calibri", int(self.width/20)), fill="black")
            self.x_entry = Entry(self.bg_canvas, font=("Calibri", int(self.width/32)), bg="white", width=int(self.width/64), justify="center")
            self.y_entry = Entry(self.bg_canvas, font=("Calibri", int(self.width/32)), bg="white", width=int(self.width/64), justify="center")
            self.bg_canvas.create_window(int(self.width/3.36), int(self.height/1.63), window=self.x_entry)
            self.bg_canvas.create_window(int(self.width/1.42), int(self.height/1.63), window=self.y_entry)
            self.bg_canvas.pack()
            self.x_entry.focus_set()

        elif self.mode == "update":
            self.bg_canvas.create_text(int(self.width/3.36), int(self.height/2.57), text="X position", font=("Calibri", int(self.width/20)), fill="black")
            self.bg_canvas.create_text(int(self.width/1.42), int(self.height/2.57), text="Y position", font=("Calibri", int(self.width/20)), fill="black")
            self.x_entry = Entry(self.bg_canvas, font=("Calibri", int(self.width/32)), bg="white", width=int(self.width/64), justify="center")
            self.y_entry = Entry(self.bg_canvas, font=("Calibri", int(self.width/32)), bg="white", width=int(self.width/64), justify="center")
            self.bg_canvas.create_window(int(self.width/3.36), int(self.height/1.63), window=self.x_entry)
            self.bg_canvas.create_window(int(self.width/1.42), int(self.height/1.63), window=self.y_entry)
            self.bg_canvas.pack()
            self.x_entry.focus_set()


        self.bind("<Return>", lambda event: self.retrieve_data())
        self.bind("<Escape>", lambda event: self.destroy())

    def retrieve_data(self):
        if self.mode == "init":
            if len(self.name_entry.get()) >= 3 and bot.find_window(self.name_entry.get()) != False:
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
                    temp = self.bg_canvas.create_text(int(self.width/2), int(self.height/1.2), text="Coordonnées invalides", font=("Calibri", int(self.width/26.66)), fill="black")
                    self.after(2000, lambda: self.bg_canvas.delete(temp))
            else:
                del self.data[:]
                self.name_entry.delete(0, END)
                self.x_entry.delete(0, END)
                self.y_entry.delete(0, END)
                self.name_entry.focus_set()
                temp = self.bg_canvas.create_text(int(self.width/2), int(self.height/1.2), text="Nom de personnage invalide", font=("Calibri", int(self.width/26.66)), fill="black")
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
                temp = self.bg_canvas.create_text(int(self.width/2), int(self.height/1.2), text="Coordonnées invalides", font=("Calibri", int(self.width/26.66)), fill="black")
                self.after(2000, lambda: self.bg_canvas.delete(temp))

        if self.mode == "init" and len(self.data) == 3:
            return_value = (self.data[0], self.data[1], self.data[2])
            self.destroy()
            return return_value
        elif (self.mode == "travel" or self.mode == "update") and len(self.data) == 2:
            return_value = (self.data[0], self.data[1])
            self.destroy()
            return return_value
