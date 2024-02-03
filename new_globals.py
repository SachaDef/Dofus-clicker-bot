import ctypes, ctypes.wintypes
import pickle

# Constants
CLEAR_RED = '#e60000'
DARK_RED = '#800000'
CLEAR_GREEN = '#009900'
DARK_GREEN = '#004d00'
BORDER_GRAY = '#565B5E'
SECONDARY_BACKGROUND_GRAY = "#292929"
MAIN_BACKGROUND_GRAY = "#212121"
ENTRY_GRAY = '#343638'

# Shared variables
tracked_characters: list = []   # List of (character_name, character_tab, character_bot)
click_listening_flag: bool = False
active_windows: list = []
active_character_names: list = []
path_files: list = []
path_names: list = []
user_changing: bool = True
map_textbox_changed: bool = False
path_textbox_changed: bool = False
displayed_map: tuple = ()

# buttons freezes
refresh_freeze: bool = False

# ctypes clarity
DwmGetWindowAttribute = ctypes.WinDLL("dwmapi").DwmGetWindowAttribute
HWND = ctypes.wintypes.HWND
DWORD = ctypes.wintypes.DWORD
byref = ctypes.byref
sizeof = ctypes.sizeof
DWMWA_CLOAKED = 14 
isCloacked = ctypes.c_int(0)

# Pickle file read&print (helper)
MapCoords = tuple[int, int]
ScreenCoords = tuple[int, int]
Clicks = list[ScreenCoords]
def read_print(filename: str) -> dict[MapCoords : Clicks]:
    try:
        with open(filename, "rb") as file:
            try:
                data = pickle.load(file)
                return data
            except EOFError:
                return {}
    except FileNotFoundError:
        return {}