from Hist import HistCSV

class HistEncoder:
    def __init__(self, strategy):
        self.strategy = strategy

    def set_strategy(self, strategy):
        self.strategy = strategy

    def encode(self, file_path, histogram):
        self.strategy.write(file_path, histogram)

    def decode(self, file_path):
        return self.strategy.read(file_path)

if __name__ == "__main__":
    histogram = {0: 10, 1: 15, 2: 5, 3: 20}
    encoder = HistEncoder(HistCSV())
    encoder.encode("/home/wilkaone/Projects/mipt-python/hometask8/encoders/test.csv", histogram)
    histogram_decoded = encoder.decode("/home/wilkaone/Projects/mipt-python/hometask8/encoders/test.csv")
    print(histogram_decoded)