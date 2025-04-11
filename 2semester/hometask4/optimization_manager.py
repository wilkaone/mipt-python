import os
import cv2
import shutil

def clear_folder(folder_path):
    # Удаляет папку и её содержимое, затем создаёт папку заново.
    if os.path.exists(folder_path):
        shutil.rmtree(folder_path)
    os.makedirs(folder_path)

class OptimizationManager:
    def __init__(self, optimizer, log_file="results.log", gen_folder="gen"):
        self.optimizer = optimizer # Оптимизатор
        self.log_file = log_file # Файл для записи результатов
        self.history = [] # История найденных решений
        self.gen_folder = gen_folder # Папка для сохранения сгенерированных изображений

    def run(self):
        best_x, best_f = self.optimizer.optimize() # Запускаем оптимизацию
        self.history.append((best_x, best_f))
        self._save_log(best_x, best_f)
        
        # Генерируем изображение по найденным параметрам и сохраняем его
        best_img = self.optimizer.func.generate_image_with_params(best_x)
        
        method_name = self.optimizer.__class__.__name__
        best_img_path = os.path.join(self.gen_folder, f"best_generated_{method_name}.png")
        cv2.imwrite(best_img_path, best_img)
        print(f"Best generated image saved to: {best_img_path}")
        
        return best_x, best_f

    def _save_log(self, x, f):
        # Записываем решение и значение функции в лог-файл
        line = f"Best solution: x={x}, f={f}\n"
        with open(self.log_file, "a") as fout:
            fout.write(line)