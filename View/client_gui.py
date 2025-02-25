'''
MIT License

Copyright (c) 2019 Harish

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
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
