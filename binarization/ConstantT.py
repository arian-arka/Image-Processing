from ImageThreshold import *

def applyConstantT(src,t = 55):
    img = Image.open(src).convert('L')
    return applyT(img,t)

if __name__ == "__main__":
    applyConstantT('image1.png').save('image1_constant_t_128.png')
