#
import cv2

def processing(image):
    return cv2.equalizeHist(image)