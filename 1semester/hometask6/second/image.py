class Image:
    def __init__(self, width, height):
        self.__width = width
        self.__height = height
        self.__size = width * height
        self.__data_pixels = list()

    def get_width(self):
        return self.__width
    
    def set_width(self, width):
        self.__width = width
        self.__size = self.__width * self.__height 
    
    def get_height(self):
        return self.__height
    
    def set_height(self, height):
        self.__height = height
        self.__size = self.__width * self.__height 
    
    def get_size(self):
        return self.__size
    
    def get_data(self):
        return self.__data_pixels
    
    def set_data(self, data):
        self.__data_pixels = data

    def show(self):
        pass
    def __del__(self):
        pass

class ImageBinary(Image):
    def __init__(self, width, height, data):
        super().__init__(width, height)
        self.set_data(data)
    def show(self):
        for i in range(self.get_height()):
            print(' '.join(str(self.get_data()[i * self.get_width() + j]) for j in range(self.get_width())))
    def __del__(self):
        pass

class ImageMonochrome(Image):
    def __init__(self, width, height, data):
        super().__init__(width, height)
        self.set_data(data)
    def show(self):
        for i in range(self.get_height()):
            print(' '.join(str(self.get_data()[i * self.get_width() + j]) for j in range(self.get_width())))
    def __del__(self):
        pass

class ImageColor(Image):
    def __init__(self, width, height, data):
        super().__init__(width, height)
        self.set_data(data)
    def show(self):
        for i in range(self.get_height()):
            row = []
            for j in range(self.get_width()):
                red, green, blue = self.get_data()[i * self.get_width() + j]
                row.append(f"[{red},{green},{blue}]")
            print(' '.join(row))
    def __del__(self):
        pass
    
