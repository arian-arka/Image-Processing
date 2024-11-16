from ImageThreshold import *

def applyGlobalIterative(src):
    img = Image.open(src).convert('L')
    width, height = img.size
    window = getWindow(img,0,0,width,height)
    lights = lightOccurances(window)
    hist = histogram(lights,width * height)
    t = findT(hist)
    print('t:',t)
    return applyT(img,t)


if __name__ == "__main__":
    applyGlobalIterative('image1.png').save('image1_global_iterative.png')
