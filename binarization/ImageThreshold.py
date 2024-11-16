from PIL import Image
import numpy
import math

def applyT(img,t):
    width, height = img.size
    newImg = Image.new(img.mode, (width, height), 'white')
    [[newImg.putpixel((i, j), 255 if img.getpixel((i, j)) > t else 0) for j in range(height)] for i in range(width)]
    return newImg

def applyTInWindow(window,t):
    for i in range(window['w']):
        for j in range(window['h']):
            window['window'][i][j] = 255 if window['window'][i][j] > t else 0
    return window

def getWindow(img,x,y,w,h):
    width, height = img.size

    actualWidth = w if x + w <= width else width - x
    actualHeight = h if y + h <= height else height - y

    return {
        'window' : [[img.getpixel((i, j)) for j in range(y,y+actualHeight)] for i in range(x,x+actualWidth)],
        'w' : actualWidth,
        'h' : actualHeight
    }

def setWindow(img,x,y,window):
    #print(x,y,window['w'],window['h'])
    # for i in range(x, x + window['w']):
    #     for j in range(y, y + window['h']):
    #         img.putpixel((i, j), window['window'][i-x][j-j])

    [[img.putpixel((i, j),window['window'][i-x][j-y]) for j in range(y, y + window['h'])] for i in range(x, x + window['w'])]

def lightOccurances(window):
    indices = [0 for x in range(256)]
    for i in range(window['w']):
        for j in range(window['h']):
            for index in range(256):
                if window['window'][i][j] == index:
                    indices[index] += 1
    return indices

def histogram(data,count):
    return [val / count for val in data]

def findT(hist,T = 128):
    t = T
    for i in range(1000):
        e1 = sum([(ii + 1) * hist[ii] for ii in range(t)])
        e2 = sum([(ii + 1) * hist[ii] for ii in range(t, 256)])
        newT = (e1 + e2) / 2
        newT = int(numpy.round(newT))
        if abs(newT - t) < 10 ** -7:
            return t
        t = newT
    return t

def meanOfWindow(window):
    sum = 0
    for i in range(window['w']):
        for j in range(window['h']):
            sum +=  window['window'][i][j]
    return sum / (window['w'] * window['h'])

def stdOfWindow(window,avg):
    sum = 0
    for i in range(window['w']):
        for j in range(window['h']):
            sum += (window['window'][i][j] - avg) ** 2
    std = math.sqrt(sum / (window['w'] * window['h']))
    return std