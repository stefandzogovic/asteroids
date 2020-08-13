from PyQt5.QtWidgets import (
    QGraphicsScene)

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