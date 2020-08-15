import datetime
import functools
import math
import pickle
import sys

from PyQt5.QtCore import (
    Qt, QBasicTimer, pyqtSlot)
from PyQt5.QtGui import (
    QPixmap,
    QBrush)
from PyQt5.QtWidgets import (
    QGraphicsPixmapItem, QGraphicsScene, QDesktopWidget, QGraphicsRectItem, QGraphicsView, QApplication, QTableWidget,
    QTableWidgetItem, QPushButton)

from MultiPlayer import networkmultiplayer, Missile, Asteroid

in_lobby = 0
spejs = ""
brojacthreadova = 0
lista = []
screen = 0
current_lobby_id = 0
povratnistring = ","
SCREEN_WIDTH            = 1920
SCREEN_HEIGHT           = 1080
#PLAYER_SPEED            = 3   # pix/frame
PLAYER_BULLET_X_OFFSETS = [0, 45]
PLAYER_BULLET_Y         = 15
BULLET_SPEED            = 10  # pix/frame
BULLET_FRAMES           = 50
FRAME_TIME_MS           = 16  # ms/frame
ASTEROID_SIZE3 = 50
ASTEROID_SIZE2 = 100
ASTEROID_SIZE1 = 200
listaasteroida = []


class Player(QGraphicsPixmapItem):
    def __init__(self, position, datetime):

        self.brojacmetaka = 0
        self.angle = 0         # Ugao rotacije
        self.direction = [0, -1]
        self.throttle = False
        self.speed = 0
        self.spejs = 0
        self.fire_time = datetime   # Player ne moze da pukne vise puta u meriodu od 0.15 sekundi, pa zato treba datetime

        self.score = 0
        self.lives = 3

        QGraphicsPixmapItem.__init__(self)
        self.slika = QPixmap('PNG/playerShip3_red.png')
        self.setPixmap(self.slika)

        self.active_missiles = []
        self.setPos(position[0], position[1])  # Pocetna pozicija, sredina ekrana

    def destroyPlayer(self, scene):  # na osnovu broja zivota menja score, 4 je za deus ex machinu i kad dode do poslenjeg zivota KRAJ
        global listaasteroida
        global povratnistring
        povratnistring = ","
        try:
            for asteroid in listaasteroida:
                if self.collidesWithItem(asteroid):
                    self.setPos(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)  # ako udari asteroid, respawn na sredinu ekrana
                    povratnistring = "," + str(scene.net.id) + "@" + str(asteroid.id) + "@" + str(asteroid.x()) + "@" + str(asteroid.y())
                    listaasteroida.remove(asteroid)
                    scene.removeItem(asteroid)
                    # asteroid.th.terminate()
        except Exception as e:
            trace_back = sys.exc_info()[2]
            line = trace_back.tb_lineno
            print(format(line), e)
    def game_update(self, keys_pressed):
        global screen
        dx = 0
        dy = 0

        self.spejs = 0

        if Qt.Key_Left in keys_pressed:
            self.angle -= 8
            self.angle %= 360

            self.direction[0] = math.sin(-math.radians(self.angle))
            self.direction[1] = math.cos(math.radians(self.angle))

            dx += self.direction[0] * self.speed
            dy += self.direction[1] * self.speed

            self.setTransformOriginPoint(self.boundingRect().center())

            self.setRotation(self.angle)

        if Qt.Key_Right in keys_pressed:
            self.angle += 8
            self.angle %= 360

            self.direction[0] = math.sin(-math.radians(self.angle))
            self.direction[1] = math.cos(math.radians(self.angle))

            dx += self.direction[0] * self.speed
            dy += self.direction[1] * self.speed

            self.setTransformOriginPoint(self.boundingRect().center())
            self.setRotation(self.angle)
            # self.setTransformOriginPoint(-self.boundingRect().width() /2, -self.boundingRect().height() / 2)

        if Qt.Key_Up in keys_pressed:
            self.throttle = True

            if self.speed < 6:
                self.speed += 1
            self.direction[0] = math.sin(-math.radians(self.angle))
            self.direction[1] = math.cos(math.radians(self.angle))

            dx += self.direction[0] * self.speed
            dy += self.direction[1] * self.speed
        else:
            if self.speed > 0:
                self.speed -= 3

        if Qt.Key_Space in keys_pressed:

            self.spejs = 0
            new_time = datetime.datetime.now()
            if new_time - self.fire_time > datetime.timedelta(seconds=0.15):
                adjust = [0, 0]
                self.spejs = 1
                adjust[0] = math.sin(-math.radians(self.angle)) * self.slika.width()
                adjust[1] = -math.sin(-math.radians(self.angle)) * self.slika.height()

                # self.nekiBroj += 1
                new_missile = Missile.Missiles(self.x(), self.y(), float(self.angle), self)
                self.brojacmetaka += 1
                if self.brojacmetaka == 50:
                    self.brojacmetaka = 0
                self.active_missiles.append(new_missile)
                self.fire_time = new_time

        if int(math.ceil(self.x() / 10) * 10) > SCREEN_WIDTH:               # ako player izade van ekrana poslace ga
            self.setPos(dx, int(self.y()) + dy)                               # suprotnu stranu ekrana
        elif int(math.ceil(self.y() / 10) * 10) > SCREEN_HEIGHT:
            self.setPos(int(self.x()) + dx,  dy)
        elif int(math.ceil(self.x() / 10) * 10) < -self.slika.height():
            self.setPos(int(SCREEN_WIDTH + dx, self.y() + dy))
        elif int(math.ceil(self.y() / 10) * 10) < - self.slika.height():
            self.setPos(self.x() + dx, int(SCREEN_HEIGHT + dy))
        else:
            self.setPos(self.x() + dx, self.y() + dy)


class Scene(QGraphicsScene):
    def __init__(self):
        QGraphicsScene.__init__(self)
        self.screen = QDesktopWidget().screenGeometry()
        self.net = networkmultiplayer.Network()

        # hold the set of keys we're pressing
        self.keys_pressed = set()

        # use a timer to get 60Hz refresh (hopefully)
        self.timer = QBasicTimer()
        self.timer.start(FRAME_TIME_MS, self)

        bg = QGraphicsRectItem()
        bg.setRect(0, 0, SCREEN_WIDTH , SCREEN_HEIGHT)
        bg.setBrush(QBrush(Qt.black))
        self.addItem(bg)

        self.player = Player((SCREEN_WIDTH/2, SCREEN_HEIGHT/2), datetime.datetime.now())


        self.player2 = Player((SCREEN_WIDTH/2, SCREEN_HEIGHT/2), datetime.datetime.now())
        self.player3 =Player((SCREEN_WIDTH/2, SCREEN_HEIGHT/2), datetime.datetime.now())
        self.player4 = Player((SCREEN_WIDTH/2, SCREEN_HEIGHT/2), datetime.datetime.now())
        self.plejeri = [self.player, self.player2, self.player3, self.player4]
        self.addItem(self.player)
        self.addItem(self.player2)
        self.addItem(self.player3)
        self.addItem(self.player4)

        self.lobbies = pickle.loads(self.net.recv_pickle())
        self.table = QTableWidget()
        self.table.insertColumn(0)
        self.table.insertColumn(1)
        self.table.insertColumn(2)
        self.table.insertColumn(3)
        self.table.setHorizontalHeaderItem(0, QTableWidgetItem("Lobby Name"))
        self.table.setHorizontalHeaderItem(1, QTableWidgetItem("Current Players"))
        self.table.setHorizontalHeaderItem(2, QTableWidgetItem("Available"))
        self.table.setHorizontalHeaderItem(3, QTableWidgetItem("Create/Join"))

        self.table.setFixedSize(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 3 )
        self.table.move(SCREEN_WIDTH / 2 - self.table.width() / 2, SCREEN_HEIGHT / 2 - self.table.height() / 4)
        self.table.adjustSize()
        self.table.horizontalHeader().setSectionResizeMode(1)
        self.table.verticalHeader().setVisible(0)
        self.table.setItem(0, 0, QTableWidgetItem("Name"))

        for lob in self.lobbies:
            self.table.insertRow(lob.id - 1)
            self.table.setItem(lob.id - 1, 0, QTableWidgetItem(lob.name))
            self.table.setItem(lob.id - 1, 1, QTableWidgetItem(str(lob.player_cnt)))
            if lob.player_cnt <= 4:
                self.table.setItem(lob.id - 1, 2, QTableWidgetItem("Yes"))
            else:
                self.table.setItem(lob.id - 1, 2, QTableWidgetItem("No"))

            self.button_play = QPushButton('Join')
            self.button_play.clicked.connect(functools.partial(self.on_click_join, lob.id), lob.player_cnt)
            self.button_play.setParent(self.table)
            self.table.setCellWidget(lob.id - 1, 3, self.button_play)

        self.addWidget(self.table)

        self.view = QGraphicsView(self)
        self.view.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.view.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.view.setFixedSize(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.setSceneRect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)
        self.view.showFullScreen()


    @pyqtSlot()
    def on_click_join(self, lobby_id, player_cnt):
        global current_lobby_id
        if player_cnt < 4:
            current_lobby_id = lobby_id
            self.removeItem(self.table.graphicsProxyWidget())
            self.net.send2(str(current_lobby_id))
            self.net.id = int(self.net.recv())
            print(self.net.id)

    def send_data(self, spejs):
        global povratnistring
        """
        Send position to server
        :return: None
        """
        data = str(self.net.id) + ":" + str(self.player.x()) + "," + str(self.player.y()) + "," + str(self.player.rotation()) + "," + str(spejs) + povratnistring

        reply = self.net.send(data)
        return reply


    @staticmethod
    def parse_data(data):
        d = data.split("|")
        return d

    def keyPressEvent(self, event):
        self.keys_pressed.add(event.key())


    def keyReleaseEvent(self, event):
        self.keys_pressed.remove(event.key())

    def timerEvent(self, event):
        self.game_update()
        self.update()


    def sudarMetakAsteroid(self, b, plejer):
        global listaasteroida
        global povratnistring
        for asteroid in listaasteroida:
            if b.collidesWithItem(asteroid):
                self.removeItem(b)
                listaasteroida.remove(asteroid)
                scene.removeItem(asteroid)
                # asteroid.th.terminate()
                b.postoji = False
                plejer.active_missiles.remove(b)
                povratnistring = "," + str(scene.net.id) + "@" + str(asteroid.id) + "@" + str(asteroid.x()) + "@" + str(asteroid.y())

    def game_update(self):
        global current_lobby_id
        if current_lobby_id != 0:
            try:
                self.player.destroyPlayer(self)
                global spejs
                for b in self.player.active_missiles:
                    b.game_update(self, listaasteroida)
                    self.sudarMetakAsteroid(b, self.player)

                    if b.postoji == False:
                        self.removeItem(b)

                for b in self.player2.active_missiles:
                    b.game_update(self, listaasteroida)
                    self.sudarMetakAsteroid(b, self.player2)

                    if b.postoji == False:
                        self.removeItem(b)

                for b in self.player3.active_missiles:
                    b.game_update(self, listaasteroida)
                    self.sudarMetakAsteroid(b, self.player3)

                    if b.postoji == False:
                        self.removeItem(b)

                for b in self.player4.active_missiles:
                    b.game_update(self, listaasteroida)
                    self.sudarMetakAsteroid(b)
                    if b.postoji == False:
                        self.removeItem(b)
                self.player.game_update(self.keys_pressed)

                data, data1 = self.parse_data(self.send_data(self.player.spejs))
                data = data.split('/')
                # print(data)
                # print(data1)

                x, y, z, q, kolizija = data[0].split(':')[1].split(',')

                if kolizija != "":
                    idplayera = kolizija.split('@')[0]
                    idasteroida = kolizija.split('@')[1]
                    item = next((item for item in listaasteroida if item.id == int(idasteroida)), None)
                    try:
                        self.plejeri[(int(idplayera))].destroyPlayer(self)
                        self.removeItem(item)
                    except Exception as e:
                        trace_back = sys.exc_info()[2]
                        line = trace_back.tb_lineno
                        print(format(line), e)
                if int(q) == 1:
                    x = float(self.player2.x())
                    y = float(self.player2.y())
                    try:
                        xd = Missile.Missiles(x, y, float(z), self.player2)

                    except Exception as e:
                        trace_back = sys.exc_info()[2]
                        line = trace_back.tb_lineno
                        print(format(line), e)

                    self.player2.active_missiles.append(xd)
                    self.player2.brojacmetaka += 1
                    if self.player2.brojacmetaka == 50:
                        self.player2.brojacmetaka = 0
                self.player2.setPos(float(x), float(y))
                self.player2.setTransformOriginPoint(self.player2.boundingRect().center())
                self.player2.setRotation(float(z))

                x, y, z, q, kolizija = data[1].split(':')[1].split(',')

                if kolizija != "":
                    idplayera = kolizija.split('@')[0]
                    idasteroida = kolizija.split('@')[1]
                    item = next((item for item in listaasteroida if item.id == int(idasteroida)), None)
                    try:
                        self.plejeri[(int(idplayera))].destroyPlayer(self)
                        self.removeItem(item)
                    except Exception as e:
                        trace_back = sys.exc_info()[2]
                        line = trace_back.tb_lineno
                        print(format(line), e)
                if int(q) == 1:
                    self.player3.active_missiles.append(Missile.Missiles(self.player3.x(), self.player3.y(), float(z), self.player3))

                    self.player3.brojacmetaka += 1
                    if self.player3.brojacmetaka == 50:
                        self.player3.brojacmetaka = 0
                self.player3.setPos(float(x), float(y))
                self.player3.setTransformOriginPoint(self.player3.boundingRect().center())
                self.player3.setRotation(float(z))

                x, y, z, q, kolizija = data[2].split(':')[1].split(',')

                if kolizija != "":
                    idplayera = kolizija.split('@')[0]
                    idasteroida = kolizija.split('@')[1]
                    item = next((item for item in listaasteroida if item.id == int(idasteroida)), None)
                    try:
                        self.plejeri[(int(idplayera))].destroyPlayer(self)
                        self.removeItem(item)
                    except Exception as e:
                        trace_back = sys.exc_info()[2]
                        line = trace_back.tb_lineno
                        print(format(line), e)

                if int(q) == 1:
                    self.player4.active_missiles.append(Missile.Missiles(self.player4.x(), self.player4.y(), float(z), self.player4))

                    self.player4.brojacmetaka += 1
                    if self.player4.brojacmetaka == 50:
                        self.player4.brojacmetaka = 0
                self.player4.setPos(float(x), float(y))
                self.player4.setTransformOriginPoint(self.player4.boundingRect().center())
                self.player4.setRotation(float(z))

                if data1:
                    asteroidi = data1.split(':')
                    temp = False
                    brojasteroida = 0
                    for ast in asteroidi:
                        ast = ast.split(',')
                        temp = False
                        for asteroid in listaasteroida:
                            if int(ast[0]) == asteroid.id:
                                temp = True
                                asteroid.setX(float(ast[1]))
                                asteroid.setY(float(ast[2]))


                        if temp == False:
                            x = Asteroid.Asteroid(int(ast[0]), float(ast[1]), float(ast[2]), float(ast[3]), float(ast[4]),
                                                  float(ast[5]))
                            self.addItem(x)
                            listaasteroida.append(x)

                            # x.th = Asteroid.MoveThread2(x.velicina, self.lobbies[current_lobby_id - 1])
                            # x.th.s.connect(x.updatePosition)
                            # x.th.start()
            except Exception as e:
                trace_back = sys.exc_info()[2]
                line = trace_back.tb_lineno
                print(format(line), e)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    scene = Scene()
    sys.exit(app.exec_())
