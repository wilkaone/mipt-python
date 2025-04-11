from abc import ABC, abstractmethod

class Optimizer(ABC):
    def __init__(self, func, bounds, max_iterations=100):
        self.func = func # функция-объект
        self.bounds = bounds # допустимые диапазоны для каждой переменной
        self.dim = len(bounds) # размерность оптимизационного пространства
        self.max_iterations = max_iterations # максимальное число итераций
        self.best_x = None # Лучший найденный вектор параметров
        self.best_f = float('inf') # Лучшее (минимальное) значение функции

    @abstractmethod
    def optimize(self):
        # запускает оптимизатор и возвращает (best_x, best_f)
        pass
