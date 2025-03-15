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
        if not isinstance(image, ImageMonochrome):
            raise TypeError("[IMAGE_CONVERTOR ERROR]: Input image != type ImageMonochrome (reason: monochrome2monochrome() ).")

        result = ImageMonochrome(image.get_width(), image.get_height(), [0] * image.get_size())
        histogram = {i: len([x for x in image.get_data() if x == i]) / image.get_size()
                     for i in range(256)}
        
        average_initial = np.sum([key * value for key, value in histogram.items()])
        stddev_initial = math.sqrt(np.sum([value * (key - average_initial)**2 for key, value in histogram.items()]))

        average_final = np.mean(image.get_data())
        stddev_final = np.std(image.get_data())
        result.set_data(list(map(int, stddev_initial * (np.array(image.get_data()) - average_final) / stddev_final + average_initial)))

        return result
    
    def color2color(self, image):
        if not isinstance(image, ImageColor):
            raise TypeError("[IMAGE_CONVERTOR ERROR]: Input image != type ImageColor (reason: color2color() ).")

        result = ImageColor(image.get_width(), image.get_height(), [[0, 0, 0]] * image.get_size())
        data_array = np.array(image.get_data())
        color_channels = [data_array[:, :, i] for i in range(3)]

        corrected_channels = []
        for channel in color_channels:
            average_initial, stddev_initial = np.mean(channel), np.std(channel)
            corrected_channels.append((channel - average_initial) / stddev_initial)
        
        result.set_data(np.stack(corrected_channels, axis=2).astype(int).tolist())
        return result

    def binary2binary(self, image):
        if not isinstance(image, ImageBinary):
            raise TypeError("[IMAGE_CONVERTOR ERROR]: Input image != type ImageBinary (reason: binary2binary() ).")
        
        return copy.deepcopy(image)

    def color2monochrome(self, image):
        if not isinstance(image, ImageColor):
            raise TypeError("[IMAGE_CONVERTOR ERROR]: Input image != type ImageColor (reason: color2monochrome() ).")
        
        result = ImageMonochrome(image.get_width(), image.get_height(), [0] * image.get_size())
        result.set_data([(red + green + blue) // 3 for red, green, blue in image.get_data()])
        return result

    def monochrome2color(self, image, palette):
        if not isinstance(image, ImageMonochrome):
            raise TypeError("[IMAGE_CONVERTOR ERROR]: Input image != type ImageMonochrome (reason: monochrome2color() ).")
        if not isinstance(palette, list) or len(palette) != 256:
            raise ValueError("[IMAGE_CONVERTOR ERROR]: Palette must be a list of 256 colors for monochrome to color conversion (reason: monochrome2color() ).")
        
        result = ImageColor(image.get_width(), image.get_height(), [[0, 0, 0]] * image.get_size())
        result.set_data([palette[gray] for gray in image.get_data()])
        return result

    def monochrome2binary(self, image, threshold=128):
        if not isinstance(image, ImageMonochrome):
            raise TypeError("[IMAGE_CONVERTOR ERROR]: Input image != type ImageMonochrome (reason: monochrome2binary() ).")
        if not (0 <= threshold <= 255):
            raise ValueError("[IMAGE_CONVERTOR ERROR]: Threshold for binary conversion must be between 0 and 255 (reason: monochrome2binary() ).")
        result = ImageBinary(image.get_width(), image.get_height(), [0] * image.get_size())
        result.set_data([255 if pixel > threshold else 0 for pixel in image.get_data()])
        return result

    def binary2monochrome(self, image):
        if not isinstance(image, ImageBinary):
            raise TypeError("[IMAGE_CONVERTOR ERROR]: Input image != type ImageBinary (reason: binary2monochrome() ).")

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
        if not isinstance(image, ImageColor):
            raise TypeError("[IMAGE_CONVERTOR ERROR]: Input image != type ImageColor (reason: color2binary() ).")
        if not (0 <= threshold <= 255):
            raise ValueError("[IMAGE_CONVERTOR ERROR]: Threshold for binary conversion must be between 0 and 255 (reason: color2binary() ).")
        monochrome_image = self.color2monochrome(image)
        return self.monochrome2binary(monochrome_image, threshold)

    def binary2color(self, image, palette):
        if not isinstance(image, ImageBinary):
            raise TypeError("[IMAGE_CONVERTOR ERROR]: Input image != type ImageBinary (reason: binary2color() ).")
        if not isinstance(palette, list) or len(palette) != 256:
            raise ValueError("[IMAGE_CONVERTOR ERROR]: Palette must be a list of 256 colors for monochrome to color conversion (reason: binary2color() ).")
        
        
        monochrome_image = self.binary2monochrome(image)
        return self.monochrome2color(monochrome_image, palette)

    def __del__(self):
        pass