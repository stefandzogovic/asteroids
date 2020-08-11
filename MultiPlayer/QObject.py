import math
import sys
import random
import time

from random import randrange

from PyQt5 import QtCore
from PyQt5.QtCore import (
    Qt,
    QBasicTimer,
    QRectF, QThread, pyqtSignal, QSize, QObject)
from PyQt5.QtGui import (
    QBrush,
    QPixmap,
    QFont,
    QImage,
    QColor, QPen, QPainter)
from PyQt5.QtWidgets import (
    QDesktopWidget,
    QApplication,
    QGraphicsItem,
    QGraphicsPixmapItem,
    QGraphicsRectItem,
    QGraphicsScene,
    QGraphicsView,
    QMainWindow, QGraphicsLineItem, QLabel)

from MultiPlayer import Asteroid


class ObjekatZaThread(QGraphicsScene):
    def __init__(self, lobby):
        QGraphicsScene.__init__(self)
        self.lobbyandconn = lobby
        self.th = Asteroid.CreateAsteroidsThread(self.lobbyandconn)
        self.th.s.connect(Asteroid.createAsteroid)
        self.th.start()



"""if __name__ == '__main__':
    app = QApplication(sys.argv)
    obj = ObjekatZaThread()
    sys.exit(app.exec_())
"""