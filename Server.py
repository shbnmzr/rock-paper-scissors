import socket
from _thread import *
import pickle
from Game import Game

server = '172.21.112.1'
port = 5555

socket_obj = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    socket_obj.bind((server, port))
except socket.error as err:
    print(err)

socket_obj.listen(2)

print('Waiting for a connection, Server Started!\n')

connected = set()
games = dict()
id_count = 0


def threaded_client(conn, current_player, game_id):
    global id_count
    conn.send(str.encode(str(current_player)))

    while True:
        try:
            data = conn.recv(4096).decode()
            if game_id in games:
                game = games[game_id]
                if not data:
                    break
                else:
                    if data == 'reset':
                        game.reset_went()
                    elif data != 'get':
                        game.player(current_player, data)

                    reply = game
                    conn.sendall(pickle.dumps(game))
            else:
                break
        except:
            break

    print('Lost connection\n')
    print('Closing game ', game_id)

    try:
        del game[game_id]
        print('Closing game ', game_id)
    except:
        pass
    id_count -= 1
    conn.close()


while True:
    conn, addr = socket_obj.accept()
    print('Connected to: ', addr)

    id_count += 1
    p = 0
    game_id = (id_count - 1) // 2

    if id_count % 2 == 1:
        games[game_id] = Game(game_id)
        print('Creating a new game!\n')

    else:
        games[game_id].ready = True
        p = 1

    start_new_thread(threaded_client, (conn, p, game_id))
