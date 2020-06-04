from PyQt5.QtWidgets import *
from PyQt5.uic import *
from PyQt5.QtCore import *
import time

class MyThread(QThread):
    mySignal = pyqtSignal(int, int)
    def __init__(self):
        super().__init__()
        self.isRun = False
        
    def run(self):
        for i in range(10):
            for x in range(0, 101):
                self.mySignal.emit(i, x)
                time.sleep(0.001)
        self.isRun = True


class MyApp(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi("thread.ui", self)
        
        self.pros = []
        for i in range(0, 10):
            self.pros.append(self.lay.itemAt(i).widget())
            self.pros[i].setValue(0)
        
        self.th = MyThread()
        self.th.mySignal.connect(self.setValue)
        
    def go(self):
        if self.th.isRun == False:
            self.th.isRun = True
            self.th.start()
            
    def setValue(self, i, x):
        self.pros[i].setValue(x)
        
                
app = QApplication([])
win = MyApp()
win.show()
app.exec()

