from ImageThreshold import *


def applyNiblack(src,k, windowX, windowY):
    img = Image.open(src).convert('L').copy()
    width, height = img.size
    for i in range(0,width,windowX):
        print(i)
        for j in range(0,height,windowY):
            window = getWindow(img, i, j, windowX, windowY)
            mean = meanOfWindow(window)
            std = stdOfWindow(window,mean)
            t = int(numpy.round(mean + (k * std)))
            window = applyTInWindow(window, t)
            setWindow(img, i, j, window)
    return img

if __name__ == "__main__":
    applyNiblack('image1.png',-0.2, 25, 25).save('image1_niblack.png')
