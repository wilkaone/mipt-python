# optim/grid_search.py
import numpy as np
import itertools
from .base_optimizer import Optimizer

class GridSearchOptimizer(Optimizer):
    def __init__(self, func, bounds, max_iterations=100, steps_per_dim=5, refine=False):
        super().__init__(func, bounds, max_iterations)
        self.steps_per_dim = steps_per_dim
        self.refine = refine

    def optimize(self):
        axes = [np.linspace(bmin, bmax, self.steps_per_dim) for (bmin, bmax) in self.bounds]
        all_points = itertools.product(*axes)
        limited_points = itertools.islice(all_points, self.max_iterations)
        
        for point in limited_points:
            x = np.array(point, dtype=float)
            f_val = self.func(x)
            if f_val < self.best_f:
                self.best_f = f_val
                self.best_x = x.copy()
        
        if self.refine and self.best_x is not None:
            new_bounds = []
            for d, (bmin, bmax) in enumerate(self.bounds):
                delta = (bmax - bmin) * 0.1 
                new_min = max(bmin, self.best_x[d] - delta)
                new_max = min(bmax, self.best_x[d] + delta)
                new_bounds.append((new_min, new_max))
            axes = [np.linspace(bmin, bmax, self.steps_per_dim) for (bmin, bmax) in new_bounds]
            for point in itertools.product(*axes):
                x = np.array(point, dtype=float)
                f_val = self.func(x)
                if f_val < self.best_f:
                    self.best_f = f_val
                    self.best_x = x.copy()
        
        return self.best_x, self.best_f
