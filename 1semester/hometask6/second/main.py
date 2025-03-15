from image import ImageBinary
from image import ImageMonochrome
from image import ImageColor

from image_convertor import ImageConvertor

if __name__ == "__main__":

    convertor = ImageConvertor()

    binary_data = [0, 255, 0, 255, 255, 0, 0, 255, 0]
    monochrome_data = [50, 100, 150, 200, 50, 100, 150, 200, 50]
    color_data = [[100, 150, 200], [200, 100, 50], [50, 50, 50],
                  [255, 255, 255], [0, 0, 0],      [128, 128, 128],
                  [100, 50, 150],  [50, 150, 200], [200, 100, 50]]
    
    palette = {i: [i, 255 - i, i // 2] for i in range(256)}

    binary_image = ImageBinary(3, 3, binary_data)
    monochrome_image = ImageMonochrome(3, 3, monochrome_data)
    color_image = ImageColor(3, 3, color_data)

    print("\nOriginal Binary Image:")
    binary_image.show()

    print("\nOriginal Monochrome Image:")
    monochrome_image.show()

    print("\nOriginal Color Image:")
    color_image.show()

    print("\nMonochrome to Monochrome:")
    monochrome2monochrome_image = convertor.monochrome2monochrome(monochrome_image)
    monochrome2monochrome_image.show()

    print("\nColor to Monochrome:")
    color2monochrome_image = convertor.color2monochrome(color_image)
    color2monochrome_image.show()

    print("\nMonochrome to Color:")
    monochrome2color_image = convertor.monochrome2color(monochrome_image, palette)
    monochrome2color_image.show()

    print("\nMonochrome to Binary:")
    monochrome2binary_image = convertor.monochrome2binary(monochrome_image, threshold=100)
    monochrome2binary_image.show()

    print("\nBinary to Monochrome:")
    binary2monochrome_image = convertor.binary2monochrome(binary_image)
    binary2monochrome_image.show()

    print("\nColor to Binary:")
    color2binary_image = convertor.color2binary(color_image, threshold=128)
    color2binary_image.show()

    print("\nBinary to Color:")
    binary2color_image = convertor.binary2color(binary_image, palette)
    binary2color_image.show()