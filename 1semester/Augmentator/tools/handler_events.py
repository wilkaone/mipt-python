import os
import threading

from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtCore import QObject, pyqtSignal
from tools.dataset_loader import DatasetLoader
from augmentator.augmentator import *

class HandlerEvents(QObject):
    signal_message = pyqtSignal(str)
    def __init__(self, main_window, ui_window):
        super().__init__()
        self.main_window = main_window
        self.ui = ui_window
        self.index_show_image = 0  
        self.current_class = ""
    def load_dataset(self):
        dataset_path = QFileDialog.getExistingDirectory(self.main_window, "Select Dataset Directory")
        if dataset_path:
            self.dataset_loader = DatasetLoader(dataset_path)
            data = self.dataset_loader.load_data()
            return data
        return dict()

    def show_dataset(self):
        dataset_path = QFileDialog.getExistingDirectory(self.main_window, "Select Dataset Directory")
        if dataset_path:
            self.dataset_loader = DatasetLoader(dataset_path)
            data = self.dataset_loader.load_data()
            classes = data.keys()

            self.ui.combobox_classes.clear()
            for class_name in classes:
                self.ui.combobox_classes.addItem(class_name)
            self.index_show_image = 0
            self.current_class = ""
            self.ui.combobox_classes.setCurrentIndex(-1);
            return data
        return dict()
    
    def change_class(self, text, data):
        for class_name in data.keys():
            print(class_name)
            if class_name == text:
                images = data[class_name]
                self.current_class = class_name
                self.ui.graphicsView.set_image(images[0])

    def back_image(self, data):
        images = data[self.current_class]
        if self.index_show_image == 0:
            self.ui.graphicsView.set_image(images[len(images) - 1])
            self.index_show_image = len(images) - 1
        else:
            self.ui.graphicsView.set_image(images[self.index_show_image - 1])
            self.index_show_image -= 1

    def next_image(self, data):
        images = data[self.current_class]
        if self.index_show_image == (len(images) - 1):
            self.ui.graphicsView.set_image(images[0])
            self.index_show_image = 0
        else:
            self.ui.graphicsView.set_image(images[self.index_show_image + 1])
            self.index_show_image += 1

    def augment_dataset(self, data):
        directory = QFileDialog.getExistingDirectory(self.main_window, "Select Directory for Saving Dataset", "")
        if not directory:
            print("No directory selected.")
            return

        thread = threading.Thread(target=self.augment_dataset_thread, args=(data, directory))
        thread.start()

    def augment_dataset_thread(self, data, directory):
        if len(data) <= 0:
            return
        if directory:
            for class_name, images in data.items():
                class_dire = os.path.join(directory, class_name)

                if not os.path.exists(class_dire):
                    os.makedirs(class_dire)

                for image_path in images:
                    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
                    for index in range(self.ui.spinbox_count_aug.value()):
                        augmentator = Augmentator(image)

                        self.apply_noise(augmentator)
                        self.apply_denoising(augmentator)
                        self.apply_color_correction(augmentator)
                        self.apply_transformation(augmentator)
                        self.apply_rotation(augmentator)
                        self.apply_scaling(augmentator)
                        self.apply_motion_blur(augmentator)
                        self.apply_wave_effect(augmentator)
                        self.apply_glass_effect(augmentator)

                        image_name = os.path.splitext(os.path.basename(image_path))[0]
                        extension = os.path.splitext(image_path)[1]
                        new_image_name = f"{image_name}_{index}{extension}"
                        
                        save_path = os.path.join(class_dire, new_image_name)
                        cv2.imwrite(save_path, augmentator.get_image())
            self.signal_message.emit("Готово")

    def apply_noise(self, augmentator):
        if self.ui.checkbox_adaptive_noise.isChecked():
            noise_augmentation = AddAdaptiveNoise(noise_percentage=(self.ui.spinbox_noise.value() / 100))
            augmentator.apply(noise_augmentation)

    def apply_denoising(self, augmentator):
        if self.ui.checkbox_remove_noise.isChecked():
            method = self.ui.combobox_remove_noise_method.currentText()
            kernel_size = self.ui.combobox_remove_noise_size_kernel.currentText()

            if method == "gaussian":
                remove_noise = RemoveNoise(method="gaussian", kernel_size=int(kernel_size.replace('x', '')))
                augmentator.apply(remove_noise)
            elif method == "average":
                remove_noise = RemoveNoise(method="average", kernel_size=int(kernel_size.replace('x', '')))
                augmentator.apply(remove_noise)

    def apply_color_correction(self, augmentator):
        if self.ui.checkbox_conv.isChecked():
            method = self.ui.combobox_conv_method.currentText()

            if method == "Equalization":
                histogram_eq = HistogramEqualization()
                augmentator.apply(histogram_eq)
            elif method == "Static Color Correction":
                color_correction = StaticColorCorrection(alpha=self.ui.dspinbox_alpha.value(), beta=self.ui.spinbox_beta.value())
                augmentator.apply(color_correction)

    def apply_transformation(self, augmentator):
        if self.ui.checkbox_trans.isChecked():
            translate = Translate(tx=self.ui.spinbox_trans_x.value(), ty=self.ui.spinbox_trans_y.value())
            augmentator.apply(translate)

    def apply_rotation(self, augmentator):
        if self.ui.checkbox_rotate.isChecked():
            rotate = Rotate(angle=self.ui.spinbox_rotate.value())
            augmentator.apply(rotate)

    def apply_scaling(self, augmentator):
        if self.ui.checkbox_scale.isChecked():
            scale = Scale(fx=self.ui.dspinbox_scale.value(), fy=self.ui.dspinbox_scale.value())
            augmentator.apply(scale)

    def apply_motion_blur(self, augmentator):
        if self.ui.checkbox_motion_blur.isChecked():
            kernel_size = int(self.ui.combobox_motion_blur.currentText().replace('x', ''))
            motion_blur = MotionBlur(kernel_size=kernel_size)
            augmentator.apply(motion_blur)

    def apply_wave_effect(self, augmentator):
        if self.ui.checkbox_effect_wave.isChecked():
            method = self.ui.combobox_effect_wave_method.currentText()

            if method == "First":
                wave1 = Wave1()
                augmentator.apply(wave1)
            elif method == "Second":
                wave2 = Wave2()
                augmentator.apply(wave2)

    def apply_glass_effect(self, augmentator):
        if self.ui.checkbox_effect_glass.isChecked():
            glass_effect = GlassEffect()
            augmentator.apply(glass_effect)


        
        

        
