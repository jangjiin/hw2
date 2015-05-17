#https://github.com/jangjiin/hw2

import socket, pdb

MAX_CLIENTS = 30
PORT = 22222
QUIT_STRING = '<$quit$>'


global accounts
accounts = {}
accounts["wjj"] = {
    'passwd': 'abc',
    'socket' : '',
    'message': ''
}
accounts["wjj1"] = {
    'passwd': 'bcd',
    'socket' : '',
    'message': ''
}
accounts["wjj2"] = {
    'passwd': 'cde',
    'socket' : '',
    'message': ''
}
global user_list
user_list=[]



def create_socket(address):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.setblocking(0)
    s.bind(address)
    s.listen(MAX_CLIENTS)
    print("Now listening at ", address)
    return s

class Hall:
    global accounts
    def __init__(self):
        global accounts
        self.rooms = {} # {room_name: Room}
        self.room_player_map = {} # {playerName: roomName}
   
    

    def welcome_new(self, new_player):
        new_player.socket.sendall(b'Welcome to Wechat.\rPlease tell us your name:\n')
    def welcome_newpasswd(self, new_player):
        new_player.socket.sendall(b'Please input your password:\n')
    def list_rooms(self, player):
        
        if len(self.rooms) == 0:
            msg = 'Oops, no active rooms currently. Create your own!\n' \
                + 'Use [<join> room_name] to create a room.\n'
            player.socket.sendall(msg.encode())
        else:
            msg = 'Listing current rooms...\n'
            for room in self.rooms:
                msg += room + ": " + str(len(self.rooms[room].players)) + " player(s)\n"
            player.socket.sendall(msg.encode())
    def list_user(self, player):
        msg="Online users:"
        print(user_list)
        for item in user_list:
            msg = msg + " " + item
        msg = msg + "\n"    
        """"for listplayer in self.room_player_map:
            msg= msg + " " + listplayer
            print(msg)
        """
        player.socket.sendall(msg.encode())
        
        
        #for k, v in self.room_player_map.items():
        #    #Display key and value.
        #        print(k, v)
        """rentItems = self.room_player_map.items()
        for rentItem in rentItems:
            print("user:", rentItem[0])
            print("room:", rentItem[1])
            print("")"""
    def handle_msg(self, player, msg):
        global accounts
        instructions = b'\n'\
            + b'[<list>] to list online users\n'\
            + b'[<talk>] to talk online users\n'\
            + b'[<listroom>] to list all rooms\n'\
            + b'[<join> room_name] to join/create/switch to a room\n' \
            + b'[<quit>] to quit\n' \
            + b'\n'

        print(player.name + " says: " + msg)
        if "name:" in msg:
        
            name = msg.split()[1]
            player.name = name
            print("New connection from:", player.name)
            self.welcome_newpasswd(player)
            #player.socket.sendall(instructions)
        elif "passwd:" in msg:
            mypasswd = msg.split()[1]

            #print("passwd:", mypasswd)
            
            if player.name in accounts and accounts[player.name]['passwd'] == mypasswd:
                msg = b'login success!\n'
                user_list.append(player.name)
                player.passwd = mypasswd
                player.socket.sendall(msg)
                player.socket.sendall(instructions)
                
                #login successful, and show the message when he offline
                accounts[player.name]['socket']=player.socket
                if len(accounts[player.name]['message'])>2:
                    player.socket.sendall(accounts[player.name]['message'].encode())
                    accounts[player.name]['message']=''
            else:
                #msg = b'username or password error!\n'
                #player.socket.sendall(msg)
                self.welcome_new(player)
                
            
        elif "Yes_No:" in msg:
            same_room = False
            if len(msg.split()) >= 3 and answer == 'y': # error check
                #room_name = msg.split()[1]
                
                answer = msg.split()[3]
                
                send_talk_room_name =msg.split()[2]
                
                receiver_name = msg.split()[1]
                if receiver_name in user_list:#檢查交談對象是否在線上
                    #送出邀請對方訊息
                    
                    
                    
                    if receiver_name in self.room_player_map:
                        room_name = self.room_player_map[receiver_name]
                        room_name1 = ''
                    else:
                        room_name = player.name + receiver_name
                        room_name1 =  receiver_name + player.name
                
                    if player.name in self.room_player_map: # switching?
                        if (self.room_player_map[player.name] == room_name) or (self.room_player_map[player.name] == room_name1) :
                            #msg = "You are already talking to " + receiver_name +"\n"
                            #player.socket.sendall(msg.encode()) #in room: ' + room_name.encode())
                            same_room = True
                            if self.room_player_map[player.name] == room_name1:
                                room_name = room_name1
                        else: # switch
                            old_room = self.room_player_map[player.name]
                            self.rooms[old_room].remove_player(player)
                    if not same_room:
                        if not room_name in self.rooms: # new room:
                            new_room = Room(room_name)
                            self.rooms[room_name] = new_room
                        self.rooms[room_name].players.append(player)
                        self.rooms[room_name].welcome_new(player)
                        self.room_player_map[player.name] = room_name
                        
                    #msg = "Do you want to talk to " + player.name + " in room " + room_name + "? (y/n)\n"
                    #accounts[receiver_name]['socket'].sendall(msg.encode())
                else:
                    msg= receiver_name + " not online! You can't talk to him(her).\n"
                    player.socket.sendall(msg.encode())
            else:
                player.socket.sendall(instructions)
                #old_room = self.room_player_map[receiver_name]
                #self.rooms[old_room].remove_player(player)
  
        elif "<send>" in msg:
            if len(msg.split()) > 2: # error check
                receiver_name = msg.split()[1]
                sendingmsg = player.name + " send " + receiver_name + ": "
                for i in range (2, len(msg.split())):
                    sendingmsg =sendingmsg + msg.split()[i] + " "
                sendingmsg = sendingmsg + "\n"
                if receiver_name in user_list:
                    accounts[receiver_name]['socket'].sendall(sendingmsg.encode())
                else:
                    if receiver_name in accounts:
                        accounts[receiver_name]['message'] = accounts[receiver_name]['message'] + sendingmsg
                    else:
                        sendingmsg= "No such user name!\n"
                #print ("aaaa:",accounts[receiver_name]['message'])
                player.socket.sendall(sendingmsg.encode())
            else:
                player.socket.sendall(instructions)
        elif "<broadcat>" in msg:
            if len(msg.split()) >= 2: # error check
                msg = player.name + " broadcat: " +msg.split()[1] + "\n"
                for item in user_list:
                    accounts[item]['socket'].sendall(msg.encode())
                    
        elif "<join>" in msg:
            same_room = False
            if len(msg.split()) >= 2: # error check
                room_name = msg.split()[1]
                if player.name in self.room_player_map: # switching?
                    if self.room_player_map[player.name] == room_name:
                        player.socket.sendall(b'You are already in room: ' + room_name.encode())
                        same_room = True
                    else: # switch
                        old_room = self.room_player_map[player.name]
                        self.rooms[old_room].remove_player(player)
                if not same_room:
                    if not room_name in self.rooms: # new room:
                        new_room = Room(room_name)
                        self.rooms[room_name] = new_room
                    self.rooms[room_name].players.append(player)
                    self.rooms[room_name].welcome_new(player)
                    #self.rooms[room_name].welcome_newpasswd(player)
                    self.room_player_map[player.name] = room_name
            else:
                player.socket.sendall(instructions)
        elif "<talk>" in msg:
            same_room = False
            if len(msg.split()) >= 2: # error check
                #room_name = msg.split()[1]

                receiver_name = msg.split()[1]
                if receiver_name in user_list:#檢查交談對象是否在線上
                    #送出邀請對方訊息
                    
                    
                    
                    if receiver_name in self.room_player_map:
                        room_name = self.room_player_map[receiver_name]
                        room_name1 = ''
                    else:
                        room_name = player.name + receiver_name
                        room_name1 =  receiver_name + player.name
                        msg = player.name + " want to talk to you!" + ", Type: \"<talk> " + player.name + "\" to join.\n"
                        accounts[receiver_name]['socket'].sendall(msg.encode())  
                
                    if player.name in self.room_player_map: # switching?
                        if (self.room_player_map[player.name] == room_name) or (self.room_player_map[player.name] == room_name1) :
                            msg = "You are already talking to " + receiver_name +"\n"
                            player.socket.sendall(msg.encode()) #in room: ' + room_name.encode())
                            same_room = True
                            if self.room_player_map[player.name] == room_name1:
                                room_name = room_name1
                        else: # switch
                            old_room = self.room_player_map[player.name]
                            self.rooms[old_room].remove_player(player)
                    if not same_room:
                        if not room_name in self.rooms: # new room:
                            new_room = Room(room_name)
                            self.rooms[room_name] = new_room
                        self.rooms[room_name].players.append(player)
                        self.rooms[room_name].welcome_new(player)
                        self.room_player_map[player.name] = room_name
                        
                      
                else:
                    msg= receiver_name + " not online! You can't talk to him(her).\n"
                    player.socket.sendall(msg.encode())
            else:
                player.socket.sendall(instructions)
        elif "<list>" in msg:
            #self.list_rooms(player) 
            self.list_user(player)
        elif "<listroom>" in msg:
            self.list_rooms(player) 
        elif "<manual>" in msg:
            player.socket.sendall(instructions)
        
        elif "<quit>" in msg:
            player.socket.sendall(QUIT_STRING.encode())
            self.remove_player(player)

        else:
            # check if in a room or not first
            if player.name in self.room_player_map:
                self.rooms[self.room_player_map[player.name]].broadcast(player, msg.encode())
            else:
                msg = 'You are currently not in any room! \n' \
                    + 'Use [<listroom>] to see available rooms! \n' \
                    + 'Use [<join> room_name] to join a room! \n'
                player.socket.sendall(msg.encode())
    
    def remove_player(self, player):
        global user_list
        if player.name in self.room_player_map:
            self.rooms[self.room_player_map[player.name]].remove_player(player)
            del self.room_player_map[player.name]
            #i=user_list.index(player.name)
            #del user_list[i]
            #print ("i::::::", i)
        user_list.remove(player.name)
        print("Player: " + player.name + " has left\n")

    
class Room:
    def __init__(self, name):
        self.players = [] # a list of sockets
        self.name = name

    def welcome_new(self, from_player):
        msg = "Room: " + self.name + " welcomes: " + from_player.name + '\n'
        for player in self.players:
            player.socket.sendall(msg.encode())
    
    def broadcast(self, from_player, msg):
        msg = from_player.name.encode() + b":" + msg
        for player in self.players:
            player.socket.sendall(msg)

    def remove_player(self, player):
        self.players.remove(player)
        leave_msg = player.name.encode() + b"has left the room\n"
        self.broadcast(player, leave_msg)

class Player:
    def __init__(self, socket, name = "new"):
        socket.setblocking(0)
        self.socket = socket
        self.name = name

    def fileno(self):
        return self.socket.fileno()
