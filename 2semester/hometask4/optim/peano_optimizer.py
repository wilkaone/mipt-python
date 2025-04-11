# optim/peano_optimizer.py
import numpy as np
from .base_optimizer import Optimizer

class PeanoGlobalOptimizer(Optimizer):
    def __init__(self, func, bounds, max_iterations=100, refine=False):
        super().__init__(func, bounds, max_iterations)
        self.refine = refine # Флаг для последующего уточнения решения

    def peano_map(self, t):
        # Преобразует t = [0,1] в точку n-мерного пространства по линейному правилу
        return np.array([bmin + t * (bmax - bmin) for (bmin, bmax) in self.bounds])

    def optimize(self):
        n_points = self.max_iterations
        # Ищем лучшее значение по равномерной разбивке t = [0,1]
        for i in range(n_points):
            t = i / (n_points - 1) if n_points > 1 else 0.5
            x = self.peano_map(t)
            f_val = self.func(x)
            if f_val < self.best_f:
                self.best_f = f_val
                self.best_x = x.copy()
        
        # Если включено уточнение, запускаем локальное уточнение найденного решения
        if self.refine and self.best_x is not None:
            x_refined = self.best_x.copy()
            for _ in range(10):
                # Вычисляем численный градиент
                grad = np.zeros(self.dim)
                epsilon = 1e-5
                for d in range(self.dim):
                    x_up = x_refined.copy()
                    x_down = x_refined.copy()
                    x_up[d] += epsilon
                    x_down[d] -= epsilon
                    f_up = self.func(x_up)
                    f_down = self.func(x_down)
                    grad[d] = (f_up - f_down) / (2 * epsilon)
                # Корректируем решение маленьким шагом по направлению отрицательного градиента
                x_refined -= 0.01 * grad 
                # Ограничиваем значения в пределах заданных границ
                for d in range(self.dim):
                    bmin, bmax = self.bounds[d]
                    x_refined[d] = np.clip(x_refined[d], bmin, bmax)
                f_val = self.func(x_refined)
                if f_val < self.best_f:
                    self.best_f = f_val
                    self.best_x = x_refined.copy()
        
        return self.best_x, self.best_f
