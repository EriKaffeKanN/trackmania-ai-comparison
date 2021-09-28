# Image Processing

# Imports
from PIL.Image import Image
import pyautogui
import keyboard
from PIL import ImageEnhance
import time
import math

class Ray:

    minBrightness = 5

    def __init__(self, theta) -> None:
        self.theta = theta
        self.stepX = math.cos(theta)
        self.stepY = math.sin(theta)

    def cast(self, baseCoordinates, pixelMap):
        pos = baseCoordinates.copy()
        while pixelMap[math.floor(pos.x), math.floor(pos.y)][0] > self.minBrightness: # R = B = G because monochrome
            pos[0] += self.stepX
            pos[1] += self.stepY
        return math.sqrt(pos[0]*pos[0] + pos[1]*pos[1]) # FIX: Use numpy

class ImageProcessingModule:

    @staticmethod
    def benchmark() -> None:
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
            r = Ray(angleMin + angleStep*i)
        return None

while True:
    if keyboard.is_pressed("home"):
        while not keyboard.is_pressed("end"):
            ImageProcessingModule.getLineLengths(ImageProcessingModule.getProcessedScreenshot(), 0, 0, 0)
        print("Done recording")
    if keyboard.is_pressed("esc"):
        break