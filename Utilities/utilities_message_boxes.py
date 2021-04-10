from tkinter import *
from random import choice


def AutoCloseMessageBox(text, duration):
    root = Tk()
    width = 400
    height = 200
    root.after(1, lambda: root.focus_force())
    root.title("DofusBot")
    root.geometry(f"{width}x{height}+{int(root.winfo_screenwidth() / 2 - width / 2)}+{int(root.winfo_screenheight() / 2 - height / 2)}")
    root.minsize(width, height)
    root.maxsize(width, height)
    root.iconbitmap(r'C:\Users\sacha\Desktop\Dofus Bot\img\icon.ico')

    images = [(r'C:\Users\sacha\Desktop\Dofus Bot\img\emeraude.gif', "#8ad31e", 'black'),
              (r'C:\Users\sacha\Desktop\Dofus Bot\img\pourpre.gif', "#b83206", 'black'),
              (r'C:\Users\sacha\Desktop\Dofus Bot\img\turquoise.gif', "#188089", 'black'),
              (r'C:\Users\sacha\Desktop\Dofus Bot\img\ebene.gif', "#76694a", 'white'),
              (r'C:\Users\sacha\Desktop\Dofus Bot\img\ivoire.gif', "#e2c18e", 'black'),
              (r'C:\Users\sacha\Desktop\Dofus Bot\img\ocre.gif', "#f7c017", 'black')]
    dofus = choice(images)
    bg_img = PhotoImage(file=dofus[0])
    bg_canvas = Canvas(root, width=width, height=height, bg=dofus[1])
    bg_canvas.create_image(width / 2, height / 2, image=bg_img)
    bg_canvas.create_text(width/2, height/2, text=text, font=("Calibri", 26), fill=dofus[2], width=300, justify="center")
    bg_canvas.pack()
    bg_canvas.focus_set()

    root.bind("<Escape>", lambda event: root.destroy())
    root.bind("<Return>", lambda event: root.destroy())
    root.after(int(duration*1000), lambda: root.destroy())
    root.mainloop()


class ConfirmBox(Tk):
    def __init__(self):
        super().__init__()
        self.width = 400
        self.height = 200
        self.value = False
        self.after(1, lambda: self.focus_force())
        self.title("DofusBot")
        self.geometry(f"{self.width}x{self.height}+{int(self.winfo_screenwidth()/2 - self.width/2)}+{int(self.winfo_screenheight()/2 - self.height/2)}")
        self.minsize(self.width, self.height)
        self.maxsize(self.width, self.height)
        self.iconbitmap(r'C:\Users\sacha\Desktop\Dofus Bot\img\icon.ico')

        self.bg_img = PhotoImage(file=r'C:\Users\sacha\Desktop\Dofus Bot\img\6dofus.gif').subsample(4)
        self.bg_canvas = Canvas(self, width=self.width, height=self.height, bg="#ffffff")
        self.bg_canvas.create_image(self.width / 2, self.height / 2, image=self.bg_img)
        self.bg_canvas.create_text(self.width/2, self.height/2, text="Confirmer ? [Return/Esc]", font=("Calibri", 26), fill="black", width=300, justify="center")
        self.bg_canvas.pack()

        self.bind("<Return>", lambda event: self.confirm())
        self.bind("<Escape>", lambda event: self.infirm())

    def confirm(self):
        self.value = True
        self.destroy()

    def infirm(self):
        self.value = False
        self.destroy()