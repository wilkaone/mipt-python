# blood_cell_mse_function.py
import cv2
import numpy as np
import random
from image_generator import ImageGenerator

class BloodCellMSEFunction:
    def __init__(self, reference_img: np.ndarray, dataset_loader, num_cells_expected=1, img_size=(480, 640),
                 margin: float = 20, alpha_penalty: float = 0.1, seed=None):
        # Приводим эталонное изображение к типу float32
        self.reference_img = reference_img.astype(np.float32)
        self.img_h, self.img_w = self.reference_img.shape[:2] # Размеры примера (h, w)
        self.dataset_loader = dataset_loader
        self.img_size = img_size
        self.num_cells_expected = num_cells_expected # Ожидаемое число клеток для генерации
        self.margin = margin # Минимальный отступ от краёв
        self.alpha_penalty = alpha_penalty # Коэффициент штрафа за нарушение отступа
        
        # Создаем генератор изображений с указанными параметрами
        self.generator = ImageGenerator(
            dataset_loader=self.dataset_loader,
            img_size=self.img_size,
            num_imgs=1,
            num_cells=num_cells_expected,
            seed=seed
        )
        
        if seed is not None:
            random.seed(seed)
            np.random.seed(seed)

    def __call__(self, x: np.ndarray) -> float:
        # Генерируем изображение по параметрам x
        gen_img = self.generate_image_with_params(x)

        # Если изображение цветное, переводим его в grayscale
        if gen_img.ndim == 3 and gen_img.shape[2] == 3:
            gen_img = cv2.cvtColor(gen_img, cv2.COLOR_BGR2GRAY)

        gen_img = gen_img.astype(np.float32)
        # Если размеры не совпадают с эталоном, изменяем их
        if (gen_img.shape[0] != self.img_h) or (gen_img.shape[1] != self.img_w):
            gen_img = cv2.resize(gen_img, (self.img_w, self.img_h))
        # Вычисляем MSE между примером и сгенерированным изображением
        mse_val = np.mean((self.reference_img - gen_img)**2)
        
        # Переформатируем вектор параметров в матрицу (num_cells_expected, 3)
        try:
            cells = x.reshape(self.num_cells_expected, 3)
        except ValueError:
            raise ValueError("Длина x должна быть кратна 3 (каждый объект задаётся как (cx, cy, r)).")
        
        # Извлекаем координаты клеток
        cx = cells[:, 0]
        cy = cells[:, 1]
        # Вычисляем штрафы, если клетка слишком близко к краям
        left_penalty   = np.where(cx < self.margin, (self.margin - cx)**2, 0)
        right_penalty  = np.where(cx > (self.img_size[1] - self.margin), (cx - (self.img_size[1] - self.margin))**2, 0)
        top_penalty    = np.where(cy < self.margin, (self.margin - cy)**2, 0)
        bottom_penalty = np.where(cy > (self.img_size[0] - self.margin), (cy - (self.img_size[0] - self.margin))**2, 0)
        penalty = np.sum(left_penalty + right_penalty + top_penalty + bottom_penalty)
        # Итоговая стоимость: MSE плюс штраф
        total_cost = mse_val + self.alpha_penalty * penalty
        return total_cost

    def generate_image_with_params(self, x: np.ndarray) -> np.ndarray:
        # Проверяем, что длина x кратна 3 и соответствует ожидаемому числу клеток
        if len(x) % 3 != 0:
            raise ValueError("Длина x должна быть кратна 3 (каждый объект задаётся как (cx, cy, r)).")
        num_cells = len(x) // 3
        if num_cells != self.num_cells_expected:
            raise ValueError(f"Ожидается {self.num_cells_expected} объектов, получено {num_cells}.")

        # Загружаем фон (ресайз до img_size)
        background = self.generator._load_image(self.dataset_loader.get_random_background(), resize=True)

        # Для каждой клетки накладываем её на фон по заданным параметрам
        for i in range(num_cells):
            cx = x[3 * i]
            cy = x[3 * i + 1]
            r  = x[3 * i + 2]
            # Ограничиваем параметры, чтобы не выйти за границы
            cx = int(np.clip(cx, 0, self.img_size[1] - 1))
            cy = int(np.clip(cy, 0, self.img_size[0] - 1))
            r  = int(np.clip(r, 5, 100))
            
            # Загружаем изображение клетки и масштабируем до нужного размера
            cell = self.generator._load_image(self.dataset_loader.get_random_cell(), resize=False, with_alpha=True)
            cell = cv2.resize(cell, (r, r))
            
            # Формируем словарь координат для наложения
            coord = {"h": cy, "w": cx}
            transparency = random.uniform(0.6, 1.0)
            # Накладываем клетку на фон
            background = self.generator._overlay(background, cell, coord, transparency)
        
        return background
