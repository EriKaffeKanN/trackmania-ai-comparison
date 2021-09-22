# Image Processing

# Imports
import pyautogui
from pynput import keyboard
from PIL import ImageEnhance
import time

class ImageProcessingModule:

    @staticmethod
    def record():
        t = time.time()
        getProcessedScreenshot()
        dt = time.time() - t
        print("Elapsed Screenshot Time: {0}".format(dt))

    @staticmethod
    def getProcessedScreenshot():
        im = pyautogui.screenshot()
        colorEnhancer = ImageEnhance.Color(im)
        monochrome = colorEnhancer.enhance(0) # Black and white
        contrastEnhancer = ImageEnhance.Contrast(monochrome)
        processedIm = contrastEnhancer.enhance(10) # Arbitrary factor to increase contrast to a maximum
        return processedIm

def onKeyPress(key):
    if key == keyboard.Key.home:
        recording = True
        with keyboard.Listener(
            on_press=awaitExit
            on_release=onKeyRelease
        ) as exitListener:
            exitListener.join()
        while recording:
            def awaitExit(key2):
                if key2 == keyboard.Key.page_up:
                    recording = False
            ImageProcessingModule.record()

def onKeyRelease(key):
    if key == keyboard.Key.end:
        # Stop listener
        return False
            
if __name__ == "main":
    with keyboard.Listener(
            on_press=onKeyPress,
            on_release=onKeyRelease) as listener:
        listener.join()

