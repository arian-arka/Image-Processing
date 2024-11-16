import numpy
from PIL import Image

class Interpolation:
    def __init__(self, src):
        self.img = Image.open(src)

    def save(self, dst):
        self.img.save(dst)
        return self

    def nearsetNeighbor(self, newWidth, newHeight):
        width, height = self.img.size
        scaleW = newWidth / (width )
        scaleH = newHeight / (height)
        newImg = Image.new(self.img.mode, (newWidth, newHeight), 'white')
        for i in range(newWidth):
            for j in range(newHeight):
                x = min(width-1,numpy.floor(i / scaleW))
                y = min(height-1,numpy.floor(j / scaleH))
                pixel = self.img.getpixel((x, y))
                newImg.putpixel((i, j), pixel)
        self.img = newImg
        return self

    def findBilinearPixel(self, i, j, scaleW, scaleH, width, height):
        x = i * scaleW
        y = j * scaleH

        xBottom = int(x)
        yBottom = int(y)
        xTop = min(width - 1, numpy.ceil(x))
        yTop = min(height - 1, numpy.ceil(y))

        if xTop == xBottom and yTop == yBottom:
            return self.img.getpixel((int(x), int(y)))
        elif xTop == xBottom:
            q1 = self.img.getpixel((int(x), int(yBottom)))
            q2 = self.img.getpixel((int(x), int(yTop)))
            return q1 * (yTop - y) + q2 * (y - yBottom)
        elif yTop == yBottom:
            q1 = self.img.getpixel((int(xBottom), int(y)))
            q2 = self.img.getpixel((int(xTop), int(y)))
            return q1 * (xTop - x) + q2 * (x - xBottom)
        p00 = self.img.getpixel((int(xBottom), int(yBottom)))
        p01 = self.img.getpixel((int(xTop), int(yBottom)))
        p10 = self.img.getpixel((int(xBottom), int(yTop)))
        p11 = self.img.getpixel((int(xTop), int(yTop)))

        q1 = p00 * (xTop - x) + p01 * (x - xBottom)
        q2 = p10 * (xTop - x) + p11 * (x - xBottom)
        return q1 * (yTop - y) + q2 * (y - yBottom)

    def bilinear(self, newWidth, newHeight):
        width, height = self.img.size
        scaleW = width / newWidth
        scaleH = height / newHeight
        newImg = Image.new(self.img.mode, (newWidth, newHeight), 'white')
        for i in range(newWidth):
            for j in range(newHeight):
                pixel = self.findBilinearPixel(i, j, scaleW, scaleH, width, height)
                newImg.putpixel((i, j), int(pixel))
        self.img = newImg
        return self
