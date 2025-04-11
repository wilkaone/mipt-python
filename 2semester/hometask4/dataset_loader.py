import os
import random

class DatasetLoader:
    def __init__(self, dataset_dir):
        self.dataset_dir = dataset_dir
        self.patterns = {"Backgrounds": [], "BloodCells": []}
        self._load_patterns()

    def _load_patterns(self):
        for category in self.patterns.keys():
            cat_path = os.path.join(self.dataset_dir, category)
            if not os.path.exists(cat_path):
                raise ValueError(f"Категория {category} не найдена по пути {cat_path}")
            files = [f for f in os.listdir(cat_path) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
            if not files:
                raise ValueError(f"Ошибка: в категории {category} не найдено ни одного изображения")
            self.patterns[category] = sorted([os.path.join(cat_path, f) for f in files])
        
        if not self.patterns["Backgrounds"] or not self.patterns["BloodCells"]:
            raise ValueError("Error: Backgrounds or BloodCells not found")

    def get_random_background(self):
        return random.choice(self.patterns["Backgrounds"])

    def get_random_cell(self):
        return random.choice(self.patterns["BloodCells"])