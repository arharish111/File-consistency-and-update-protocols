'''
Student Name: Harish Harish
Student ID: 1001682418
'''
from tkinter import *
from tkinter import ttk
from Model.server import *

# For server GUI
class serverUI(threading.Thread):

    def __init__(self):

        threading.Thread.__init__(self)
        self.start()

    def run(self) -> None:
        self.window = Tk()
        self.window.title('Server')

        self.textBox = Text(self.window, width=50, height=30)  # text box to display messages
        self.textBox.pack()

        ttk.Button(self.window, text='Close', command=self.closeWindow).pack()

        self.window.mainloop()

    def addToTextBox(self, message):

        self.textBox.insert('end', message)

    def closeWindow(self):
        self.window.destroy()

def main():
    gui = serverUI()
    serverMain = Server()
    serverMain.startServer(gui)

if __name__ == '__main__':main()

