'''
Student Name: Harish Harish
Student ID: 1001682418
'''

from tkinter import *
from tkinter import ttk
import threading
import socket
from Model.client import *

initial = ''  # variable to store contents of file
previous = ''  # variable to store contents of file


# Class for client GUI

class clientInterface(threading.Thread):

    def __init__(self, userName, connect):
        threading.Thread.__init__(self)
        self.userName = userName
        self.connection = connect
        self.start()

    def run(self) -> None:
        self.window = Tk()
        self.window.title(self.userName)

        self.textBox = Text(self.window, width=50, height=30)
        self.textBox.pack()

        ttk.Button(self.window, text='Close', command=self.closeWindow).pack()

        self.window.mainloop()

    def addToTextBox(self, message):
        self.textBox.insert('end', message)

    def closeWindow(self):
        self.connection.sendDisconnection()
        self.window.destroy()


# Class for select user GUI

class selectUserUI(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        self.start()

    def run(self) -> None:
        self.master = Tk()
        self.userOptionLabel = ttk.Label(self.master, text='Select User')
        self.userOptionLabel.grid(row=0, column=0, columnspan=2)

        self.userAButton = ttk.Button(self.master, text='A', command=lambda: selectUserCallBack('A', self))
        self.userAButton.grid(row=1, column=0)

        self.userBButton = ttk.Button(self.master, text='B', command=lambda: selectUserCallBack('B', self))
        self.userBButton.grid(row=1, column=1)

        exitButton = ttk.Button(self.master, text='Exit', command=self.closeWindow)
        exitButton.grid(row=2, column=1)

        self.master.mainloop()

    def closeWindow(self):
        self.master.destroy()
        endClientPrcess()

    def displayMessageBox(self):
        messagebox.showerror(title='Error', message='This user name is taken.Please select another user')


def selectUserCallBack(userName, master):
    Client(userName, master)


def main():
    fp = open('A.txt', 'r')
    client_gui.initial = fp.read()
    client_gui.previous = initial
    fp.close()
    selectUserUI()


def endClientPrcess():
    exit(0)


if __name__ == '__main__': main()
