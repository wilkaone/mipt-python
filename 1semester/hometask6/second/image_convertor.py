import numpy as np
import math
import copy

from image import ImageBinary
from image import ImageMonochrome
from image import ImageColor

class ImageConvertor:
    def __init__(self):
        pass
    
    def monochrome2monochrome(self, image):
        result = ImageMonochrome(image.get_width(), image.get_height(), [])
        histogram = {i: len([x for x in image.get_data() if x == i]) / image.get_size()
                     for i in range(256)}
        
        average_initial = np.sum([key * value for key, value in histogram.items()])
        stddev_initial = math.sqrt(np.sum([value * (key - average_initial)**2 for key, value in histogram.items()]))

        average_final = np.mean(image.get_data())
        stddev_final = np.std(image.get_data())
        result.set_data(list(map(int, stddev_initial * (np.array(image.get_data()) - average_final) / stddev_final + average_initial)))

        return result
    
    def color2color(self, image):
        result = ImageColor(image.get_width(), image.get_height(), [])
        data_array = np.array(image.get_data())
        color_channels = [data_array[:, :, i] for i in range(3)]

        corrected_channels = []
        for channel in color_channels:
            average_initial, stddev_initial = np.mean(channel), np.std(channel)
            corrected_channels.append((channel - average_initial) / stddev_initial)
        
        result.set_data(np.stack(corrected_channels, axis=2).astype(int).tolist())
        return result

    def binary2binary(self, image):
        return copy.deepcopy(image)

    def color2monochrome(self, image):
        result = ImageMonochrome(image.get_width(), image.get_height(), [])
        result.set_data([(red + green + blue) // 3 for red, green, blue in image.get_data()])
        return result

    def monochrome2color(self, image, palette):
        result = ImageColor(image.get_width(), image.get_height(), [])
        result.set_data([palette[gray] for gray in image.get_data()])
        return result

    def monochrome2binary(self, image, threshold=128):
        result = ImageBinary(image.get_width(), image.get_height(), [])
        result.set_data([255 if pixel > threshold else 0 for pixel in image.get_data()])
        return result

    def binary2monochrome(self, image):
        result = ImageMonochrome(image.get_width(), image.get_height(), [0] * image.get_size())
        white_pixels = [(i % image.get_width(), i // image.get_width()) 
                        for i in range(image.get_size()) if image.get_data()[i] == 255]

        max_distance = math.sqrt(image.get_width() ** 2 + image.get_height() ** 2)
        for i in range(image.get_size()):
            if image.get_data()[i] == 255:
                result.get_data()[i] = 255
            else:
                x, y = i % image.get_width(), i // image.get_width()
                distance = min(math.sqrt((x - wx) ** 2 + (y - wy) ** 2) for wx, wy in white_pixels)
                result.get_data()[i] = int((1 - distance / max_distance) * 255)
        return result

    def color2binary(self, image, threshold=128):
        monochrome_image = self.color2monochrome(image)
        return self.monochrome2binary(monochrome_image, threshold)

    def binary2color(self, image, palette):
        monochrome_image = self.binary2monochrome(image)
        return self.monochrome2color(monochrome_image, palette)

    def __del__(self):
        pass