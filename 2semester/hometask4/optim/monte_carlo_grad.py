import random
import numpy as np
from .base_optimizer import Optimizer

class MonteCarloGradientOptimizer(Optimizer):
    def __init__(self, func, bounds, max_iterations=100, mc_points=30, alpha=0.05, momentum=0.9, tol=1e-6):
        super().__init__(func, bounds, max_iterations)
        self.mc_points = mc_points # Количество случайных точек для начального поиска
        self.alpha = alpha # Начальный шаг градиентного спуска
        self.momentum = momentum # Коэффициент инерции (momentum)
        self.tol = tol # Порог улучшения для адаптивного уменьшения шага

    def numerical_gradient(self, x, epsilon=1e-5):
        # Вычисляет численный градиент функции в точке x методом центральных разностей
        grad = np.zeros(self.dim)
        for i in range(self.dim):
            x_up = x.copy()
            x_down = x.copy()
            x_up[i] += epsilon
            x_down[i] -= epsilon
            f_up = self.func(x_up)
            f_down = self.func(x_down)
            grad[i] = (f_up - f_down) / (2 * epsilon)
        return grad

    def random_point(self):
        # Генерирует случайную точку в пространстве допустимых значений (bounds)
        return np.array([random.uniform(bmin, bmax) for (bmin, bmax) in self.bounds])

    def optimize(self):
        # Поиск лучшей точки методом случайного поиска (Monte Carlo)
        best_x = None
        best_f = float('inf')
        for _ in range(self.mc_points):
            x_rand = self.random_point()
            f_val = self.func(x_rand)
            if f_val < best_f:
                best_f = f_val
                best_x = x_rand

        self.best_x = best_x
        self.best_f = best_f

        # Уточнение решения методом градиентного спуска с momentum
        x_current = best_x.copy()
        v = np.zeros_like(x_current) # Инициализация вектора скорости (momentum)
        current_alpha = self.alpha # Текущий шаг

        for iteration in range(self.max_iterations):
            grad = self.numerical_gradient(x_current) # Вычисление градиента в текущей точке
            # Обновление скорости с учетом инерции и шага спуска
            v = self.momentum * v - current_alpha * grad
            x_next = x_current + v # Обновление точки

            # Ограничиваем новую точку в пределах разрешённых диапазонов
            for d in range(self.dim):
                bmin, bmax = self.bounds[d]
                x_next[d] = np.clip(x_next[d], bmin, bmax)

            f_next = self.func(x_next) # Значение функции в новой точке
            improvement = abs(self.best_f - f_next) # Разница по функции между лучшим и новой точкой
            # Если найдено улучшение, обновляем лучшее решение
            if f_next < self.best_f:
                self.best_f = f_next
                self.best_x = x_next.copy()
            # Если улучшение оказалось слишком малым, уменьшаем шаг и проверяем условие останова
            if improvement < self.tol:
                current_alpha *= 0.5
                if current_alpha < 1e-8:
                    break
            x_current = x_next # Переходим к следующей итерации

        return self.best_x, self.best_f