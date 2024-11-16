import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
import matplotlib
from filters import Filters

img = Image.open('./lena.bmp')
imgMatrix = [[img.getpixel((i, j)) for j in range(img.size[1])] for i in range(img.size[0])]

plt.figure(num='ideal low pass filter')
plt.imshow(np.array(Filters.idealLPF(img.size, 50 / 6)), cmap='gray')
plt.show()

plt.figure(num='Ideal High pass Filter')
plt.imshow(np.array(Filters.idealHPF(img.size, 50 / 6)), cmap='gray')
plt.show()
plt.figure(num='Ideal Band Pass filter')

plt.imshow(np.array(Filters.idealBPF(img.size, 50 / 6,10)), cmap='gray')
plt.show()
plt.figure(num='Ideal Band Stop filter')

plt.imshow(np.array(Filters.idealBSF(img.size, 50 / 6,10)), cmap='gray')
plt.show()
plt.figure(num='Gaussian Low Pass filter')

plt.imshow(np.array(Filters.gaussianLPF(img.size, 50 / 6)), cmap='gray')
plt.show()
plt.figure(num='Gaussian High Pass filter')

plt.imshow(np.array(Filters.gaussianHPF(img.size, 50 / 6)), cmap='gray')
plt.show()
plt.figure(num='Gaussian Band Pass filter')

plt.imshow(np.array(Filters.gaussianBPF(img.size, 50 / 6,10)), cmap='gray')
plt.show()
plt.figure(num='Gaussian Band Stop filter')

plt.imshow(np.array(Filters.gaussianBSF(img.size, 50 / 6,10)), cmap='gray')
plt.show()
plt.figure(num='Butterworth low pass filter')

plt.imshow(np.array(Filters.butterworthLPF(img.size, 50 / 6, 1)), cmap='gray')
plt.show()
plt.figure(num='Butterworth high pass filter')

plt.imshow(np.array(Filters.butterworthHPF(img.size, 50 / 6, 1)), cmap='gray')
plt.show()
plt.figure(num='Butterworth Band Pass filter')

plt.imshow(np.array(Filters.butterworthBPF(img.size, 50 / 6, 10, 1)), cmap='gray')
plt.show()
plt.figure(num='Butterworth band stop filter')

plt.imshow(np.array(Filters.butterworthBSF(img.size, 50 / 6, 10, 1)), cmap='gray')
plt.show()
plt.figure(num='Notch ideal filter')

plt.imshow(np.array(Filters.notchIdeal(img.size, 50 / 6, 5, 5)), cmap='gray')
plt.show()
plt.figure(num='Notch gaussian filter')

plt.imshow(np.array(Filters.notchGaussian(img.size, 50 / 6, 5, 5)), cmap='gray')
plt.show()

plt.figure(num='Notch .butterworth filter')

plt.imshow(np.array(Filters.notchButterworh(img.size, 50 / 6, 5, 5,2)), cmap='gray')
plt.show()