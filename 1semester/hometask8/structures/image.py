import cv2

"""
Абстрактная фабрика 
"""

class AbstractFactoryImageReader():
    def read_image(self, file_path):
        raise NotImplementedError()

class BinImageReader(AbstractFactoryImageReader):
    def read_image(self, file_path):
        image = cv2.imread(file_path, cv2.IMREAD_GRAYSCALE)
        if image is None or image.size == 0:
            raise ValueError(f"Could not read image from {file_path}")
        _, bin_image = cv2.threshold(image, 127, 255, cv2.THRESH_BINARY)
        return bin_image

class MonochromeImageReader(AbstractFactoryImageReader):
    def read_image(self, file_path):
        image = cv2.imread(file_path, cv2.IMREAD_GRAYSCALE)
        if image is None or image.size == 0:
            raise ValueError(f"Could not read image from {file_path}")
        return image

class ColorImageReader(AbstractFactoryImageReader):
    def read_image(self, file_path):
        image = cv2.imread(file_path, cv2.IMREAD_COLOR)
        if image is None or image.size == 0:
            raise ValueError(f"Could not read image from {file_path}")
        return image

def get_image_reader(ident):
    if ident == 0:
        return BinImageReader()
    elif ident == 1:
        return MonochromeImageReader()
    elif ident == 2:
        return ColorImageReader()

if __name__ == "__main__":
    try:
        # нужно изменить путь для теста (!!!)
        file_path = "/home/wilkaone/Projects/mipt-python/hometask8/structures/test.jpg"
        for i in range(3):
            reader = get_image_reader(i)
            print(f"Using {reader.__class__.__name__}")
            try:
                image = reader.read_image(file_path)
                print(f"Successfully read image with {reader.__class__.__name__}")
            except ValueError as ve:
                print(ve)
    except Exception as e:
        print(f"Error: {e}")