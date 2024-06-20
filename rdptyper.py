import time
import os
import platform
import pygetwindow as gw
from pynput.keyboard import Controller
import argparse
import base64

def get_rdp_window(title):
    windows = gw.getWindowsWithTitle(title)  # Find RDP window by title
    if not windows:
        print("Window not found")
        return None
    return windows[0]

def activate_window(window):
    current_os = platform.system()
    if current_os == 'Windows':
        import win32gui
        import win32con
        hwnd = window._hWnd
        win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)  # Restore if minimized
        win32gui.SetForegroundWindow(hwnd)
    elif current_os == 'Linux':
        os.system(f"wmctrl -ia {window._hWnd}")
    else:
        print("Unsupported OS")

def type_text_in_rdp(file_path, delay, title, base):
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return

    if base:
        with open(file_path, 'rb') as file:
            file_bytes = file.read()
            file_text = base64.b64encode(file_bytes).decode('utf-8')
    else:
        with open(file_path, 'r', encoding='utf-8') as file:
            file_text = file.read()

    if not file_text:
        print("File is empty")
        return

    rdp_window = get_rdp_window(title)
    if not rdp_window:
        return

    activate_window(rdp_window)
    time.sleep(1)

    keyboard = Controller()
    for char in file_text:
        keyboard.type(char)
        if delay:
            time.sleep(delay)
        else:
            time.sleep(0.01) 

def print_help():
    help_text = """

 ______  ______  ______ _______ _     _ ______ _______ ______  
(_____ \(______)(_____ (_______| |   | (_____ (_______(_____ \ 
 _____) )_     _ _____) )  _   | |___| |_____) _____   _____) )
|  __  /| |   | |  ____/  | |  |_____  |  ____|  ___) |  __  / 
| |  \ \| |__/ /| |       | |   _____| | |    | |_____| |  \ \ 
|_|   |_|_____/ |_|       |_|  (_______|_|    |_______|_|   |_|
                                                               

                                  
    Usage: rdptyper.py -f <file_path>

    Options:
      -h, --help    Show this help message and exit
      -f FILE       Specify the file path to read text from
      -t Title      One word from title you rdp session window
      -d Delay, ms  Delay between type one symbol, depend on channel quallity. Default 0.01s
      -b            Convert to base64 you file

    Don't forget open notepad on rdp session windows
    """
    print(help_text)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument('-f', '--file', type=str, required=False, help='Specify the file path to read text from')
    parser.add_argument('-h', '--help', action='store_true', help='Show this help message and exit')
    parser.add_argument('-d', '--delay',type=float, required=False, help='Delay between type one symbol, depend on channel quallity. Default 0.01s')
    parser.add_argument('-t', '--title', type=str, required=False, help='One word from title you rdp session window')    
    parser.add_argument('-b', '--base64', action='store_true', required=False, help='Convert to base64 you file')    


    args = parser.parse_args()

    if args.help:
        print_help()
    elif args.file and args.title:
        type_text_in_rdp(args.file, args.delay, args.title, args.base64)
    elif args.title == None and args.file:
        print("No title specified. Use -h or --help for usage information.") 
    else:
        print("No file specified. Use -h or --help for usage information.")
