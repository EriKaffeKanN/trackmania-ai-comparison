# Screenshot handling and image processing

from PIL.Image import Image
import pyautogui
from PIL import ImageEnhance, ImageDraw
import time
import math
from typing import List

class Ray:

    minBrightness = 5

    def __init__(self, theta) -> None:
        self.theta = theta
        self.stepX = math.cos(theta)
        self.stepY = -math.sin(theta)

    def cast(self, baseCoordinates, pixelMap, maxX, maxY) -> float:
        pos = baseCoordinates.copy()
        transformedPos = [0, 0]
        while pixelMap[math.floor(pos[0]), math.floor(pos[1])][0] > self.minBrightness: # R = B = G because monochrome, hence why im indexing pixelMap at 0
            pos[0] += self.stepX
            pos[1] += self.stepY
            transformedPos = [pos[0] - baseCoordinates[0], pos[1] - baseCoordinates[1]]
            if pos[0] < 0 or pos[1] < 0 or pos[0] > maxX or pos[1] > maxY:
                return math.sqrt(transformedPos[0]**2 + transformedPos[1]**2)
        return math.sqrt(transformedPos[0]**2 + transformedPos[1]**2) # FIX: Use numpy to increase efficiency

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

    # Returns array of all lengths from the base of a given image to the nearest
    # black pixel for each angle between angleMin and angleMax with step angleStep
    @staticmethod
    def getLineLengths(img, angleMin, angleMax, angleStep) -> List[int]:
        pixelMap = img.load()
        baseCoordinates = [img.size[0]//2, img.size[1]-1]
        lineLengths = []
        rayQuantity = int((angleMax-angleMin)//angleStep)
        for i in range(rayQuantity + 2):
            r = Ray(angleMin + angleStep*i)
            lineLengths.append(r.cast(baseCoordinates, pixelMap, img.size[0], img.size[1]))
        return lineLengths

    @staticmethod
    def visualizeLines(img, lineLengths, angleMin, angleMax, angleStep) -> None:
        draw = ImageDraw.Draw(img)
        baseCoordinates = [img.size[0]//2, img.size[1]-1]
        lineQuantity = int((angleMax-angleMin)//angleStep)
        for l in range(lineQuantity + 2):
            theta = angleMin + angleStep*l
            stepX = math.cos(theta)
            stepY = -math.sin(theta)
            pos = baseCoordinates.copy()
            while (pos[0]-baseCoordinates[0])*(pos[0]-baseCoordinates[0]) + (pos[1]-baseCoordinates[1])*(pos[1] - baseCoordinates[1]) < lineLengths[l]*lineLengths[l]:
                pos[0] += stepX
                pos[1] += stepY
            line = (baseCoordinates[0], baseCoordinates[1], int(pos[0]-1), int(pos[1]-1))
            draw.line(line, fill="red", width=5)
            bbox = (int(pos[0]-1) - 20, int(pos[1]-1) - 20, int(pos[0]-1) + 20, int(pos[1]-1) + 20)
            draw.ellipse(bbox, fill="red")
        img.show()