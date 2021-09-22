# Image Processing

# Imports
import pyautogui
from pynput import keyboard
from PIL import ImageEnhance
import time

def getProcessedScreenshot():
    im = pyautogui.screenshot()
    colorEnhancer = ImageEnhance.Color(im)
    monochrome = colorEnhancer.enhance(0) # Black and white
    contrastEnhancer = ImageEnhance.Contrast(monochrome)
    processedIm = contrastEnhancer.enhance(10) # Arbitrary factor to increase contrast to a maximum
    return processedIm

record = False

def onKeyPress(key):
    global record

    try:
        print('alphanumeric key {0} pressed'.format(key.char))
    except AttributeError:
        print('special key {0} pressed'.format(key))
    
        if key == keyboard.Key.home:
            record = True
        if key == keyboard.Key.page_up:
            record = False
        if record:
            t = time.time()
            #getProcessedScreenshot()
            dt = time.time() - t
            print(f"Elapsed Screenshot Time: {dt}")

def onKeyRelease(key):
    global record

    if key == keyboard.Key.end:
        # Stop listener
        return False

with keyboard.Listener(
        on_press=onKeyPress,
        on_release=onKeyRelease) as listener:
    listener.join()