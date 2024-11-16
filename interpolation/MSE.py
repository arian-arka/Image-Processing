from PIL import Image

class MSE:
    def __init__(self, src,dst):
        self.srcImg = Image.open(src)
        self.dstImg = Image.open(dst)

    def calculate(self):
        width,height  = self.srcImg.size
        n = height * width
        summation = 0
        for i in range(width):
            for j in range(height):
                summation += (self.srcImg.getpixel((i,j)) - self.dstImg.getpixel((i,j))) ** 2
        print(summation,n)
        return summation / n