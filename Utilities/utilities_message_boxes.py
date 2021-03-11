from tkinter import *


def AutoCloseMessageBox(title, text, duration):
    root = Tk()
    root.after(1, lambda: root.focus_force())
    root['bg'] = 'white'
    root.title(title)
    root.geometry("400x150+650+300")
    label = Label(root, text=text, font=("Calibri", 20), bg="white", fg="black")
    label.pack(expand=YES)
    label.focus_set()
    root.after(int(duration*1000), lambda: root.destroy())
    root.mainloop()


class ConfirmBox(Tk):
    def __init__(self):
        super().__init__()
        self.after(1, lambda: self.focus_force())
        self.value = False
        self.title("MapMakingBot")
        self.geometry("400x150+420+180")
        self['bg'] = 'white'
        self.label = Label(self, text="Confirmer ?", font=("Calibri", 24), bg="white", fg="black")
        self.label.pack(expand=YES)
        self.label.focus_set()
        self.bind("<Return>", lambda event: self.confirm())
        self.bind("<Escape>", lambda event: self.infirm())

    def confirm(self):
        self.value = True
        self.destroy()

    def infirm(self):
        self.value = False
        self.destroy()