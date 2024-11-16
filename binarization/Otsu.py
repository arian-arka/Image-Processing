from ImageThreshold import *

def applyLocalIterative(src):
    img = Image.open(src).convert('L').copy()
    width, height = img.size
    window = getWindow(img, 0, 0, width, height)
    lightOccurances = [0 for i in range(256)]

    for light in range(256):
        beforeLight = []
        afterLight = []
        print(light)
        for i in range(width):
            for j in range(height):
                pixel = window['window'][i][j]
                if light <= pixel:
                    afterLight.append(pixel)
                else:
                    beforeLight.append(pixel)
        meanBefore = sum(beforeLight) / len(beforeLight) if len(beforeLight) else 0
        meanAfter = sum(afterLight) / len(afterLight) if len(afterLight) else 0
        lightOccurances[light] = len(beforeLight) * len(afterLight) * (meanBefore - meanAfter) ** 2

    t = 0
    for i in range(len(lightOccurances)):
        if lightOccurances[t] < lightOccurances[i]:
            t = i
    print(t)

    return applyT(img, t)


if __name__ == "__main__":
    applyLocalIterative('image1.png').save('image1_otsu.png')
