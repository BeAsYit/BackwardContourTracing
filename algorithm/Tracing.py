from PIL import Image


class Tracing:
    def __init__(self):
        self.backgroundPixels = []
        self.contourPixels = []
        self.image_params = self.image_params()
        self.search = ((1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1,-1), (0, -1), (1, -1))

    def find_backgroundPixels(self):
        for height in range(self.image_params[0]):
            for width in range(self.image_params[1]):
                if self.image_params[2][height, width][0] > 15 or self.image_params[2][height, width][1] > 15 or \
                                self.image_params[2][height, width][2] > 15:
                    continue
                self.backgroundPixels.append([height, width])

    def tracing(self):
        startP = activeP = self.find_start_pixel()
        cw_neighbourP = self.clockwise(activeP)
        counter_cw_neighbourP = self.counter_clockwise(activeP)
        if cw_neighbourP != counter_cw_neighbourP:
            endP = startP
            self.contourPixels.append(cw_neighbourP)
            activeP = cw_neighbourP

    def find_start_pixel(self):
        for height in self.image_params[0]:
            for width in self.image_params[1]:
                if [height, width] not in self.backgroundPixels:
                    return [height, width]

    def clockwise(self, activeP, previousP=False, index_previousP = 0):
        if previousP:
            pass
        else:
            for i in self.search:
                if [(activeP[0]+i[0]), (activeP[1]+i[1])] not in self.backgroundPixels:
                    return [(activeP[0]+i[0]), (activeP[1]+i[1])]

    def counter_clockwise(self, activeP):
        for i in reversed(self.search):
            if [(activeP[0]+i[0]), (activeP[1]+i[1])] not in self.backgroundPixels:
                return [(activeP[0]+i[0]), (activeP[1]+i[1])]

    @staticmethod
    def image_params():
        image = Image.open("../data/1.jpg")
        height = image.size[0]
        width = image.size[1]
        pixels = image.load()
        return height, width, pixels


a = Tracing()
a.find_backgroundPixels()
