'''
Student Name: Harish Harish
Student ID: 1001682418
'''
import threading
import socket
import json
import time
from tkinter import messagebox
from View.client_gui import *
from View import client_gui

class Client(threading.Thread):

    def __init__(self, userName, mainWindow):
        threading.Thread.__init__(self)
        self.userName = userName
        self.mainUI = mainWindow
        self.host = 'localhost'
        self.port = 8888
        self.sendUserNameMessage = 'send-username'
        self.start()

    def run(self) -> None:

        try:
            self.soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.soc.connect((self.host, self.port))  # making connection with the server
        except Exception as e:
            print(e.args[1])
        else:
            self.hostNameWithPort = str(self.soc.getsockname())
            self.headerLines = {'data': self.userName,
                                'Host': self.hostNameWithPort,
                                'User-Agent': self.userName,
                                'Message-Type': self.sendUserNameMessage
                                }
            self.sendUserName()

# To send user name to the server

    def sendUserName(self):

        handleInvalidationNotice(self)
        self.sendMessageToServer()

# To send messages to the server

    def sendMessageToServer(self):

        jsonMessage = json.dumps(self.headerLines)
        try:
            self.soc.sendall(jsonMessage.encode('utf-8'))  # sending  message to the server
            if self.headerLines['Message-Type'] == 'user-disconnected':
                self.soc.close()
        except Exception as e:
            print(e.args[1])

# Parse incoming message and call function based on message type

    def parseIncomingMessageFromServer(self, data):

        self.parsedData = json.loads(data.decode('utf-8'))
        if self.parsedData['Message-Type'] == 'invalidation-notice':
            self.handleInvalidationNotice()
        elif self.parsedData['Message-Type'] == 'respond-username':
            self.handleRespondUserName()
        elif self.parsedData['Message-Type'] == 'respond-send-data':
            self.handleRespondSendData()
        elif self.parsedData['Message-Type'] == 'send-modified-data':
            self.handleSendModifiedData()

# To handle modified file

    def handleSendModifiedData(self):

        message = 'Would you like accept below data' + '\n' + self.parsedData['data']
        self.headerLines['Message-Type'] = 'respond-invalidation'
        if self.userName == 'A':
            if messagebox.askyesno('Data modified by B', message):
                client_gui.previous = self.parsedData['data']
                fp = open('A.txt', 'w')
                fp.write(self.parsedData['data'])
                fp.close()
                self.headerLines['Status'] = 'True'
            else:
                self.headerLines['Status'] = 'False'
        else:
            if messagebox.askyesno('Data modified by A', message):
                client_gui.previous = self.parsedData['data']
                fp = open('B.txt', 'w')
                fp.write(self.parsedData['data'])
                fp.close()
                self.headerLines['Status'] = 'True'
            else:
                self.headerLines['Status'] = 'False'
        if self.headerLines['Status'] == 'False':
            self.sendMessageToServer()

# To handle user acceptation or rejection by the server

    def handleRespondUserName(self):
        if self.parsedData['Status'] == 'True':
            self.userUI = clientInterface(self.userName, self)
            fileHandling(self)
        else:
            self.soc.close()
            self.mainUI.displayMessageBox()

# To handle invalidation notice sent by the server

    def handleInvalidationNotice(self):

        self.headerLines['Message-Type'] = 'request-modified-data'
        self.sendMessageToServer()

# To handle rejection of modified data

    def handleRespondSendData(self):

        if self.userName == 'A':
            fp = open('A.txt', 'w')
            fp.write(client_gui.previous)
            client_gui.initial = client_gui.previous
            fp.close()
            messagebox.showinfo('Rejection', 'Client B has rejected the update. Reverted local changes')
        else:
            fp = open('B.txt', 'w')
            fp.write(client_gui.previous)
            client_gui.initial = client_gui.previous
            fp.close()
            messagebox.showinfo('Rejection', 'Client A has rejected the update. Reverted local changes')

# To handle disconnection of client

    def sendDisconnection(self):

        self.headerLines['Message-Type'] = 'user-disconnected'
        self.sendMessageToServer()

# Class to handle file modifications

class fileHandling(threading.Thread):

    def __init__(self, cli):
        threading.Thread.__init__(self)
        self.clientIns = cli
        self.start()

    def run(self) -> None:
        if self.clientIns.userName == 'A':
            while 1:
                fp = open('A.txt', 'r')
                data = fp.read()
                if client_gui.initial != data:
                    client_gui.previous = client_gui.initial
                    client_gui.initial = data
                    self.clientIns.userUI.addToTextBox('File modified with below data:' + '\n' + data + '\n')
                    self.clientIns.headerLines['Message-Type'] = 'send-data'
                    self.clientIns.headerLines['data'] = data
                    self.clientIns.sendMessageToServer()
                fp.close()
                time.sleep(5)
        else:
            while 1:
                fp = open('B.txt', 'r')
                data = fp.read()
                if client_gui.initial != data:
                    client_gui.previous = client_gui.initial
                    client_gui.initial = data
                    self.clientIns.userUI.addToTextBox('File modified with below data:' + '\n' + data + '\n')
                    self.clientIns.headerLines['Message-Type'] = 'send-data'
                    self.clientIns.headerLines['data'] = data
                    self.clientIns.sendMessageToServer()
                fp.close()
                time.sleep(5)

# class to handle response from the server

class handleInvalidationNotice(threading.Thread):

    def __init__(self, soc):
        threading.Thread.__init__(self)
        self.serverConnection = soc
        self.start()

    def run(self) -> None:
        while True:
            try:
                invalidData = self.serverConnection.soc.recv(1024)
            except Exception as e:
                break
            else:
                if invalidData:
                    self.serverConnection.parseIncomingMessageFromServer(invalidData)
