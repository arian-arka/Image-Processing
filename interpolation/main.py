from Interpolation import Interpolation
from MSE import MSE

if __name__ == '__main__':
    Interpolation('InputImage.bmp').nearsetNeighbor(512, 512).save('./Im_NNI.bmp')
    Interpolation('InputImage.bmp').bilinear(512, 512).save('./Im_BLI.bmp')

    mseNearestNeighbor = MSE('OriginalImage.bmp', 'Im_NNI.bmp').calculate()
    mseBilinear = MSE('OriginalImage.bmp', 'Im_BLI.bmp').calculate()
    print('mse nearest neighbor =',mseNearestNeighbor)
    print('mse bilinear =',mseBilinear)
    if mseNearestNeighbor > mseBilinear:
        print('bilinear is better')
    elif mseNearestNeighbor < mseBilinear:
        print('nearest neighbor is better')
    else:
        print('both are equal')