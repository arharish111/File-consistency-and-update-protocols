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

