# text_send_server.py

import socket
import select
import time
from cryptography.fernet import Fernet

HOST = 'localhost'
PORT = 11111
ACK_TEXT = 'Text Received'


def main():

    # instantiate a socket object
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print('socket instantiated')

    # bind the socket
    sock.bind((HOST, PORT))
    print('socket binded')

    # start the socket listening for two connections. The two clients Bob and Alice
    sock.listen(2)
    print('socket now listening')

    # accept the socket response from the clients, and get the connection objects

    conn, addr = sock.accept()
    conn2, addr2 = sock.accept()

    # Note: execution# on waits here until the client calls sock.connect()
    print('socket accepted, connection object')

    # Continued Loop For testing of the connection.
    Running = True
    while Running:
            messageAtoB = receiveTextViaSocket(conn)
            print('Recieved: ' + messageAtoB)
            forwardtoB(messageAtoB, conn2)

#            messageBtoA = receiveTextViaSocket(conn2)
#            print('Recieved: ' + messageBtoA)
#            forwardtoA(messageBtoA, conn2)

    # end while
# end function


def forwardtoA(message, conn):
    print("Forwarding on to A")
    sendTextViaSocket(message, conn)

def forwardtoB(message, conn):
    print("Forwarding on to B")
    sendTextViaSocket(message, conn)

def sendTextViaSocket(message, sock):
    # encode the text message
    encodedMessage = bytes(message, 'utf-8')

    # send the data via the socket to the server
    sock.sendall(encodedMessage)
    #sock.sendall(message)

    # receive acknowledgment from the server
    encodedAckText = sock.recv(1024) # size
    ackText = encodedAckText.decode('utf-8')

    # log if acknowledgment was successful
    if ackText == ACK_TEXT:
        print('server acknowledged reception of text')
    else:
        print('error: server has sent back ' + ackText)
    # end if
# end function

def receiveTextViaSocket(sock):
    # get the text via the socket
    encodedMessage = sock.recv(1024)

    # if we didn't get anything, log an error and bail
    if not encodedMessage:
        print('error: encodedMessage was received as None')
        return None
    # end if

    # decode the received text message
    message = encodedMessage.decode('utf-8')

    # now time to send the acknowledgement
    # encode the acknowledgement text
    encodedAckText = bytes(ACK_TEXT, 'utf-8')

    # send the encoded acknowledgement text
    sock.sendall(encodedAckText)

    return message

# end function


if __name__ == '__main__':
    main()