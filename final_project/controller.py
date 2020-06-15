from PyQt5.QtWidgets import *
from PyQt5.uic import *
from PyQt5 import QtSql
from PyQt5.QtCore import *

class MyApp(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi("hi.ui",self)
        
        self.db=QtSql.QSqlDatabase.addDatabase('QMYSQL')
        self.db.setHostName("3.34.124.67")
        self.db.setDatabaseName("15_8")
        self.db.setUserName("15_8")
        #self.db.setPassword("???")
        self.ok=self.db.open()
        print(self.ok)
        
        self.timer=QTimer()
        self.timer.setInterval(10)
        self.timer.timeout.connect(self.pollingQuery)
        self.timer.start()
        
    def pollingQuery(self):
        self.query=QtSql.QSqlQuery("select * from command2")
        self.text.clear()
        while(self.query.next()):
            self.record=self.query.record()
            str="%s | %10s | %10s | %4d" % (self.record.value(0).toString(),self.record.value(1), self.record.value(2),self.record.value(3))
            self.text.appendPlainText(str)
            
    def commandQuery(self,cmd,arg):
        self.query.prepare("insert into command2 (time, cmd_string, arg_string, is_finish) values (:time, :cmd, :arg, :finish)");
        time=QDateTime().currentDateTime()
        self.query.bindValue(":time",time)
        self.query.bindValue(":cmd",cmd)
        self.query.bindValue(":arg",arg)
        self.query.bindValue(":finish",0)
        self.query.exec()
        
    def clickedRight(self):
        print("right")
        self.commandQuery("right","1 sec")
    
    def clickedLeft(self):
        print("left")
        self.commandQuery("left", "1 sec")
    
    def clickedGo(self):
        print("go")
        self.commandQuery("go","1 sec")
    
    def clickedBack(self):
        print("back")
        self.commandQuery("back","1 sec")
    
    def clickedMid(self):
        print("mid")
        self.commandQuery("mid", "1 sec")
        
        
app=QApplication([])
win=MyApp()
win.show()
app.exec()