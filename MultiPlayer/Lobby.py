from PyQt5.QtCore import QObject


class Lobby:
    def __init__(self, id):
        self.player_cnt = 0
        self.id = id
        self.name = "Lobby {}".format(self.id)
        self.queue = []
        self.queue_for_asteroids = []
        self.pos = ["0:0,0,0,0,", "1:0,0,0,0,", "2:0,0,0,0,", "3:0,0,0,0,"]
        self.brojacthreadova = 0
        self.brojasteroida = 5
        self.trenutannivo = 1
        self.vejvovi = 1
        self.ajdi = 0
        self.brojac = 0

class Lobby_and_conn:
    def __init__(self, lobby):
        self.lobby = lobby
        self.connections = []
        self.lista = []

