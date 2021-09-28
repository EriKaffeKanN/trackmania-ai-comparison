# Image Processing

# Imports
from PIL.Image import Image
import pyautogui
import keyboard
from PIL import ImageEnhance
import time
import math

class Ray:
    def __init__(self) -> None:
        pass

class ImageProcessingModule:

    @staticmethod
    def record() -> None:
        t = time.time()
        ImageProcessingModule.getProcessedScreenshot()
        dt = time.time() - t
        print("Elapsed Screenshot Time: {0}".format(dt))

    @staticmethod
    def getProcessedScreenshot() -> Image:
        im = pyautogui.screenshot()
        colorEnhancer = ImageEnhance.Color(im)
        monochrome = colorEnhancer.enhance(0) # Black and white
        contrastEnhancer = ImageEnhance.Contrast(monochrome)
        processedIm = contrastEnhancer.enhance(10) # Arbitrary factor to increase contrast to a maximum
        return processedIm

    @staticmethod
    def getLineLengths(img, angleMin, angleMax, angleStep) -> list[int]:
        pixelMap = img.load()
        baseCoordinates = [img.size[0]//2, img.size[1]-1]
        rayQuantity = (angleMax-angleMin)//angleStep
        for i in range(rayQuantity):
            theta = angleMin + angleStep*i
            stepX = math.cos(theta)
            stepY = math.sin(theta)
        return None


while True:
    if keyboard.is_pressed("home"):
        while not keyboard.is_pressed("end"):
            ImageProcessingModule.getLineLengths(ImageProcessingModule.getProcessedScreenshot(), 0, 0, 0)
        print("Done recording")
    if keyboard.is_pressed("esc"):
        break