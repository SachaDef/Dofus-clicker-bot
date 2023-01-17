import win32gui

from ctypes import c_int, WinDLL, byref, sizeof
from ctypes.wintypes import HWND, DWORD
dwmapi = WinDLL("dwmapi")
DWMWA_CLOAKED = 14 
isCloacked = c_int(0)


# Get active windows
def winEnumHandler(window_handle, _):      # Copied from https://stackoverflow.com/questions/61865399/win32gui-shows-some-windows-that-are-not-open
    if win32gui.IsWindowVisible(window_handle) and win32gui.GetWindowText(window_handle) != '':
        dwmapi.DwmGetWindowAttribute(HWND(window_handle),
                                        DWORD(DWMWA_CLOAKED),
                                        byref(isCloacked),
                                        sizeof(isCloacked))
        title = win32gui.GetWindowText(window_handle)
        if (isCloacked.value == 0):
            windows.append((window_handle, title))

# Filter active windows
def window_filtering(string_filter):
    global windows
    windows = []
    win32gui.EnumWindows(winEnumHandler, None)
    dofus_windows = [window for window in windows if "Dofus 2" in window[1]]
    if "Character name".startswith(string_filter) or string_filter == "":
        return dofus_windows
    else:
        for dofus_window in dofus_windows:
            if not dofus_window[1].lower().startswith(string_filter.lower()):
                dofus_windows.remove(dofus_window)
        return dofus_windows

# Automatisation bot
class CharacterBot():

    def __init__(self):
        pass
