import math

from PyQt5.QtGui import (
    QPixmap)
from PyQt5.QtWidgets import (
    QDesktopWidget,
    QGraphicsPixmapItem)


class Missiles(QGraphicsPixmapItem):
    def __init__(self, x, y, angle, player):
        self.id = player.brojacmetaka
        self.angle = angle
        self.direction = [0, 0]
        self.postoji = True
        self.speed = 15
        QGraphicsPixmapItem.__init__(self)
        self.setPixmap(QPixmap("PNG/Lasers/laserBlue01.png"))
        self.Iks = x
        self.Ipsilon = y

        self.setPos(self.Iks, self.Ipsilon)

    def game_update(self, scena, listaasteroida):


        screen = QDesktopWidget().screenGeometry()


        scena.addItem(self)

        self.direction[0] = math.sin(-math.radians(self.angle))
        self.direction[1] = math.cos(math.radians(self.angle))
        self.Iks += self.direction[0] * 15
        self.Ipsilon += self.direction[1] * 15
        #self.setTransformOriginPoint(self.boundingRect().center()) #lol

        self.setRotation(self.angle)

        self.setPos(self.Iks + 45, self.Ipsilon + 45)

        if int(math.ceil(self.x() / 10) * 10) == screen.width() or int(math.ceil(self.y() / 10) * 10) == screen.height() \
                or int(math.ceil(self.x() / 10) * 10) == 0 or int(math.ceil(self.y() / 10) * 10) == 0:
            scena.removeItem(self)
            self.postoji = False



