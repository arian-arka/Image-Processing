from PIL import Image
import multiprocessing
import math

import numpy

def splitRows(count, cpuCount=40):
    step = count // cpuCount
    info = []
    offset = 0
    l = cpuCount
    for i in range(l):
        until = count if i + 1 == l else offset + step
        info.append({
            'id': i,
            'offset': offset,
            'until': until,
        })
        offset = until
    return info

def findIterativeT(numberOfLights, width, height):
    histogram = [x / (width * height) for x in numberOfLights]
    t = 128
    for i in range(1000):
        e1 = sum([(i + 1) * histogram[i] for i in range(t)])
        e2 = sum([(i + 1) * histogram[i] for i in range(t, 256)])
        newT = (e1 + e2) / 2
        newT = int(numpy.round(newT))
        if abs(newT - t) < 10 ** -7:
            return newT
        t = newT
    return t

def _numberOfEachLight(start, end, img, sharedMemory):
    sharedMemory[str(start) + '-' + str(end)] = []
    indices = [0 for x in range(end - start)]
    width, height = img.size
    for index in range(start, end):
        for i in range(width):
            for j in range(height):
                if img.getpixel((i, j)) == index:
                    indices[index - start] += 1
    sharedMemory[str(start) + '-' + str(end)] = indices

def numberOfEachLight(src):
    img = Image.open(src).convert('L')
    manager = multiprocessing.Manager()
    data = manager.dict()
    threads = []
    for info in splitRows(256, 40):
        threads.append(
            multiprocessing.Process(target=_numberOfEachLight, args=(info['offset'], info['until'], img, data)))
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    all = []
    for arr in data.values():
        for v in arr:
            all.append(v)
    return all

def windowLocalIterative(startY, endY, width, height, window, sharedMemory):
    img = sharedMemory['img']
    for y in range(startY, endY, window[1]):
        for x in range(0, width, window[0]):
            iterateY = endY if endY - y < window[1] else y + window[1]
            iterateX = width if width - x < window[0] else x + window[0]
            # print(x,iterateX,y,iterateY)
            # print(window)
            # print(iterateX,iterateY)
            # print('------------')
            indices = [0 for x in range(256)]
            for index in range(len(indices)):
                for _x in range(x, iterateX):
                    for _y in range(y, iterateY):
                        if img.getpixel((_x, _y)) == index:
                            indices[index] += 1
            # print(indices)
            t = findIterativeT(indices, width - x if width - x < window[0] else window[0],
                               endY - y if endY - y < window[1] else window[1])
            #
            for _x in range(x, iterateX):
                for _y in range(y, iterateY):
                    pixel = img.getpixel((_x, _y))
                    sharedMemory[str(_x) + ',' + str(_y)] = 255 if pixel > t else 0

def windowNiblackIterative(startY, endY, width, height, window, sharedMemory):
    img = sharedMemory['img']
    k = sharedMemory['k']
    for y in range(startY, endY, window[1]):
        for x in range(0, width, window[0]):
            iterateY = endY if endY - y < window[1] else y + window[1]
            iterateX = width if width - x < window[0] else x + window[0]

            sumOfPixels = 0
            for _x in range(x, iterateX):
                for _y in range(y, iterateY):
                    sumOfPixels += img.getpixel((_x, _y))

            windowLengthY = endY - y if endY - y < window[1] else window[1]
            windowLengthX = width - x if width - x < window[0] else window[0]

            avgOfPixels = sumOfPixels / (windowLengthY * windowLengthX)

            standardDeviation = 0
            for _x in range(x, iterateX):
                for _y in range(y, iterateY):
                    standardDeviation += (img.getpixel((_x, _y)) - avgOfPixels) ** 2

            standardDeviation = math.sqrt(standardDeviation / (windowLengthY * windowLengthX))
            standardDeviation = int(numpy.round(standardDeviation))

            #print(standardDeviation)

            t = int(numpy.round(avgOfPixels + (k * standardDeviation)))
            #print(t)
            for _x in range(x, iterateX):
                for _y in range(y, iterateY):
                    pixel = img.getpixel((_x, _y))
                    sharedMemory[str(_x) + ',' + str(_y)] = 255 if pixel > t else 0

def applyTInWindow(src, window, function, args):
    img = Image.open(src).convert('L')
    width, height = img.size

    manager = multiprocessing.Manager()
    data = manager.dict()
    data['img'] = img

    for key in args:
        data[key] = args[key]

    threads = []
    for info in splitRows(height, window[1]):
        # print(info)
        threads.append(
            multiprocessing.Process(target=function, args=(info['offset'], info['until'], width, height, window, data)))
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    newImg = Image.new(img.mode, (width, height), 'white')
    data.pop('img')
    for key in args:
        data.pop(key)
    keys = data.keys()
    print(len(keys))
    for key in keys:
        pixel = data[key]
        indices = key.split(',')
        # print(pixel,indices)
        # print(indices,pixel)
        newImg.putpixel((int(indices[0]), int(indices[1])), pixel)
    return newImg
    # else:
    #     all = []
    #     for arr in data.values():
    #         for v in arr:
    #             all.append(v)
    #     return all

class Binarization:
    def __init__(self, src):
        self.src = src
        self.img = Image.open(src).convert('L')

    def save(self, dst):
        self.img.save(dst)

    def T(self, t=128):
        width, height = self.img.size
        newImg = Image.new(self.img.mode, (width, height), 'white')
        [[newImg.putpixel((i, j), 255 if self.img.getpixel((i, j)) > t else 0) for j in range(height)] for i in
         range(width)]
        self.img = newImg
        return self

    def globalIterative(self):
        width, height = self.img.size
        t = findIterativeT(numberOfEachLight(self.src), width, height)
        print(t)
        return self.T(t)

    def localIterative(self, window):
        self.img = applyTInWindow(self.src, window, windowLocalIterative,{})
        return self

    def niblack(self, k, window):
        self.img = applyTInWindow(self.src, window, windowNiblackIterative, {'k': k})
        return self

if __name__ == "__main__":
    # Binarization('./image1.png').T(128).save('image1_t128.png')
    # Binarization('./image1.png').globalIterative().save('image1_globalIterative.png')
    # Binarization('./image1.png').localIterative((25,25)).save('image1_localIterative.png')
    # Binarization('./image1.png').niblack(0.3, (25, 25)).save('image1_niblack.png')
    # Binarization('./image1.png').niblack(0.8, (25, 25)).save('image1_niblack2.png')
    # Binarization('./image1.png').niblack(0.2, (25, 25)).save('image1_niblack3.png')
    # Binarization('./image1.png').niblack(-0.2, (25, 25)).save('image1_niblack4.png')
    Binarization('./image1.png').niblack(-0.2, (45, 45)).save('image1_niblack5.png')
