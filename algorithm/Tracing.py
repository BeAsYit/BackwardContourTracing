from PIL import Image


class Tracing:
    def __init__(self):
        self.backgroundPixels = []
        self.contourPixels = []
        self.image_params = self.image_params()
        self.search = ((0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1))

    def find_backgroundPixels(self):
        for height in range(self.image_params[0]):
            for width in range(self.image_params[1]):
                if self.image_params[2][width, height][0] > 50 or self.image_params[2][width, height][1] > 50 or \
                                self.image_params[2][width, height][2] > 50:
                    continue
                self.backgroundPixels.append((width, height))
        print("formed")

    def tracing(self):
        print("Tracing")
        startP = activeP = self.find_start_pixel()
        cw_neighbourP = self.clockwise(activeP)
        counter_cw_neighbourP = self.counter_clockwise(activeP)
        if cw_neighbourP != counter_cw_neighbourP:
            endP = startP
            self.contourPixels.append(endP)
            self.contourPixels.append(cw_neighbourP)
            previous_index = self.find_previous_index(cw_neighbourP, activeP)
            activeP = cw_neighbourP
            while True:
                contour_neighbourP = self.clockwise(activeP, True, previous_index)
                if contour_neighbourP != endP:
                    if contour_neighbourP not in self.contourPixels:
                        self.contourPixels.append(contour_neighbourP)
                    else:
                        break
                    previous_index = self.find_previous_index(activeP, contour_neighbourP)
                    activeP = contour_neighbourP
                elif contour_neighbourP == endP:
                    break
        print(self.contourPixels)

    def draw_countour(self):
        img = Image.new('RGB', (self.image_params[1], self.image_params[0]))

        for pixel in self.backgroundPixels:
            img.putpixel(pixel, (255, 255, 255))

        for pixel in self.contourPixels:
            img.putpixel(pixel, (255, 0, 0))
        img.show()

    def find_start_pixel(self):
        print("finding start pixel")
        for height in range(self.image_params[0]):
            for width in range(self.image_params[1]):
                if self.image_params[2][width, height][0] > 50 or self.image_params[2][width, height][1] > 50 or \
                                self.image_params[2][width, height][2] > 50:
                    print("found")
                    print(width, height)
                    return [width, height]

    def clockwise(self, activeP, previousP=False, index_previousP=0):
        if previousP:
            check = (index_previousP + 1) % 8
            new_search = self.search[check:] + self.search[:check]
            for i in new_search:
                if [(activeP[0] + i[0]), (activeP[1] + i[1])] not in self.backgroundPixels:
                    return [(activeP[0] + i[0]), (activeP[1] + i[1])]
        else:
            for i in self.search:
                if [(activeP[0] + i[0]), (activeP[1] + i[1])] not in self.backgroundPixels:
                    return [(activeP[0] + i[0]), (activeP[1] + i[1])]

    def counter_clockwise(self, activeP):
        print("Counter clockwise")
        for i in reversed(self.search):
            if [(activeP[0] + i[0]), (activeP[1] + i[1])] not in self.backgroundPixels:
                return [(activeP[0] + i[0]), (activeP[1] + i[1])]

    def find_previous_index(self, previous, active):
        return self.search.index((previous[0] - active[0], previous[1] - active[1])) + 1

    @staticmethod
    def image_params():
        image = Image.open("../data/1.jpg")
        width = image.size[0]
        height = image.size[1]
        pixels = image.load()
        return height, width, pixels


a = Tracing()
a.find_backgroundPixels()
a.tracing()
a.draw_countour()
