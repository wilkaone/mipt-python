class Image:
    def __init__(self, width, height):
        if width <= 0 or height <= 0:
            raise ValueError("[IMAGE ERROR]: Width and/or Height <= 0 (reason: constructor)")

        self._width = width
        self._height = height
        self._size = width * height
        self._data_pixels = list()

    def get_width(self):
        return self._width
    
    def set_width(self, width):
        if width <= 0:
            raise ValueError("[IMAGE ERROR]: Width <= 0 (reason: set_width() )")
        self._width = width
        self._size = self._width * self._height 
    
    def get_height(self):
        return self._height
    
    def set_height(self, height):
        if height <= 0:
            raise ValueError("[IMAGE ERROR]: Height <= 0 (reason: set_height() )")
        self._height = height
        self._size = self._width * self._height 
    
    def get_size(self):
        return self._size
    
    def get_data(self):
        return self._data_pixels

    def show(self):
        pass
    def __del__(self):
        pass

class ImageBinary(Image):
    def __init__(self, width, height, data):
        super().__init__(width, height)
        self.set_data(data)

    def set_data(self, data):
        if len(data) != self.get_height() * self.get_width():
            raise ValueError("[IMAGE ERROR]: Data != Size (reason: set_data() )")
        self._data_pixels = data
    
    def show(self):
        for i in range(self.get_height()):
            print(' '.join(str(self.get_data()[i * self.get_width() + j]) for j in range(self.get_width())))
    def __del__(self):
        pass

class ImageMonochrome(Image):
    def __init__(self, width, height, data):
        super().__init__(width, height)
        self.set_data(data)

    def set_data(self, data):
        if len(data) != self.get_height() * self.get_width():
            raise ValueError("[IMAGE ERROR]: Data != Size (reason: set_data() )")
        self._data_pixels = data

    def show(self):
        for i in range(self.get_height()):
            print(' '.join(str(self.get_data()[i * self.get_width() + j]) for j in range(self.get_width())))

    def __del__(self):
        pass

class ImageColor(Image):
    def __init__(self, width, height, data):
        super().__init__(width, height)
        self.set_data(data)
    
    def set_data(self, data):
        if len(data) != self.get_height() * self.get_width():
            raise ValueError("[IMAGE ERROR]: Data != Size (reason: set_data())")

        for pixel in data:
            if isinstance(pixel, list) and len(pixel) == 3:
                pass
            else:
                raise ValueError("[IMAGE ERROR]: Each pixel in color image should be a list of three values (RGB) (reason: set_data())")

        self._data_pixels = data

    def show(self):
        for i in range(self.get_height()):
            row = []
            for j in range(self.get_width()):
                red, green, blue = self.get_data()[i * self.get_width() + j]
                row.append(f"[{red},{green},{blue}]")
            print(' '.join(row))
    def __del__(self):
        pass
    
