from PyQt5.QtWidgets import *
from PyQt5.uic import *
from sense_hat import SenseHat
from time import sleep

class MyApp(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi("hi.ui",self)
        self.main()
        
    def main(self):
        self.sense=SenseHat()

    def go(self):
        #self.sense.show_message(self.lineEdit.text())
        for y in range(8):
            for x in range(8):
                self.sense.set_pixel(x,y,200,192,188)
                sleep(0.1)
        self.sense.clear()
        

app=QApplication([])
win=MyApp()
win.show()
app.exec()