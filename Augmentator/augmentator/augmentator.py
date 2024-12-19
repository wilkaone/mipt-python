import cv2
import numpy as np

class Augmentator:
    def __init__(self, image: np.ndarray):
        if image is None:
            raise ValueError("Исходное изображение не должно быть None")
        self.original_image = image
        self.processed_image = image.copy()

    def apply(self, augmentation):
        self.processed_image = augmentation.apply(self.processed_image)

    def reset(self):
        self.processed_image = self.original_image.copy()

    def get_image(self):
        return self.processed_image

class Augmentation:
    def apply(self, image: np.ndarray) -> np.ndarray:
        raise NotImplementedError("Метод apply() должен быть реализован в подклассах")

class AddAdaptiveNoise(Augmentation):
    def __init__(self, noise_percentage: float = 0.05):
        if not (0.0 < noise_percentage <= 1.0):
            raise ValueError("Доля шума должна быть в пределах (0.0, 1.0]")
        self.noise_percentage = noise_percentage

    def apply(self, image: np.ndarray) -> np.ndarray:
        if len(image.shape) != 2:
            raise ValueError("Изображение должно быть в оттенках серого")

        noisy_image = image.copy()
        num_pixels = int(self.noise_percentage * image.size)

        coords = np.random.choice(image.size, num_pixels, replace=False)
        flat_image = noisy_image.ravel()

        noise_values = np.random.randint(0, 256, num_pixels, dtype=np.uint8)

        flat_image[coords] = noise_values
        return noisy_image.reshape(image.shape)

class RemoveNoise(Augmentation):
    def __init__(self, method: str = "gaussian", kernel_size: int = 5):
        if method not in ["gaussian", "average"]:
            raise ValueError("Метод должен быть 'gaussian' или 'average'")
        if kernel_size <= 0 or kernel_size % 2 == 0:
            raise ValueError("Размер ядра должен быть положительным нечетным числом")
        self.method = method
        self.kernel_size = kernel_size

    def apply(self, image: np.ndarray) -> np.ndarray:
        if len(image.shape) != 2:
            raise ValueError("Изображение должно быть в оттенках серого")

        if self.method == "gaussian":
            return cv2.GaussianBlur(image, (self.kernel_size, self.kernel_size), 0)
        elif self.method == "average":
            return cv2.blur(image, (self.kernel_size, self.kernel_size))

class HistogramEqualization(Augmentation):
    def apply(self, image: np.ndarray) -> np.ndarray:
        if len(image.shape) != 2:
            raise ValueError("Изображение должно быть в оттенках серого")

        return cv2.equalizeHist(image)

class StaticColorCorrection(Augmentation):
    def __init__(self, alpha: float = 1.0, beta: int = 0):
        self.alpha = alpha
        self.beta = beta

    def apply(self, image: np.ndarray) -> np.ndarray:
        return cv2.convertScaleAbs(image, alpha=self.alpha, beta=self.beta)

class Translate(Augmentation):
    def __init__(self, tx: int = 0, ty: int = 0):
        self.tx = tx
        self.ty = ty

    def apply(self, image: np.ndarray) -> np.ndarray:
        rows, cols = image.shape[:2]
        M_translate = np.float32([[1, 0, self.tx], [0, 1, self.ty]])
        return cv2.warpAffine(image, M_translate, (cols, rows))

class Rotate(Augmentation):
    def __init__(self, angle: float = 0.0, center: tuple = None):
        self.angle = angle
        self.center = center

    def apply(self, image: np.ndarray) -> np.ndarray:
        rows, cols = image.shape[:2]
        if self.center is None:
            self.center = (cols // 2, rows // 2)
        M_rotate = cv2.getRotationMatrix2D(self.center, self.angle, 1.0)
        return cv2.warpAffine(image, M_rotate, (cols, rows))

class Scale(Augmentation):
    def __init__(self, fx: float = 1.0, fy: float = 1.0):
        self.fx = fx
        self.fy = fy

    def apply(self, image: np.ndarray) -> np.ndarray:
        return cv2.resize(image, None, fx=self.fx, fy=self.fy, interpolation=cv2.INTER_LINEAR)

class GlassEffect(Augmentation):
    def apply(self, image: np.ndarray) -> np.ndarray:
        rows, cols = image.shape[:2]
        glass_image = image.copy()
        for i in range(rows):
            for j in range(cols):
                x = i + int((np.random.rand() - 0.5) * 10)
                y = j + int((np.random.rand() - 0.5) * 10)
                if 0 <= x < rows and 0 <= y < cols:
                    glass_image[i, j] = image[x, y]
        return glass_image

class MotionBlur(Augmentation):
    def __init__(self, kernel_size: int = 5):
        self.kernel_size = kernel_size

    def apply(self, image: np.ndarray) -> np.ndarray:
        kernel = np.zeros((self.kernel_size, self.kernel_size))
        kernel[int((self.kernel_size - 1)/2), :] = np.ones(self.kernel_size)
        kernel /= self.kernel_size
        return cv2.filter2D(image, -1, kernel)

class Wave1(Augmentation):
    def apply(self, image: np.ndarray) -> np.ndarray:
        rows, cols = image.shape[:2]
        wave_image = np.zeros_like(image)
        for l in range(cols):
            k_shift = int(3 * np.sin(2 * np.pi * l / 60))
            wave_image[:, l] = np.roll(image[:, l], k_shift)
        return wave_image

class Wave2(Augmentation):
    def apply(self, image: np.ndarray) -> np.ndarray:
        rows, cols = image.shape[:2]
        wave_image = np.zeros_like(image)
        for l in range(cols):
            k_shift = int(3 * np.sin(2 * np.pi * l / 30))
            wave_image[:, l] = np.roll(image[:, l], k_shift)
        return wave_image

# Пример использования
if __name__ == "__main__":
    image = cv2.imread("/home/wilkaone/Projects/Augmentator/augmentator/lena.png", cv2.IMREAD_GRAYSCALE)
    if image is None:
        raise FileNotFoundError("Файл изображения 'example.jpg' не найден или не может быть загружен")

    augmentator = Augmentator(image)

    noise_augmentation = AddAdaptiveNoise(noise_percentage=0.05)
    augmentator.apply(noise_augmentation)

    cv2.imshow("Noisy Image", augmentator.get_image())

    remove_noise = RemoveNoise(method="gaussian", kernel_size=5)
    augmentator.apply(remove_noise)
    
    remove_noise_average = RemoveNoise(method="average", kernel_size=5)
    augmentator.apply(remove_noise_average)

    cv2.imshow("Denoised Image", augmentator.get_image())

    histogram_eq = HistogramEqualization()
    augmentator.apply(histogram_eq)

    cv2.imshow("Histogram Equalized Image", augmentator.get_image())

    color_correction = StaticColorCorrection(alpha=1.2, beta=20)
    augmentator.apply(color_correction)

    cv2.imshow("Color Corrected Image", augmentator.get_image())

    scale = Scale(fx=1.5, fy=1.5)
    augmentator.apply(scale)
    cv2.imshow("Scaled Image", augmentator.get_image())

    translate = Translate(tx=50, ty=50)
    augmentator.apply(translate)
    cv2.imshow("Translated Image", augmentator.get_image())

    rotate = Rotate(angle=45)
    augmentator.apply(rotate)
    cv2.imshow("Rotated Image", augmentator.get_image())

    glass_effect = GlassEffect()
    augmentator.apply(glass_effect)
    cv2.imshow("Glass Effect", augmentator.get_image())

    motion_blur = MotionBlur(kernel_size=15)
    augmentator.apply(motion_blur)
    cv2.imshow("Motion Blur", augmentator.get_image())

    wave1 = Wave1()
    augmentator.apply(wave1)
    cv2.imshow("Wave 1", augmentator.get_image())

    wave2 = Wave2()
    augmentator.apply(wave2)
    cv2.imshow("Wave 2", augmentator.get_image())

    cv2.waitKey(0)
    cv2.destroyAllWindows()

