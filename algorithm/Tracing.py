from PIL import Image


im = Image.open("../data/1.jpg")

print(im.format, im.size, im.mode)
pix = im.load()
print(pix)
print(pix[0,0], pix[20,20], pix[426,240])
class Tracing:
    def __init__(self):
        self.backgroundPixels = []
        self.contourPixels = []

    def find_backgroundPixels(self):
        pass
