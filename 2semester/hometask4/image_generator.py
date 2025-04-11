import os
import cv2
import random
import numpy as np

from dataset_loader import DatasetLoader

class ImageGenerator:
    def __init__(self, dataset_loader, img_size=(480, 640), num_imgs=5, num_cells=25, seed=None):
        self.dataset_loader = dataset_loader
        self.img_size = img_size
        self.num_cells = num_cells
        self.num_imgs = num_imgs

        if seed is not None:
            random.seed(seed)
            np.random.seed(seed)

    def generate_and_save(self, save_dir):
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)

        for idx in range(self.num_imgs):
            img = self._generate_image()
            cv2.imwrite(os.path.join(save_dir, f"result_{idx}.png"), img)

    def _generate_image(self):
        coords = self._generate_cell_coords()

        background = self._load_image(self.dataset_loader.get_random_background(), resize=True)

        for i in range(self.num_cells):
            cell = self._load_image(self.dataset_loader.get_random_cell(), resize=True, with_alpha=True)

            transparency = random.uniform(0.6, 1.0)

            background = self._overlay(background, cell, coords[i], transparency)

        return background

    def _generate_cell_coords(self):
        return [{"h": random.randint(0, self.img_size[0] - int(self.img_size[0] * 0.01)),
                 "w": random.randint(0, self.img_size[1] - int(self.img_size[1] * 0.01))}
                for _ in range(self.num_cells)]

    def _load_image(self, image_path, resize=False, with_alpha=False):
        flags = cv2.IMREAD_UNCHANGED if with_alpha else cv2.IMREAD_COLOR
        image = cv2.imread(image_path, flags)
        
        if image is None:
            raise ValueError(f"Error: Failed to load image {image_path}")

        if resize:
            image = cv2.resize(image, (self.img_size[1], self.img_size[0]))

        return image

    def _overlay(self, background, cell, coord, transparency=1.0):
        scale = round(random.uniform(0.05, 0.20), 2)
        cell_size = int(min(self.img_size) * scale)
        cell = cv2.resize(cell, (cell_size, cell_size))

        cell, cell_h, cell_w = self._rotate_cell(cell, cell_size, cell_size)

        if coord["h"] + cell_h > background.shape[0]:
            cell_h = background.shape[0] - coord["h"]
        if coord["w"] + cell_w > background.shape[1]:
            cell_w = background.shape[1] - coord["w"]

        cell = cell[:cell_h, :cell_w]

        if cell.shape[-1] == 4:
            alpha = (cell[:, :, 3] / 255.0) * transparency
            for c in range(3):
                background[coord["h"]:coord["h"] + cell_h, coord["w"]:coord["w"] + cell_w, c] = (
                    (1 - alpha) * background[coord["h"]:coord["h"] + cell_h, coord["w"]:coord["w"] + cell_w, c] +
                    alpha * cell[:, :, c]
                )

        return background

    def _rotate_cell(self, cell, cell_h, cell_w):
        center = (cell_w // 2, cell_h // 2)
        angle = random.randint(0, 360)
        matrix = cv2.getRotationMatrix2D(center, angle, 1.0)

        new_w = int((cell_h * abs(matrix[0, 1])) + (cell_w * abs(matrix[0, 0])))
        new_h = int((cell_h * abs(matrix[0, 0])) + (cell_w * abs(matrix[0, 1])))

        matrix[0, 2] += (new_w / 2) - center[0]
        matrix[1, 2] += (new_h / 2) - center[1]

        rotated = cv2.warpAffine(cell, matrix, (new_w, new_h))

        return rotated, new_h, new_w

# dataset_path = "/home/ilyakositsyn/projects/PyScripts/hometask4/MyDataset"
# save_path = "/home/ilyakositsyn/projects/PyScripts/hometask4/Gen"

# dataset_loader = DatasetLoader(dataset_path)

# generator = ImageGenerator(dataset_loader, num_imgs=25, num_cells=3, seed=42)
# generator.generate_and_save(save_path)
