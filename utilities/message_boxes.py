from mttkinter.mtTkinter import *
from random import choice


class AutoCloseMessageBox(Tk):

    def __init__(self, title, text, duration):
        super().__init__()
        self.window_title = title
        self.text = text
        self.duration = duration
        self.width = 500
        self.height = 250
        self.after(1, lambda: self.focus_force())
        self.title(self.window_title)
        self.geometry(f"{self.width}x{self.height}+{int(self.winfo_screenwidth() / 2 - self.width / 2)}+{int(self.winfo_screenheight() / 2 - self.height / 2)}")
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
        self.bg_canvas.create_image(self.width / 2, self.height / 2, image=self.bg_img)
        self.bg_canvas.create_text(self.width/2, self.height/2, text=self.text, font=("Calibri", 26), fill=dofus[2], width=300, justify="center")
        self.bg_canvas.pack()
        self.bg_canvas.focus_set()
        self.bind("<Escape>", lambda event: self.destroy())
        self.bind("<Return>", lambda event: self.destroy())
        self.after(int(self.duration*1000), lambda: self.destroy())
        self.mainloop()


class ConfirmBox(Tk):
    def __init__(self, title):
        super().__init__()
        self.width = 500
        self.height = 250
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
        self.bg_canvas.create_image(self.width / 2, self.height / 2, image=self.bg_img)
        self.bg_canvas.create_text(self.width/2, self.height/2, text="Confirmer ?", font=("Calibri", 26), fill="black", width=300, justify="center")
        self.bg_canvas.pack()

        self.bind("<Return>", lambda event: self.confirm())
        self.bind("<Escape>", lambda event: self.infirm())

    def confirm(self):
        self.value = True
        self.destroy()

    def infirm(self):
        self.value = False
        self.destroy()