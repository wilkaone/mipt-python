"""
Шаблонный метод (Template method)
"""
import cv2
import numpy as np

class ObjectAnalysis(object):
    def template_method(self, image):

        image = self.noise_filtering(image)
        data = self.segmentation(image)
        data = self.object_parameters(data)

        return data

    def noise_filtering(self, image):
        raise NotImplementedError()

    def segmentation(self, data):
        raise NotImplementedError()

    def object_parameters(self, data):
        (image, data) = data
        (numLabels, labels, stats, centroids) = data
        x = []
        y = []
        w = []
        h = []
        area = []
        for i in range(1, numLabels):
            # extract the connected component statistics for the current
            # label
            x.append(stats[i, cv2.CC_STAT_LEFT])
            y.append(stats[i, cv2.CC_STAT_TOP])
            w.append(stats[i, cv2.CC_STAT_WIDTH])
            h.append(stats[i, cv2.CC_STAT_HEIGHT])
            area.append(stats[i, cv2.CC_STAT_AREA])

        return (x, y, w, h, area)


class BinaryImage(ObjectAnalysis):
    def __init__(self):
        pass

    def noise_filtering(self, image):
        median = cv2.medianBlur(image, 5)
        return median

    def segmentation(self, image):
        output = cv2.connectedComponentsWithStats(image, 4, cv2.CV_32S)
        return (image, output)

class MonochromeImage(BinaryImage):
    def __init__(self):
        pass

    def noise_filtering(self, image):
        return cv2.GaussianBlur(image, (5, 5), 0)

    def segmentation(self, image):
        edges = cv2.Canny(image, 100, 200)
        output = cv2.connectedComponentsWithStats(edges, 4, cv2.CV_32S)
        return (edges, output)

class ColorImage(MonochromeImage):
    def __init__(self):
        pass

    def segmentation(self, image):
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        _, binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)

        dist_transform = cv2.distanceTransform(binary, cv2.DIST_L2, 5)
        _, sure_fg = cv2.threshold(dist_transform, 0.7 * dist_transform.max(), 255, 0)

        sure_fg = np.uint8(sure_fg)
        unknown = cv2.subtract(binary, sure_fg)
        _, markers = cv2.connectedComponents(sure_fg)
        markers = markers + 1
        markers[unknown == 255] = 0
        cv2.watershed(image, markers)

        output = cv2.connectedComponentsWithStats(sure_fg, 4, cv2.CV_32S)
        return (image, output)



"""
Декоратор - структурный паттерн
"""

class FilteredAnalysis(ObjectAnalysis):
    def __init__(self, obj):
        self._proc = obj

    def template_method(self, image):
        (_x, _y, _w, _h, _area) = self._proc.template_method(image)
        x = []
        y = []
        w = []
        h = []
        area = []
        moments = []

        for i in range(len(_area)):
            if _area[i] > 10 and _area[i] < 2500:
                x.append(_x[i])
                y.append(_y[i])
                w.append(_w[i])
                h.append(_h[i])
                area.append(_area[i])

                mask = np.zeros_like(image, dtype=np.uint8)
                cv2.rectangle(mask, (x[-1], y[-1]), (x[-1] + w[-1], y[-1] + h[-1]), 255, -1)
                hu_moments = cv2.HuMoments(cv2.moments(mask)).flatten()
                moments.append(hu_moments)

        return (x, y, w, h, area, moments)


if __name__== '__main__':
    print("Binary Image Processing")
    bin_segm = BinaryImage()
    (x,y,w,h,area) = bin_segm.template_method(cv2.imread('/home/wilkaone/Projects/mipt-python/hometask8/data/1.jpg', cv2.IMREAD_GRAYSCALE))
    for i in range(len(area)):
            print([x[i], y[i], w[i],h[i],area[i]])

    print("Decorated Binary Image Processing")
    filt_bin = FilteredAnalysis(BinaryImage())
    (x, y, w, h, area, moments) = filt_bin.template_method(cv2.imread('/home/wilkaone/Projects/mipt-python/hometask8/data/1.jpg', cv2.IMREAD_GRAYSCALE))
    for i in range(len(area)):
        print([x[i], y[i], w[i], h[i], area[i], moments[i]])

    print("Color Image Processing")
    color_segm = ColorImage()
    (x, y, w, h, area) = color_segm.template_method(cv2.imread('/home/wilkaone/Projects/mipt-python/hometask8/data/1.jpg', cv2.IMREAD_COLOR))
    for i in range(len(area)):
        print([x[i], y[i], w[i], h[i], area[i]])
