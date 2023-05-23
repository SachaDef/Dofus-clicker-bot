import ctypes

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
tracked_characters = []   # List of (character_name, character_tab, character_bot)
click_listening_flag = False
active_windows = []
active_character_names = []
path_files = []
path_names = []
map_textbox_changed = False
path_textbox_changed = False

# ctypes clarity
DwmGetWindowAttribute = ctypes.WinDLL("dwmapi").DwmGetWindowAttribute
HWND = ctypes.wintypes.HWND
DWORD = ctypes.wintypes.DWORD
byref = ctypes.byref
sizeof = ctypes.sizeof
DWMWA_CLOAKED = 14 
isCloacked = ctypes.c_int(0)