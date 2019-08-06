'''
Student Name: Harish Harish
Student ID: 1001682418
'''

import socket
import threading
import json
from View.server_gui import *

userDict = {'A': 0, 'B': 0}  # to store connected users
aList = []  # to store messages for client A
bList = []  # to store messages for client B
connDict = {}  # to store connection objects

# To start the server
class Server:

    def startServer(self, interface):

        self.interface = interface
        host = 'localhost'  # setting host
        port = 8888  # setting port number
        self.soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.soc.bind((host, port))  # binding to the set host and port number
        self.soc.listen(2)  # only listens to two clients
        while True:
            conn, addr = self.soc.accept()
            if conn:
                Connections(conn, self.interface)


# Threading sub-class to handle clients
class Connections(threading.Thread):

    def __init__(self, conn, interface):
        threading.Thread.__init__(self)
        self.conn = conn
        self.interface = interface
        self.headerLines = {'Server': str(self.conn.getsockname()), 'Status': 'True'}  # basic response dictionary
        self.start()  # threads gets started

    def run(self) -> None:
        while True:
            data = self.conn.recv(1024)  # receive data from the client
            if data:
                self.parseData(data)
                if self.headerLines['Status'] == 'True':
                    if self.headerLines['Message-Type'] == 'invalidation-notice' or \
                            self.headerLines['Message-Type'] == 'respond-send-data':
                        if self.headerLines['user'] == 'B':
                            self.conn = connDict['B']
                        else:
                            self.conn = connDict['A']
                        del self.headerLines['user']
                    try:
                        # print(self.conn)
                        self.conn.sendall(json.dumps(self.headerLines).encode('utf-8'))  # send data to the client
                    except Exception as e:
                        print(e.args[1])
                else:
                    if self.headerLines['Message-Type'] == 'disconnect':
                        break
                    else:
                        self.conn.sendall(json.dumps(self.headerLines).encode('utf-8'))
                        break

    # Function to parse the incoming message
    def parseData(self, data):
        parsedData = json.loads(data.decode('utf-8'))
        # self.interface.addToTextBox(parsedData)  # Display incoming message
        if parsedData['Message-Type'] == 'send-username':  # handle user connection

            self.headerLines['Message-Type'] = 'respond-username'

            if userDict[parsedData['User-Agent']]:
                self.headerLines['Status'] = 'False'
            else:
                userDict[parsedData['User-Agent']] = 1
                connDict[parsedData['User-Agent']] = self.conn
                self.interface.addToTextBox('Connected User: ' + parsedData['User-Agent'] + '\n')

        elif parsedData['Message-Type'] == 'send-data':  # handle modified data sent by the client

            self.interface.addToTextBox('File modified by client: ' + parsedData['User-Agent'] + ' with below data:' +
                                        '\n' + parsedData['data'])
            self.headerLines['Message-Type'] = 'invalidation-notice'
            # self.headerLines['data'] = parsedData['data']

            if parsedData['User-Agent'] == 'A':
                self.headerLines['user'] = 'B'
                bList.append(parsedData['data'])
            else:
                self.headerLines['user'] = 'A'
                aList.append(parsedData['data'])

        elif parsedData['Message-Type'] == 'request-modified-data':  # handle request for modified data

            self.headerLines['Message-Type'] = 'send-modified-data'
            if parsedData['User-Agent'] == 'A':
                self.headerLines['data'] = aList.pop(0)
                aList.clear()
            else:
                self.headerLines['data'] = bList.pop(0)
                bList.clear()

        elif parsedData['Message-Type'] == 'respond-invalidation':  # handle rejection of modified data

            self.headerLines['Message-Type'] = 'respond-send-data'

            if parsedData['User-Agent'] == 'A':
                self.headerLines['user'] = 'B'
            else:
                self.headerLines['user'] = 'A'

        elif parsedData['Message-Type'] == 'user-disconnected':  # handle user disconnection

            self.headerLines['Status'] = 'False'
            self.headerLines['Message-Type'] = 'disconnect'
            userDict[parsedData['User-Agent']] = 0
