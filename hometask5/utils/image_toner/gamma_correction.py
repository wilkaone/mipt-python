import cv2
import numpy as np

def processing(image, gamma):    
    return cv2.LUT(image, np.array([((i / 255.0) ** (1.0 / gamma)) * 255 for i in range(256)]).astype("uint8"))