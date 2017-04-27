#!/usr/bin/env python

"""

Reference for async socket with 'select' module: 
    http://www.binarytides.com/code-chat-application-server-client-sockets-python/

"""

import socket, select
from pymongo import MongoClient, errors
import pprint # For print mongo object // pprint.pprint(post)   
from bson.json_util import dumps # For converting mongo object to JSON string
import ast # For converting JSOn string to dict
from datetime import datetime # For add date time in mongodb

###########################################################
############## Variables and Configuration ################
###########################################################

# List to keep track of socket descriptors
"""
CONNECTION_LIST = [
    'Hodor': {
        'sock': sock
    }
]

"""
CONNECTION_LIST = []
RECV_BUFFER = 4096 # Advisable to keep it as an exponent of 2
PORT = 8888

# MongoDB Config
DB_USERNAME = 'XXX'
DB_PASSWORD = 'XXX'
DB_URL = 'XXX'


try:
    mongo_client = MongoClient(DB_URL)
    #mongo_client.server_info() # Will be checked for exception
    db = mongo_client['ezzen']
    users = db.users

    ## !! There is no error now even mongo server is inconnect, and  I don't know why !!

#except errors.ServerSelectionTimeoutError:
except:
    print '[-] There is an error on connecting to Database(MongoDB)'
    exit(1)

##pprint.pprint(users.find({'username':'hodor'}))
#pprint.pprint(user)

# Create Socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# this has no effect, why ?
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

#List of Client in App
"""
CLIENT_LIST = [{
    id: _id,
    name: _name,
    groups:[],
}]
"""

CLIENT_LIST = [{
    'id': 0,
    'name': 'dummy',
    'groups':[],
}]

# List of Group in App
"""
GROUP_LIST = [{
    id: _id,

}]
"""
GROUP_LIST =  []

hello_text = """

        $$$$$$$$\ $$$$$$$$\ $$$$$$$$\ $$$$$$$$\ $$\   $$\ 
        $$  _____|\____$$  |\____$$  |$$  _____|$$$\  $$ |
        $$ |          $$  /     $$  / $$ |      $$$$\ $$ |
        $$$$$\       $$  /     $$  /  $$$$$\    $$ $$\$$ |
        $$  __|     $$  /     $$  /   $$  __|   $$ \$$$$ |
        $$ |       $$  /     $$  /    $$ |      $$ |\$$$ |
        $$$$$$$$\ $$$$$$$$\ $$$$$$$$\ $$$$$$$$\ $$ | \$$ |
        \________|\________|\________|\________|\__|  \__|

[*] Computer Engineering, Chulalongkorn University
[*] Disitributed Essential Mini Project 2016 Term 2 by Ezzen                                                                   
"""

#########################################
############### Funcitons ###############
#########################################

def mongo_to_dict(mongo_object):
    """
    For converting Mongo Object to dict
    """
    python_dict = ast.literal_eval(dumps(mongo_object))
    return python_dict

def broadcast_data (sock, message):
    """
    Function to broadcast chat messages to all connected clients
    """
    #Do not send the message to master socket and the client who has send us the message
    for socket in CONNECTION_LIST:
        if socket != server_socket and socket != sock :
            try :
                socket.send(message)
            except :
                # broken socket connection may be, chat client pressed ctrl+c for example
                socket.close()
                CONNECTION_LIST.remove(socket)

def send_message(groupID, clientID, clientMessage, timestamp): # Unfinish
    """
    Send Message To all client in the group specifies by groupID
    """
    for socket in GROUP_LIST[groupID]:
        message = ''
        try :
            socket.send(message)
        except :
            # broken socket connection may be, chat client pressed ctrl+c for example
            socket.close()
            CONNECTION_LIST.remove(socket)

def exit_group(clientID, groupID):  # Unfinish
    #CLIENT_LIST[clientID][]
    pass

def join_group(clientID, groupID):  # Unfinish
    pass

def leave_group(clientID, groupID):  # Unfinish
    pass

def load_unread_message(sock, clientID, groupID, lastMessageNo):  # Unfinish
    pass

def login(username, password):  # Unfinish

    if(True):
        print '[INFO] %s has logined' % clientName

def signup(sock, username, password):  # Unfinish
    try:# Check for Exist User
        user = users.find({'username':username})[0]
        print 'User Exist :('
        sock.send('R FAIL\n')
    except IndexError: # User not Found, we can signup
        print 'Success :)'
        users.insert({
            'id':0,
            'username':username,
            'password':password,
            'date':datetime.now()})
        sock.send('R SUCC\n')
        print '[INFO] %s has signed up' % username

def disconnect(clientID):
    pass

############################################

def main():
    # Just some greeting with Admin & Developer
    #print "\n"*100
    print hello_text
    
    server_socket.bind(("0.0.0.0", PORT))
    # Listen For 10 Client
    server_socket.listen(10)
 
    # Add server socket to the list of readable connections
    CONNECTION_LIST.append(server_socket)
 
    print "[*] Chat server started on port " + str(PORT)
 
    while 1:
        # Get the list sockets which are ready to be read through select
        read_sockets,write_sockets,error_sockets = select.select(CONNECTION_LIST,[],[])
 
        for sock in read_sockets:
            #New connection
            if sock == server_socket:
                # Handle the case in which there is a new connection recieved through server_socket
                sockfd, addr = server_socket.accept()
                CONNECTION_LIST.append(sockfd)
                print "Client (%s, %s) connected" % addr

                broadcast_data(sockfd, "[%s:%s] entered room\n" % addr)

            #Some incoming message from a client
            else:
                # Data recieved from client, process it
                try:
                    #In Windows, sometimes when a TCP program closes abruptly,
                    # a "Connection reset by peer" exception will be thrown
                    data = sock.recv(RECV_BUFFER)
                    if data:
                        broadcast_data(sock, "\r" + '<' + str(sock.getpeername()) + '> ' + data)                
                    
                    # Assign Paramter From Clinet Message
                    msg = data.split()
                    protocol = msg[0]
                    
                    ################################
                    ###### Protocol Selection ######
                    ################################

                    if protocol == 'M' : # Unfinish
                        groupID = msg[1]
                        clientID = msg[2]
                        clientMessage = msg[3]
                        timestamp = msg[4]
                        send_message(groupID, clientID, clientMessage, timestamp)
                    elif protocol == 'C':
                        action = msg[1]
                        if action == 'EXTG':
                            clientID = msg[2]
                            groupID = msg[3]
                            exit_group(clientID, groupID)
                            clientName = 'Hodor'#CLIENT_LIST[clientID]
                            groupName = 'Team Jon' #GROUP_LIST[groupID]
                            print '[INFO] {0} exits {1}'.format(clientName, groupName)
                        elif action == 'JOIN':
                            clientID = msg[2]
                            groupID = msg[3]
                            joing_group(clientID, groupID)
                            clientName = 'Hodor'#CLIENT_LIST[clientID]
                            groupName = 'Team Jon' #GROUP_LIST[groupID]
                            print '[INFO] {0} joins {1}'.format(clientName, groupName)
                        elif action == 'LEVG':
                            clientID = msg[2]
                            groupID = msg[3]
                            leave_group(clientID, groupID)
                        elif action == 'LUNR':
                            clientID = msg[2]
                            groupID = msg[3]
                            lastMessageNo = msg[4]
                            load_unread_message(sock, clientID, groupID, lastMessageNo)
                        elif action == 'LOGN': # Unfinish
                            username = msg[2]
                            password = msg[3]
                            login(username, password)
                            sock.send('Hello Ping'+'\n')
                        elif action == 'SIGN': # Unfinish
                            username = msg[2]
                            password = msg[3]
                            signup(sock, username, password)
                        elif action == 'DISC':
                            clientID = msg[2]
                            disconnect(clientID)
                            print '[INFO] %s exits program' % clientID
                        else:
                            sock.send("Unknown Action\n")
                    else:
                        sock.send("Unknown Protocol\n")

                except:
                    broadcast_data(sock, "Client (%s, %s) is offline" % addr)
                    print 'Client (%s, %s) is offline' % addr
                    sock.close()
                    CONNECTION_LIST.remove(sock)
                    continue

    server_socket.close()

if __name__ =="__main__":
    main()