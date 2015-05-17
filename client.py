import socket
import select
import sys
import os
from threading import Thread
from chat_util import Room, Hall, Player
import chat_util
#from queue 
import queue
from getpass import getpass

READ_BUFFER = 4096
def prompt():
    print('>', end=' ', flush = True)

class ChatClient:
    msg_prefix = ''
    
    def __init__(self, host, port, nickname):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) #from chat_client
        self.socket.connect((host, port))
        #self.input = self.socket.makefile('rb', 0)
        self.output = self.socket.makefile('wb', 0)

        #Send the given nickname to the server.
        """"
        authenticationDemand = self.input.readline().decode('utf-8')
        if not authenticationDemand.startswith("Who are you?"):
            raise Exception ("This doesn't seem to be a Python Chat Server.")
        self.output.write((nickname + '\r\n').encode('utf-8'))
        response = self.input.readline().strip().decode('utf-8')
        if not response.startswith("Hello"):
            raise Exception (response)
        print(response)

        #Start out by printing out the list of members.
        self.output.write(('/names\r\n').encode('utf-8'))
        print("Currently in the chat room:", self.input.readline().decode('utf-8').strip())
        """
        
        self.run()

    def run(self):
        """Start a separate thread to gather the input from the
        keyboard even as we wait for messages to come over the
        network. This makes it possible for the user to simultaneously
        send and receive chat text."""
        
        propagateStandardInput = self.PropagateStandardInput(self.output)
        propagateStandardInput.start()

        #Read from the network and print everything received to standard
        #output. Once data stops coming in from the network, it means
        #we've disconnected.
        inputText = True
        while inputText:
            #inputText = self.input.readline()#.decode('utf-8')
            
            inputText = self.socket.recv(READ_BUFFER)
            if inputText:
                #print (inputText.strip())
               
                if inputText == chat_util.QUIT_STRING.encode():
                    sys.stdout.write('Bye\n')
                    sys.exit(2)
                else:
                    sys.stdout.write(inputText.decode())
                    
                    if 'Please tell us your name' in inputText.decode():
                        
                        msg_prefix = 'name: ' # identifier for name
                    elif 'Please input your password' in inputText.decode():
                        msg_prefix = 'passwd: ' # identifier for name
                    elif 'Do you want to talk to' in inputText.decode():
                        msg = inputText.decode()
                        msg_prefix = 'Yes_No: ' + msg.split()[6] + ' ' + msg.split()[9]+ ' ' # identifier for name
                        
                    else:
                        msg_prefix = ''
                    
                    
                    #with q.mutex: #clear the queue
                    #    q.queue.clear()
                    #print ("q.put:", msg_prefix)
                    q.put(msg_prefix)
                    prompt()
                    
                #stack.push(1)
            else:
                print("Server down!")
                sys.exit(2)            
                
        propagateStandardInput.done = True

    class PropagateStandardInput(Thread):
        """A class that mirrors standard input to the chat server
        until it's told to stop."""
        
        def __init__(self, output):
            """Make this thread a daemon thread, so that if the Python
            interpreter needs to quit it won't be held up waiting for this
            thread to die."""
            Thread.__init__(self)
            self.setDaemon(True)
            self.output = output
            self.done = False

        def run(self):
           
            "Echo standard input to the chat server until told to stop."
            #msg_prefix = ''
            while not self.done:
                #msg = msg_prefix + sys.stdin.readline()
                #server_connection.sendall(msg.encode())
                
                msg_prefix=q.get()
                #print ("q.get:", msg_prefix, file = sys.stderr)
                if "passwd:" in msg_prefix:
                    inputText = getpass()  
                else:
                    inputText = sys.stdin.readline() #.strip() #no need to decode when read from stdin
                
                if inputText:
                    
                    
                    inputText = msg_prefix + inputText
                    self.output.write(inputText.encode())
                    #print ("send:", inputText, file = sys.stderr)
                    #t_item = q.get()
                    #print (t_item)
                    with q.mutex: #clear the queue
                        q.queue.clear()

if __name__ == '__main__':
    import sys
    #See if the user has an OS-provided 'username' we can use as a default 
    #chat nickname. If not, they have to specify a nickname.
    try:
        import pwd
        defaultNickname = pwd.getpwuid(os.getuid())[0]
    except ImportError:
        defaultNickname = None

    if len(sys.argv) < 2:
        print("Usage: Python3 client.py [hostname]", file = sys.stderr)
        sys.exit(1)

    hostname = sys.argv[1]
    port = chat_util.PORT

    nickname = defaultNickname
    #q = Queue.LiFoQueue()
    q = queue.Queue() #LiFo
    ChatClient(hostname, port, nickname)

    
    
