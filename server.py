#https://github.com/jangjiin/hw2
import select, socket, sys, pdb
from chat_util import Hall, Room, Player
import chat_util

READ_BUFFER = 4096

host = sys.argv[1] if len(sys.argv) >= 2 else ''
listen_sock = chat_util.create_socket((host, chat_util.PORT))

hall = Hall()
connection_list = []
connection_list.append(listen_sock)





while True:
    # Player.fileno()
    read_players, write_players, error_sockets = select.select(connection_list, [], [])
    for player in read_players:
        if player is listen_sock: # new connection, player is a socket
            new_socket, add = player.accept()
            new_player = Player(new_socket)
            connection_list.append(new_player)
            hall.welcome_new(new_player)
            #hall.welcome_newpasswd(new_player)

        else: # new message
            try:
                msg = player.socket.recv(READ_BUFFER)
            except ConnectionResetError: #by wjj handle user quit
                player.socket.close()
                connection_list.remove(player)
                continue
            if msg:
                msg = msg.decode().lower()
                hall.handle_msg(player, msg)
            else:
                player.socket.close()
                connection_list.remove(player)

    for sock in error_sockets: # close error sockets
        sock.close()
        connection_list.remove(sock)
