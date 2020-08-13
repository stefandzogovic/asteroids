import math
import random
import time
from random import randrange

from PyQt5.QtCore import (
    QThread, pyqtSignal)
from PyQt5.QtGui import (
    QPixmap)
from PyQt5.QtWidgets import (
    QDesktopWidget,
    QGraphicsPixmapItem)

ASTEROID_SIZE3 = 50
ASTEROID_SIZE2 = 100
ASTEROID_SIZE1 = 200

class Asteroid(QGraphicsPixmapItem):
    def __init__(self, id, x, y, putanja, velicina, z):
        QGraphicsPixmapItem.__init__(self)
        self.z = z
        self.th = 0
        self.id = id
        self.brojac = 0
        self.putanja = putanja
        self.velicina = velicina
        self.setPos(x, y)
        if velicina == 1:
            self.setPixmap(QPixmap("PNG/Meteors/meteorGrey_big1.png").scaled(ASTEROID_SIZE1, ASTEROID_SIZE1))
        elif velicina == 2:
            self.setPixmap(QPixmap("PNG/Meteors/meteorGrey_big1.png").scaled(ASTEROID_SIZE2, ASTEROID_SIZE2))
        else:
            self.setPixmap(QPixmap("PNG/Meteors/meteorGrey_big1.png").scaled(ASTEROID_SIZE3, ASTEROID_SIZE3))

    def destroy(self, lista):
        if self.velicina == 1 or self.velicina == 2:
            self.breakintwo(self, self.velicina + 1, lista)
        else:
            lista.remove(self)
            self.th.quit()
            del self

    def breakintwo(self, asteroid, velicina, lista):
        for x in lista:
            if x.split(',')[0] == asteroid.id:
                lista.remove(x)

        self.createTwoBrokenAsteroids(asteroid.x(), asteroid.y(), velicina)

    def createTwoBrokenAsteroids(self, x, y, velicina, scena):
        createAsteroid(x + 20, y + 20, random.randint(1, 4), velicina, scena)
        createAsteroid(x - 20, y - 20, random.randint(1, 4), velicina, scena)


    def updatePosition(self, x, y):
        screen = QDesktopWidget().screenGeometry()
        if self.z == 1:  # asteroid se stvara na levom delu ekrana
            if self.putanja == 0:  # stvoren asteroid se krece dijagonalno ka dole
                if int(math.ceil(self.x() / 10) * 10) == screen.width():
                    self.setPos(0, self.y())
                if int(math.ceil(self.y() / 10) * 10) == screen.height():
                    self.setPos(self.x(), 0)
                else:
                    self.setPos(x + self.x(), self.y() + y)
            else:  # stvoren asteroid se krece dijagonalno ka gore
                if int(math.ceil(self.x() / 10) * 10) == screen.width():
                    self.setPos(0, self.y())
                if int(math.ceil(self.y() / 10) * 10) == -150:
                    self.setPos(self.x(), screen.height())
                else:
                    self.setPos(x + self.x(), self.y() - y)

        elif self.z == 2:
            if self.putanja == 0:
                if int(math.ceil(self.x() / 10) * 10) == 0:
                    self.setPos(screen.width(), self.y())
                elif int(math.ceil(self.y() / 10) * 10) == -150:
                    self.setPos(self.x(), screen.height())
                else:
                    self.setPos(self.x() - x, self.y() - y)
            else:
                if int(math.ceil(self.x() / 10) * 10) == -150:
                    self.setPos(screen.width(), self.y())
                if int(math.ceil(self.y() / 10) * 10) == screen.height():
                    self.setPos(self.x(), 0)
                else:
                    self.setPos(self.x() - x, self.y() + y)

        elif self.z == 3:
            if self.putanja == 0:
                if int(math.ceil(self.y() / 10) * 10) == screen.height():
                    self.setPos(self.x(), 0)
                if int(math.ceil(self.x() / 10) * 10) == screen.width():
                    self.setPos(0, self.y())
                else:
                    self.setPos(self.x() + x * 0.4, self.y() + y * 1.4)
            else:
                if int(math.ceil(self.y() / 10) * 10) == screen.height():
                    self.setPos(self.x(), 0)
                if int(math.ceil(self.x() / 10) * 10) == -150:
                    self.setPos(screen.width(), self.y())
                else:
                    self.setPos(self.x() - x * 0.4, self.y() + y * 1.4)

        elif self.z == 4:
            if int(math.ceil(self.y() / 10) * 10) == -50:
                self.setPos(self.x(), screen.height())
            else:
                self.setPos(self.x(), self.y() - y)


class MoveThread(QThread):
    s = pyqtSignal(float, float)

    def __init__(self, velicina, lobby):
        super().__init__()
        self.velicina = velicina
        self.var = lobby.lobby.trenutannivo / 10

    def run(self):
        while True:
            time.sleep(0.01)
            self.s.emit(self.velicina / 2 + self.var, self.velicina / 2 + self.var)

class CreateAsteroidsThread(QThread):
    s = pyqtSignal(float, float, float, float, object)

    def __init__(self, lobby):
        super().__init__()
        self.lobby = lobby

    def run(self):
        screen = QDesktopWidget().screenGeometry()
        blokiraj = True
        while True:
            if self.lobby.lobby.queue_for_asteroids:
                temp = self.lobby.lobby.queue_for_asteroids.pop()
                temp = temp.split(',')
                self.s.emit(float(temp[0]), float(temp[1]), float(temp[2]), float(temp[3]), self.lobby)
            velicina = random.randint(1, 3)
            if blokiraj:
                xory = random.randint(0, 1)
                if xory == 0:
                    leftorright = random.randint(0, 1)
                    if leftorright == 0:
                        self.s.emit(0, randrange(0, screen.height()), 1, velicina, self.lobby)
                    else:
                        self.s.emit(screen.width(), randrange(0, screen.height()), 2, velicina, self.lobby)
                else:
                    upordown = random.randint(0, 1)
                    if upordown == 0:
                        self.s.emit(randrange(0, screen.width()), 0, 3, velicina, self.lobby)
                    else:
                        self.s.emit(randrange(0, screen.width()), screen.height() - 25, 4, velicina, self.lobby)

                time.sleep(0.5)
                self.lobby.lobby.brojacthreadova = self.lobby.lobby.brojacthreadova + 1

                if self.lobby.lista != [] and self.lobby.lobby.brojacthreadova % self.lobby.lobby.brojasteroida == 0:
                    blokiraj = False
            else:

                if self.lobby.lista != [] and self.lobby.lobby.brojacthreadova % self.lobby.lobby.brojasteroida == 0:
                    blokiraj = False
                    time.sleep(0.02)
                else:
                    blokiraj = True
                    self.lobby.lobby.vejvovi += 1
                    if self.lobby.lobby.vejvovi > self.lobby.lobby.trenutannivo:
                        self.lobby.lobby.brojacthreadova = 0
                        self.lobby.lobby.brojasteroida += 1
                        self.lobby.lobby.trenutannivo += 1
                        self.lobby.lobby.vejvovi = 1
                        time.sleep(5)
                self.s.emit(0, 0, -1, velicina, 0)


def createAsteroid(iks, ips, z, velicina, lobby):
    # print(lobby)
    if z != -1:
          putanja = random.randint(0, 1)
          # stringg = str(lobby.ajdi) + "," + str(iks) + "," + str(ips) + "," + str(putanja) + "," + str(velicina) + "," + str(z) + ":"
          ast = Asteroid(lobby.lobby.ajdi, iks, ips, putanja, velicina, z)
          lobby.lista.append(ast)
          ast.th = MoveThread(ast.velicina, lobby)
          ast.th.s.connect(ast.updatePosition)
          ast.th.start()
          # lobby.lista.append(stringg)
          lobby.lobby.ajdi += 1



def createRandomAsteroid(vel):
        screen = QDesktopWidget().screenGeometry()
        velicina = float(vel) - 1
        if velicina == 0:
            return 0
        xory = random.randint(0, 1)
        if xory == 0:
            leftorright = random.randint(0, 1)
            if leftorright == 0:
                return 0, randrange(0, screen.height()), 1, velicina
            else:
                return screen.width(), randrange(0, screen.height()), 2, velicina

        else:
            upordown = random.randint(0, 1)
            if upordown == 0:
                return randrange(0, screen.width()), 0, 3, velicina
            else:
                return randrange(0, screen.width() - 150), screen.height() - 25, 4, velicina