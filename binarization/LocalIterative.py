from ImageThreshold import *

def applyLocalIterative(src, windowX, windowY):
    img = Image.open(src).convert('L').copy()
    width, height = img.size

    for i in range(0,width,windowX):
        for j in range(0,height,windowY):
            window = getWindow(img, i, j, windowX, windowY)
            lights = lightOccurances(window)
            hist = histogram(lights, windowX * windowY)
            t = findT(hist)
            setWindow(img,i,j, applyTInWindow(window,t) )

    return img

if __name__ == "__main__":
    applyLocalIterative('image1.png', 25, 25).save('image1_local_iterative.png')
