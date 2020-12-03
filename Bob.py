# text_receive_client.py

import socket
import select
import time
from cryptography.fernet import Fernet

HOST = 'localhost'
PORT = 11111
ACK_TEXT = "Text Received"
ENC_KEY = input("Welcome Bob, Please enter the pre-shared key: ")
alphabet = "abcdefghijklmnopqrstuvwxyz"

def main():
    # instantiate a socket object
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print('socket instantiated')

    # connect the socket
    connectionSuccessful = False
    while not connectionSuccessful:
        try:
            sock.connect((HOST, PORT))    # Note: if execution gets here before the server starts up, this line will cause an error, hence the try-except
            print('socket connected')
            connectionSuccessful = True
        except:
            pass
        # end try
    # end while



    socks = [sock]
    while True:
        readySocks, _, _ = select.select(socks, [], [], 5)
        for sock in readySocks:
            message = receiveTextViaSocket(sock)
            print('received: ' + str(message))
            dec_mess = vigenere_dec(message)
            print("Decrypted to: " + dec_mess)

        # end for
    # end while
# end function



def receiveTextViaSocket(sock):
    """
    Method that will recieve a message via the socket
    :param sock: Put the connection that you want to send the message along
    :return: recieved message
    """
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

def sendTextViaSocket(message, sock):
    """
    This method allows you to send a message over a socket connection
    :param message: messsage string
    :param sock: the socket to send it over. type=Socket
    """
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


def vigenere_enc(message):
    """
    This will encrypt the raw message. This requires a key to input in the ENC_KEY global variable.
    :param message: plain text string
    :return: encrypted string
    """
    enc_string = ""

    # Takes string from user
    input_string = message
    input_string = input_string.lower()

    # Lengths of input_string
    string_length = len(input_string)

    # Expands the encryption key to make it longer than the inputted string
    expanded_key = ENC_KEY
    expanded_key_length = len(expanded_key)
    while expanded_key_length < string_length:
        # Adds another repetition of the encryption key
        expanded_key = expanded_key + ENC_KEY
        expanded_key_length = len(expanded_key)

    key_position = 0

    for letter in input_string:
        if letter in alphabet:
            # cycles through each letter to find it’s numeric position in the alphabet
            position = alphabet.find(letter)
            # moves along key and finds the characters value
            key_character = expanded_key[key_position]
            key_character_position = alphabet.find(key_character)
            key_position = key_position + 1
            # changes the original of the input string character
            new_position = position + key_character_position
            if new_position >= 26:
                new_position = new_position - 26
            new_character = alphabet[new_position]
            enc_string = enc_string + new_character
        else:
            enc_string = enc_string + letter
    return(enc_string)


def vigenere_dec(message):
    """
    This will encrypt the raw message. This requires a key to input in the ENC_KEY global variable.
    :param message: encrypted message
    :return: plain-text message
    """

    dec_string = ""

    # Takes string from user
    input_string = message
    input_string = input_string.lower()

    # Lengths of input_string
    string_length = len(input_string)

    # Expands the encryption key to make it longer than the inputted string
    expanded_key = ENC_KEY
    expanded_key_length = len(expanded_key)

    while expanded_key_length < string_length:
        # Adds another repetition of the encryption key
        expanded_key = expanded_key + ENC_KEY
        expanded_key_length = len(expanded_key)

    key_position = 0

    for letter in input_string:
        if letter in alphabet:
            # cycles through each letter to find it's numeric position in the alphabet
            position = alphabet.find(letter)
            # moves along key and finds the characters value
            key_character = expanded_key[key_position]
            key_character_position = alphabet.find(key_character)
            key_position = key_position + 1
            # changes the original of the input string character
            new_position = position - key_character_position
            if new_position >= 26:
                new_position = new_position + 26
            new_character = alphabet[new_position]
            dec_string = dec_string + new_character
        else:
            dec_string = dec_string + letter
    return(dec_string)


if __name__ == '__main__':
    main()