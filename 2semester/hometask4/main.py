import cv2
import numpy as np
import os
import shutil

from dataset_loader import DatasetLoader
from blood_cell_mse_function import BloodCellMSEFunction
from optim.monte_carlo_grad import MonteCarloGradientOptimizer
from optim.peano_optimizer import PeanoGlobalOptimizer
from optim.grid_search import GridSearchOptimizer
from optimization_manager import OptimizationManager

def clear_folder(folder_path):
    # Удаляет папку и её содержимое, затем создаёт её заново.
    if os.path.exists(folder_path):
        shutil.rmtree(folder_path)
    os.makedirs(folder_path)

def main():
    # Очистка папки для сохранения сгенерированных изображений
    clear_folder("/home/wilkaone/Projects/mipt-python_backup/2semester/hometask4/Gen")

    # Загрузка изображения (пример) и перевод его в grayscale
    reference_path = "/home/wilkaone/Projects/mipt-python_backup/2semester/hometask4/example.png"
    reference_img = cv2.imread(reference_path, cv2.IMREAD_COLOR)
    if reference_img is None:
        raise ValueError(f"Cannot load reference image: {reference_path}")
    reference_img = cv2.cvtColor(reference_img, cv2.COLOR_BGR2GRAY)

    # Указываем путь к датасету с изображениями клеток и фонов
    dataset_path = "/home/wilkaone/Projects/mipt-python_backup/2semester/hometask4/MyDataset/"
    dataset_loader = DatasetLoader(dataset_path)

     # Определяем, сколько клеток ожидается в генерируемом изображении
    num_cells_expected = 3
    # Создаем функцию оценки (MSE с штрафами) для оптимизации
    func = BloodCellMSEFunction(
        reference_img=reference_img,
        dataset_loader=dataset_loader,
        num_cells_expected=num_cells_expected,
        img_size=(480, 640),
        seed=42
    )

    # Для каждой клетки задаем границы: cx = [0,640], cy = [0,480], r = [5,100]
    bounds = [(0, 640), (0, 480), (5, 100)] * num_cells_expected

    # Запуск оптимизации методом Monte Carlo + градиентного спуска
    optimizer_mc = MonteCarloGradientOptimizer(
        func=func,
        bounds=bounds,
        max_iterations=40,
        mc_points=20,
        alpha=0.1
    )
    manager_mc = OptimizationManager(optimizer_mc, 
                                     log_file="/home/wilkaone/Projects/mipt-python_backup/2semester/hometask4/results_montecarlo.log", 
                                     gen_folder="/home/wilkaone/Projects/mipt-python_backup/2semester/hometask4/Gen")
    best_x_mc, best_f_mc = manager_mc.run()
    print(f"[MonteCarlo+Grad] Best: x={best_x_mc}, f={best_f_mc}")

    # Запуск оптимизации методом развёртки Пеано + глобальной оптимизации
    optimizer_peano = PeanoGlobalOptimizer(
        func=func,
        bounds=bounds,
        max_iterations=40
    )
    manager_peano = OptimizationManager(optimizer_peano, 
                                        log_file="/home/wilkaone/Projects/mipt-python_backup/2semester/hometask4/results_peano.log", 
                                        gen_folder="/home/wilkaone/Projects/mipt-python_backup/2semester/hometask4/Gen")
    best_x_peano, best_f_peano = manager_peano.run()
    print(f"[PeanoGlobal] Best: x={best_x_peano}, f={best_f_peano}")

    # Запуск оптимизации методом перебора по сетке (Grid Search)
    optimizer_grid = GridSearchOptimizer(
        func=func,
        bounds=bounds,
        max_iterations=2000,
        steps_per_dim=5
    )
    manager_grid = OptimizationManager(optimizer_grid, 
                                       log_file="/home/wilkaone/Projects/mipt-python_backup/2semester/hometask4/results_grid.log", 
                                       gen_folder="/home/wilkaone/Projects/mipt-python_backup/2semester/hometask4/Gen")
    best_x_grid, best_f_grid = manager_grid.run()
    print(f"[GridSearch] Best: x={best_x_grid}, f={best_f_grid}")

if __name__ == "__main__":
    main()
