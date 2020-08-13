import pickle
import random
import socket
import sys
import threading

from PyQt5.QtWidgets import QApplication

from MultiPlayer import QObject, Lobby
from MultiPlayer.Lobby import Lobby_and_conn


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connections = []
lobbies_and_connections = []
lobbies = []

server = '0.0.0.0' #When you run a server-type process inside a Docker container, it needs to be configured to listen on
                   # the special "all interfaces" address 0.0.0.0. Each container has its own notion of localhost or 127.0.0.1,
                   #and if you set a process to listen or bind to 127.0.0.1, it can only be reached from its own localhost which
                   #is different from all other containers' localhost and the host's localhost.

port = 9000

server_ip = socket.gethostbyname(server)
print(server_ip)

lobby = Lobby.Lobby(1)
lobbies.append(lobby)
lobbies_and_connections.append(Lobby.Lobby_and_conn(lobby))

try:
    s.bind((server, port))

except socket.error as e:
    print(str(e))

s.listen()
print("Waiting for a connection")



def opsluzi_lobby(lista, lobby):
    global currentId, pos
    # conn.send(str.encode(str(currentId)))
    while True:
        if lobby.lobby.queue:
            reply = lobby.lobby.queue.pop()
            print("Recieved: " + reply)
            arr = reply.split(":")
            id = int(arr[0])
            missile = int((arr[1]).split(',')[3])
            kolizija = ((arr[1]).split(',')[4])
            if kolizija != "":
                idplayera, idasteroida, iksasteroida, ipsasteroida = kolizija.split('@')
                for x in lobby.lista:
                    stringg = str(x.id) + "," + str(x.x()) + "," + str(x.y()) + "," + str(x.putanja) + "," + str(x.velicina) + "," + str(x.z) + ":"
                    if stringg.split(',')[0] == idasteroida:
                        lobby.lista.remove(x)
                        x.th.quit()
                        del x
                        if float(stringg.split(',')[4]) != 3.0:
                            z = random.randint(1, 4)
                            # Asteroid.createAsteroid(float(iksasteroida) + 20, float(ipsasteroida) + 20, z, float(stringg.split(',')[4]) + 1, lobby)
                            lobby.lobby.queue_for_asteroids.append(str(float(iksasteroida) + 20) + ',' + str(float(ipsasteroida) + 20) + ',' + str(z)+ ',' + str(float(stringg.split(',')[4]) + 1))
                            z = random.randint(1, 4)
                            lobby.lobby.queue_for_asteroids.append(str(float(iksasteroida) + 20) + ',' + str(float(ipsasteroida) + 20) + ',' + str(z)+ ',' + str(float(stringg.split(',')[4]) + 1))
            lobby.lobby.pos[id] = reply
            reply = ""
            for x in lobby.lobby.pos:
                z = x.split(":")[0]
                if int(z) != id:
                    reply += x + "/"
            reply = reply[:-1]
            reply = reply + "|"
            if lobby.lista:
                for x in lobby.lista:
                    stringg = str(x.id) + "," + str(x.x()) + "," + str(x.y()) + "," + str(x.putanja) + "," + str(x.velicina) + "," + str(x.z) + ":"
                    reply = reply + stringg
                reply = reply[:-1]
            print("Sending: " + reply)

            lobby.connections[id].sendall(str.encode(reply))


def chooselobby(conn):
    global lobbies
    conn.sendall(pickle.dumps(lobbies))
    recv = conn.recv(2048)
    recv = recv.decode('utf-8')
    lobbies_and_connections[int(recv) - 1].connections.append(conn)
    x = lobbies_and_connections[int(recv) - 1].lobby.player_cnt
    conn.send(str(x).encode())
    lobbies_and_connections[int(recv) - 1].lobby.player_cnt += 1
    processThread2 = threading.Thread(target=client_recv, args=(conn, int(recv),))  # <- note extra ','
    processThread2.start()

def threadAcceptClient(lista):
    global connections
    while True:
        conn, addr = s.accept()
        connections.append(conn)
        print("Connected to: ", addr)
        processThread = threading.Thread(target=chooselobby, args=(conn,))  # <- note extra ','
        processThread.start()

def client_recv(conn, lobby_id):
    while True:
        data = conn.recv(2048)
        if not data:
            conn.send(str.encode("Goodbye"))
            break
        else:
            reply = data.decode('utf-8')
            lobbies[lobby_id - 1].queue.append(reply)

    lobbies_and_connections[lobby.id - 1].lobby.player_cnt -= 1
    lobbies_and_connections[lobby.id - 1].connections.remove(conn)
    print("Connection Closed")
    conn.shutdown(socket.SHUT_RDWR)
    conn.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    i = 0
    x = 0
    processThread = threading.Thread(target=threadAcceptClient, args=(x,))  # <- note extra ','
    processThread.start()

    x = QObject.ObjekatZaThread(lobbies_and_connections[0])
    processThread2 = threading.Thread(target=opsluzi_lobby, args=(x, lobbies_and_connections[0],))  # <- note extra ','
    processThread2.start()


    sys.exit(app.exec_())
