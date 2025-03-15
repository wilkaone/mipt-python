import os
import random

class DatasetLoader:
    def __init__(self, dataset_dir):
        self.dataset_dir = dataset_dir
        self.patterns = {"Backgrounds": [], "BloodCells": []}
        self._load_patterns()

    def _load_patterns(self):
        for root, _, files in os.walk(self.dataset_dir):
            category = os.path.basename(root)
            if category in self.patterns:
                self.patterns[category] = sorted([os.path.join(root, f) for f in files])

        if not self.patterns["Backgrounds"] or not self.patterns["BloodCells"]:
            raise ValueError("Error: Backgrounds or BloodCells not found")

    def get_random_background(self):
        return random.choice(self.patterns["Backgrounds"])

    def get_random_cell(self):
        return random.choice(self.patterns["BloodCells"])