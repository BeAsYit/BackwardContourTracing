from PIL import Image
import math


class BackwardContourTracing:
    def __init__(self, picture):
        self.picture_name = picture
        image = Image.open("../data/" + picture)
        self.backgroundPixels = []
        self.contourPixels = []
        self.image_params = (image.size[1], image.size[0], image.load())
        self.search = ((0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1))

    def find_background_pixels(self, xy):
        try:
            return math.sqrt(self.image_params[2][xy[0], xy[1]][0] ** 2 + self.image_params[2][xy[0], xy[1]][1] ** 2 +
                             self.image_params[2][xy[0], xy[1]][2] ** 2) < 50
        except IndexError:
            return True

    def tracing(self, mode):
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
                        if not activeP or not contour_neighbourP:
                            break
                        self.contourPixels.append(contour_neighbourP)
                        previous_index = self.find_previous_index(contour_neighbourP, activeP)
                        activeP = contour_neighbourP
                    elif contour_neighbourP in self.contourPixels:
                        previous_index = self.find_previous_index(contour_neighbourP, activeP)
                        self.contourPixels.remove(activeP)
                        self.backgroundPixels.append(activeP)
                        activeP = self.contourPixels[-1]
                elif contour_neighbourP == endP:
                    break
        self.draw_contour(mode)

    def draw_contour(self, mode):
        img = Image.new("RGB", (self.image_params[1], self.image_params[0]))
        for height in range(self.image_params[0]):
            for width in range(self.image_params[1]):
                img.putpixel((width, height), self.image_params[2][width, height])
        for pixel in self.contourPixels:
            try:
                img.putpixel(pixel, (0, 255, 0))
            except IndexError:
                pass
        if mode == "show":
            img.show()
        elif mode == "save":
            img.save(self.picture_name, "JPEG")

    def find_start_pixel(self):
        for height in range(self.image_params[0]):
            for width in range(self.image_params[1]):
                if not math.sqrt(self.image_params[2][width, height][0] ** 2 + self.image_params[2][width, height][1]
                        ** 2 + self.image_params[2][width, height][2] ** 2) < 50:
                    return width, height

    def clockwise(self, activeP, previousP=False, index_previousP=0):
        if previousP:
            check = index_previousP % 8
            new_search = self.search[check:] + self.search[:check]
            for i in new_search:
                if (activeP[0] + i[0], activeP[1] + i[1]) not in self.backgroundPixels and \
                        not self.find_background_pixels((activeP[0] + i[0], activeP[1] + i[1])):
                    return activeP[0] + i[0], activeP[1] + i[1]
        else:
            for i in self.search:
                if (activeP[0] + i[0], activeP[1] + i[1]) not in self.backgroundPixels and \
                        not self.find_background_pixels((activeP[0] + i[0], activeP[1] + i[1])):
                    return activeP[0] + i[0], activeP[1] + i[1]

    def counter_clockwise(self, activeP):
        for i in reversed(self.search):
            if (activeP[0] + i[0], activeP[1] + i[1]) not in self.backgroundPixels and \
                    not self.find_background_pixels((activeP[0] + i[0], activeP[1] + i[1])):
                return activeP[0] + i[0], activeP[1] + i[1]

    def find_previous_index(self, newP, active):
        return self.search.index((newP[0] - active[0], newP[1] - active[1])) - 1


a = BackwardContourTracing(input("Please, enter name of a file, and it's extension\nExample: 1.jpg\n"))
a.tracing(input(
    "If you want to save new picture, enter word save\nIf you want to just look at new picture, enter word show:\n"))
