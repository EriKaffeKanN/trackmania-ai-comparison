# Image Processing

# Imports
import pyautogui
from pynput import keyboard

def getProcessedScreenshot():
    im1 = pyautogui.screenshot("images.png")

exit = False

def onKeyPress(key):
    try:
        print('alphanumeric key {0} pressed'.format(key.char))
    
        if key.char == 's':
            getProcessedScreenshot()
    except AttributeError:
        print('special key {0} pressed'.format(key))

def onKeyRelease(key):
    print('{0} released'.format(key))
    if key == keyboard.Key.esc:
        # Stop listener
        return False

with keyboard.Listener(
        on_press=onKeyPress,
        on_release=onKeyRelease) as listener:
    listener.join()

