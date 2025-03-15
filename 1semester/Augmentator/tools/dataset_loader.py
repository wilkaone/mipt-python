import os
import re

class DatasetLoader:
    def __init__(self, dataset_path):
        self.dataset_path = dataset_path
        self.data = {}

    def load_data(self):
        for class_dir in sorted(os.listdir(self.dataset_path)):
            class_path = os.path.join(self.dataset_path, class_dir)
            if os.path.isdir(class_path):
                images = sorted(
                    [os.path.join(class_path, img) for img in os.listdir(class_path) if img.lower().endswith(('.png', '.jpg', '.jpeg'))],
                    key=lambda x: int(re.search(r'(\d+)', os.path.basename(x)).group(0)) 
                )
                self.data[class_dir] = images
        return self.data