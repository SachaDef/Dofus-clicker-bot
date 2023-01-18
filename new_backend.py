import win32gui
import os

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
def window_filtering():
    global windows
    windows = []
    win32gui.EnumWindows(winEnumHandler, None)
    return [window for window in windows if "Dofus 2" in window[1]]

# Get all path files
def get_all_paths(string_filter):
    orig_dir = os.getcwd()
    os.chdir("data/paths")
    root_dir = os.getcwd()
    path_files = os.listdir()
    os.chdir(orig_dir)
    return [root_dir+"\\"+path_file.replace(".txt", "") for path_file in path_files if (".txt" in path_file and
                                                                    (path_file.startswith(string_filter) or string_filter == "Farming path"))]
    



# Automatisation bot
class CharacterBot():

    def __init__(self):
        pass
