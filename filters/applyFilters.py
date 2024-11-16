import matplotlib.pyplot as plt
import numpy as np
import numpy.fft
from PIL import Image
import matplotlib
from filters import Filters, transformPI

def applyFilterThenPlot(name,src, filter, *args):
    img = Image.open(src).convert('L')
    imgMatrix = np.array([[img.getpixel((i, j)) for j in range(img.size[1])] for i in range(img.size[0])])

    plt.figure(num=name+'-image')
    plt.imshow(imgMatrix, cmap='gray')
    plt.show()

    args = list(args)
    args.insert(0, img.size)
    strFilter = 'Filters.{0}(*args)'.format(filter)

    filter = np.array(eval(strFilter, {'args': args, 'Filters': Filters}))
    plt.figure(num=name+'-filter')
    plt.imshow(filter, cmap='gray')
    plt.show()

    f = np.fft.fft2(np.array(imgMatrix))
    f = numpy.fft.fftshift(numpy.array(f))
    plt.figure(num=name + '-fft')
    plt.imshow(abs(f), cmap='gray')
    plt.show()

    out = f * filter
    out = np.fft.ifftshift(out)
    out = np.fft.ifft2(out)
    out = np.abs(out)

    newImg = Image.new(img.mode, (img.size), 'white')
    [[newImg.putpixel((i, j), int(out[i][j])) for j in range(img.size[1])] for i in range(img.size[0])]
    newImg.save('test.bmp')
    plt.figure(num=name+'-image')
    plt.imshow(out, cmap='gray')
    plt.show()

applyFilterThenPlot('idealLPF-45','./lena.bmp','idealLPF',45) #pi/4
applyFilterThenPlot('idealLPF-90','./lena.bmp','idealLPF',90) #pi/2
applyFilterThenPlot('idealLPF-120','./lena.bmp','idealLPF',120) #2pi/3

applyFilterThenPlot('gaussianLPF-45','./lena.bmp','gaussianLPF',45) #pi/4
applyFilterThenPlot('gaussianLPF-90','./lena.bmp','gaussianLPF',90) #pi/2
applyFilterThenPlot('gaussianLPF-120','./lena.bmp','gaussianLPF',120) #2pi/3

applyFilterThenPlot('butterworthLPF-45','./lena.bmp','butterworthLPF',45,2) #pi/4
applyFilterThenPlot('butterworthLPF-90','./lena.bmp','butterworthLPF',90,2) #pi/2,n=2
applyFilterThenPlot('butterworthLPF-120','./lena.bmp','butterworthLPF',120,2) #2pi/3,n=2

applyFilterThenPlot('idealHPF-45','./lena.bmp','idealHPF',45) #pi/4
applyFilterThenPlot('idealHPF-90','./lena.bmp','idealHPF',90) #pi/2
applyFilterThenPlot('idealHPF-120','./lena.bmp','idealHPF',120) #2pi/3

applyFilterThenPlot('gaussianHPF-45','./lena.bmp','gaussianHPF',45) #pi/4
applyFilterThenPlot('gaussianHPF-90','./lena.bmp','gaussianHPF',90) #pi/2
applyFilterThenPlot('gaussianHPF-120','./lena.bmp','gaussianHPF',120) #2pi/3

applyFilterThenPlot('butterworthHPF-45','./lena.bmp','butterworthHPF',45,2) #pi/4,n=2
applyFilterThenPlot('butterworthHPF-90','./lena.bmp','butterworthHPF',90,2) #pi/2,n=2
applyFilterThenPlot('butterworthHPF-120','./lena.bmp','butterworthHPF',120,2) #2pi/3,n=2

applyFilterThenPlot('notchIdeal1','./noisyimage1.bmp','notchIdeal',75,108,6) #u0=108,v0=6
applyFilterThenPlot('notchGaussian1','./noisyimage1.bmp','notchGaussian',75,108,6) #u0=108,v0=6
applyFilterThenPlot('notchButterworh1','./noisyimage1.bmp','notchButterworh',75,108,6,2) #u0=108,v0=6
applyFilterThenPlot('notchIdeal2','./noisyimage2.bmp','notchIdeal',75,6,108) #u0=6,v0=108
applyFilterThenPlot('notchGaussian2','./noisyimage2.bmp','notchGaussian',75,6,108) #u0=6,v0=108
applyFilterThenPlot('notchButterworth2','./noisyimage2.bmp','notchButterworh',75,6,108,2) #u0=6,v0=108

applyFilterThenPlot('idealBSF1-22_5','./noisyimage1.bmp','idealBSF',75,22.5)
applyFilterThenPlot('idealBSF1-11_25','./noisyimage1.bmp','idealBSF',75,22.5/2)
applyFilterThenPlot('idealBSF2-22_5','./noisyimage2.bmp','idealBSF',75,22.5)
applyFilterThenPlot('idealBSF2-11_25','./noisyimage2.bmp','idealBSF',75,22.5/2)

applyFilterThenPlot('gaussianBSF1-22_5','./noisyimage1.bmp','gaussianBSF',75,22.5)
applyFilterThenPlot('gaussianBSF1-11_25','./noisyimage1.bmp','gaussianBSF',75,22.5/2)
applyFilterThenPlot('gaussianBSF2-22_5','./noisyimage2.bmp','gaussianBSF',75,22.5)
applyFilterThenPlot('gaussianBSF2-11_25','./noisyimage2.bmp','gaussianBSF',75,22.5/2)

applyFilterThenPlot('butterworthBSF1-22_5','./noisyimage1.bmp','butterworthBSF',75,22.5,2)
applyFilterThenPlot('butterworthBSF1-11_25','./noisyimage1.bmp','butterworthBSF',75,22.5/2,2)
applyFilterThenPlot('butterworthBSF2-22_5','./noisyimage2.bmp','butterworthBSF',75,22.5,2)
applyFilterThenPlot('butterworthBSF2-11_25','./noisyimage2.bmp','butterworthBSF',75,22.5/2,2)

applyFilterThenPlot('idealBPF1-22_5','./noisyimage1.bmp','idealBPF',75,22.5)
applyFilterThenPlot('idealBPF1-11_25','./noisyimage1.bmp','idealBPF',75,22.5/2)
applyFilterThenPlot('idealBPF2-22_5','./noisyimage2.bmp','idealBPF',75,22.5)
applyFilterThenPlot('idealBPF2-11_25','./noisyimage2.bmp','idealBPF',75,22.5/2/2)

applyFilterThenPlot('gaussianBPF1-22_5','./noisyimage1.bmp','gaussianBPF',75,22.5)
applyFilterThenPlot('gaussianBPF1-11_25','./noisyimage1.bmp','gaussianBPF',75,22.5/2)
applyFilterThenPlot('gaussianBPF2-22_5','./noisyimage2.bmp','gaussianBPF',75,22.5)
applyFilterThenPlot('gaussianBPF2-11_25','./noisyimage2.bmp','gaussianBPF',75,22.5/2)

applyFilterThenPlot('butterworthBPF1-22_5','./noisyimage1.bmp','butterworthBPF',75,22.5,2)
applyFilterThenPlot('butterworthBPF1-11_25','./noisyimage1.bmp','butterworthBPF',75,22.5/2,2)
applyFilterThenPlot('butterworthBPF2-22_5','./noisyimage2.bmp','butterworthBPF',75,22.5,2)
applyFilterThenPlot('butterworthBPF2-11_25','./noisyimage2.bmp','butterworthBPF',75,22.5/2,2)

