from PyQt5.QtWidgets import QGraphicsView, QGraphicsPixmapItem, QGraphicsScene
from PyQt5.QtGui import QMouseEvent, QPixmap
from PyQt5.Qt import Qt

class ImageGraphicsView(QGraphicsView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.zoom_factor_base = 1.0015
        self.scale_factor = 1
        self.setCursor(Qt.CrossCursor)

        self.scene = QGraphicsScene()
        self.pixmap_item = QGraphicsPixmapItem()

        self.scene.addItem(self.pixmap_item)
        self.setScene(self.scene)

    def wheelEvent(self, event):
        scale_factor = 1.25
        if event.angleDelta().y() > 0:
            self.scale(scale_factor, scale_factor)
        else:
            self.scale(1.0 / scale_factor, 1.0 / scale_factor)

    def mousePressEvent(self, event):
        if event.buttons() & Qt.RightButton:
            release_event = QMouseEvent(
                QMouseEvent.MouseButtonRelease,
                event.localPos(),
                event.screenPos(),
                Qt.RightButton,
                event.buttons() & ~Qt.RightButton,
                event.modifiers(),
            )
            super().mouseReleaseEvent(release_event)
            self.setDragMode(QGraphicsView.ScrollHandDrag)
            fake_event = QMouseEvent(
                event.type(),
                event.localPos(),
                event.screenPos(),
                Qt.LeftButton,
                event.buttons() | Qt.LeftButton,
                event.modifiers(),
            )
            super().mousePressEvent(fake_event)

        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.RightButton:
            fake_event = QMouseEvent(
                event.type(),
                event.localPos(),
                event.screenPos(),
                Qt.RightButton,
                event.buttons() & ~Qt.RightButton,
                event.modifiers(),
            )
            super().mouseReleaseEvent(fake_event)
            self.setDragMode(QGraphicsView.NoDrag)

        super().mouseReleaseEvent(event)

    def set_image(self, file_path):
        pixmap = QPixmap(file_path)
        self.pixmap_item.setPixmap(QPixmap(file_path))
        self.resetTransform()