import csv

class HistStrategy:
    def write(self, file_path, histogram):
        raise NotImplementedError()

    def read(self, file_path):
        raise NotImplementedError()
    
class HistCSV(HistStrategy):
    def write(self, file_path, histogram):
        with open(file_path, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["bin", "count"])
            for bin_value, count in histogram.items():
                writer.writerow([bin_value, count])
        print(f"Histogram write to {file_path} (CSV)")

    def read(self, file_path):
        histogram = {}
        with open(file_path, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                histogram[int(row["bin"])] = int(row["count"])
        print(f"Histogram read from {file_path} (CSV)")
        return histogram
