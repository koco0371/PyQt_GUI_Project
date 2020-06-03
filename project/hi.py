from PyQt5.QtWidgets import *
from PyQt5.uic import *
import hashlib

class MyApp(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi("des2.ui",self)
        
    def bye(self):
        self.close()
    
    def check(self):
        str1=self.textBox1.text()
        str2=self.textBox2.text()
        hashCode1 = hashlib.sha256(str1.encode()).hexdigest()
        hashCode2 = hashlib.sha256(str2.encode()).hexdigest()
        
        result=int(hashCode1,16)+ int(hashCode2,16)
        result=result+(777*self.spinBox.value())
        result=result%101
        
        msg=QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setWindowTitle("Warning Warning")
        msg.setText("By NASA, " + str(result)+ \
                    "% possibility Couple")
        msg.exec()
    
    def clear(self):
        self.textBox1.setText("")
        self.textBox2.setText("")
        self.spinBox.setValue(0)

app=QApplication([])
win=MyApp()
win.show()
app.exec()
