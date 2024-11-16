# from PIL import Image
# import cv2,numpy
#
# m=[2,4]
# n=[4,2]
# img = Image.open('./stgImage_991531041_pixelA_5_3_pixelB_3_5.png')
# width, height = img.size
# newImg = Image.new('L', (width // 8, height // 8), 'white')
# for i in range(0, width, 8):
#     print(i)
#     for j in range(0, height, 8):
#         l = []
#         for ii in range(8):
#             filter = []
#             for jj in range(8):
#                 filter.append(img.getpixel((i+ii,j+jj)))
#             l.append(filter)
#         l = cv2.dct(numpy.float32(l))
#         if l[m[0]][m[1]] > l[n[0]][n[1]]:
#             b = 255
#         else:
#             b=0
#         newImg.putpixel((i // 8, j // 8), b)
# newImg.save('test.png')

from scipy.io import loadmat
d = loadmat('./keyX_keyY_991531041(4)(1)(1).mat')
x = d['keyX']
y = d['keyY']