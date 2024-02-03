from time import sleep
import ctypes, ctypes.wintypes
import win32gui, win32con, win32api
import sys
import new_globals as globals
import customtkinter as ctk
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("dark-blue")


# ==== GUI ==== #
class PopUp(ctk.CTk):
    
    def __init__(self, title, width=300, height=200, duration=0, text="Label"):
        super().__init__()
        screenw = self.winfo_screenwidth()
        screenh = self.winfo_screenheight()
        self.title(title)
        self.geometry(f"{width}x{height}+{int(screenw/2-width/2)-40}+{int(screenh/2-height/2)-80}")
        self.configure(bg_color=globals.MAIN_BACKGROUND_GRAY, fg_color=globals.MAIN_BACKGROUND_GRAY)
        self.attributes("-topmost", True)
        ctk.CTkLabel(self, text=text).pack(expand=True)
        if duration:
            self.after(duration, self.destroy)
        self.bind("<Return>", lambda _: self.confirm())
        self.bind("<Escape>", lambda _: self.infirm())
        self.mainloop()
    
    def confirm(self):
        self.destroy()

    def infirm(self):
        self.destroy()


# ==== WINDOW HANDLING ==== #
# Variables
active_windows = []

# ctypes clarity
DwmGetWindowAttribute = ctypes.WinDLL("dwmapi").DwmGetWindowAttribute
HWND = ctypes.wintypes.HWND
DWORD = ctypes.wintypes.DWORD
byref = ctypes.byref
sizeof = ctypes.sizeof
DWMWA_CLOAKED = 14 
isCloacked = ctypes.c_int(0)

# Get active windows
def winEnumHandler(window_handle: int, _) -> None:      # Copied from https://stackoverflow.com/questions/61865399/win32gui-shows-some-windows-that-are-not-open
    global active_windows
    if win32gui.IsWindowVisible(window_handle) and win32gui.GetWindowText(window_handle) != '':
        DwmGetWindowAttribute(HWND(window_handle),
                              DWORD(DWMWA_CLOAKED),
                              byref(isCloacked),
                              sizeof(isCloacked))
        title: str = win32gui.GetWindowText(window_handle)
        if (isCloacked.value == 0):
            active_windows.append((window_handle, title))

# Filter out non-dofus windows
def window_filtering() -> None:
    global active_windows
    active_windows = []
    win32gui.EnumWindows(winEnumHandler, None)

# Get window handle from given character name
Window = tuple[()] | tuple[int, str]
def get_named_window(filter: str) -> Window:
    global active_windows
    for window in active_windows:
        if window[1].lower().startswith(filter):
            return window
    return ()


# ==== MAIN ==== #
def key_stroke(hwnd, hex_val):
    win32api.SendMessage(hwnd, win32con.WM_KEYDOWN, hex_val, 0)
    sleep(0.05)
    win32api.SendMessage(hwnd, win32con.WM_KEYUP, hex_val, 0)


if __name__ == "__main__":
    character = sys.argv[1]
    n_iter = int(sys.argv[2])
    n_iter = 10_000 if n_iter == -1 else n_iter

    window_filtering()
    hwnd = get_named_window(character)
    if not hwnd:
        print("No window found")
        exit(0)
    hwnd = hwnd[0]

    print("\nLoop 1")
    key_stroke(hwnd, 0x31)
    sleep(5)
    key_stroke(hwnd, 0x32)
    for i in range(n_iter-1):
        print(f"Loop {i+2}")
        sleep(5)
        key_stroke(hwnd, 0x31)
        sleep(5)
        key_stroke(hwnd, 0x32)
    popup = PopUp(title="DDLoop", text="Loop done !", duration=1000)
    