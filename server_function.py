#Function to broadcast chat messages to all connected clients
def broadcast_data (sock, message):
    #Do not send the message to master socket and the client who has send us the message
    for socket in CONNECTION_LIST:
        if socket != server_socket and socket != sock :
            try :
                socket.send(message)
            except :
                # broken socket connection may be, chat client pressed ctrl+c for example
                socket.close()
                CONNECTION_LIST.remove(socket)

def send_message(sock,groupID):
    for socket in CHAT_LIST[groupID]:
        message = ""
        try :
            socket.send(message)
        except :
            # broken socket connection may be, chat client pressed ctrl+c for example
            socket.close()
            CONNECTION_LIST.remove(socket)