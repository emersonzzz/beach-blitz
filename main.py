'''
Project: beach-blitz-client
Description: Jump into action with this fun packed, beach themed game!
Contributors: Emerson Reinhard
'''

# imports

import dataset
import pygame
import socket
import threading

# vars

WIDTH = 750
HEIGHT = 500

greenidle = (47, 151, 95) 
greenhover = (73, 177, 121) 

green2idle = (102, 185, 63)
green2hover = (132, 180, 111)

blueidle = (95, 204, 161)
bluehover = (135, 201, 176)

redidle = (211, 101, 75)
redhover = (209, 133, 115)

smoothwhite = (229, 229, 229)
toothpaste = (206, 206, 206)
darkgrey = (26, 26, 26)
darkgrey1 = (52, 52, 52)
darkgrey2 = (78, 78, 78)
errorred = (235, 64, 52)
orchidpurple = (176, 105, 238)

accounts_db = dataset.connect('sqlite:///accounts.db')

credentials_db = accounts_db['credentials']
cosmetics_db = accounts_db['cosmetics']
options_db = accounts_db['options']

HEADER = 64
PORT = 5555
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = '!DISCONNECT'
TESTING_SERVER = '192.168.1.66'
ADDR = (TESTING_SERVER, PORT)
CONNECTED = False

# code

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

class serverSide():
    def connect():
        client.connect(ADDR)
        CONNECTED = True

    def disconnect():
        serverSide.send('!DISCONNECT')
        CONNECTED = False
    
    def send(msg):
        message = msg.encode(FORMAT)
        msg_length = len(message)
        send_length = str(msg_length).encode(FORMAT)
        send_length += b' ' * (HEADER - len(send_length))
        client.send(send_length)
        client.send(message)
        print(client.recv(2048).decode(FORMAT))

    def checkforactiveclient():
        activeacc = credentials_db.find_one(loggedin='True')
        print(activeacc)
        if activeacc == None:
            return None
        else:
            username = list(activeacc.values())[1]
            return username

class uiHandler():
    def loadwindow():
        pygame.init()
        screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
        uiHandler.loadassets(screen)

    def loadassets(screen):
        rawmessage = 'hello world'
        while True:
            WIDTH = pygame.display.Info().current_w
            HEIGHT = pygame.display.Info().current_h
            screen.fill((26, 26, 26))

            '''header'''

            pygame.font.init()
            headerfont = pygame.font.Font(r'assets\gfx\mainfont.otf', 25)
            header = headerfont.render('what would you like to say to the server?', True, (229, 229, 229))
            headerrect = header.get_rect()
            headerrect.top = 15
            headerrect.left = 15
            screen.blit(header, headerrect)

            '''text box - background'''

            textboxbg = pygame.Rect(15, 66, 720, 66)
            pygame.draw.rect(screen, (52, 52, 52), textboxbg, border_radius=7)

            '''text box - text'''

            message = headerfont.render(rawmessage, True, (229, 229, 229))
            msgrect = message.get_rect()
            msgrect.top = 81
            msgrect.left = 35
            screen.blit(message, msgrect)

            '''send button - send'''

            pygame.display.update()
            for eve in pygame.event.get():
                if eve.type == pygame.QUIT:
                    serverSide.disconnect()
                    pygame.quit()
                    quit()
                if eve.type == pygame.KEYDOWN:
                    if eve.key == pygame.K_BACKSPACE:
                        rawmessage = rawmessage[:-1]
                    elif eve.key == pygame.K_RETURN:
                        serverSide.send(rawmessage)
                        rawmessage = ''
                    else:
                        rawmessage += eve.unicode

# console

serverSide.connect()
uiHandler.loadwindow()