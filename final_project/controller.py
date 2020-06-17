from PyQt5.QtWidgets import *
from PyQt5.uic import *
from PyQt5 import QtSql
from PyQt5.QtCore import *
from time import sleep


         

class MyApp(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi("hi.ui",self)
        
        
        self.speed=80
        self.state=False
        self.db=QtSql.QSqlDatabase.addDatabase('QMYSQL')
        self.db.setHostName("3.34.124.67")
        self.db.setDatabaseName("15_8")
        self.db.setUserName("15_8")
        self.db.setPassword("1234")
        self.ok=self.db.open()
        self.setValue(0)
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
            
        self. query=QtSql.QSqlQuery("select * from sensing2 order by time desc limit 15")
        str=""
        while (self.query.next()) :
            self.record=self.query.record()
            str+="%s | %10s | %10s | %10s \n"%(self.record.value(0).toString(),self.record.value(1), self.record.value(2), self.record.value(3))
        
        self.text2.setPlainText(str)
            
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
        self.setValue(self.speed)
        self.state=True
        self.commandQuery("go","1 sec")
    
    def clickedBack(self):
        print("back")
        self.state=True
        self.setValue(self.speed)
        self.commandQuery("back","1 sec")
    
    def clickedMid(self):
        print("center")
        self.commandQuery("center", "1 sec")
        
    def clickedSpeedUp(self):
        print("speeeeed UP!!")
        self.speed+=20
        if self.state:
            self.setValue(self.speed)
        self.commandQuery("speedUp","1 sec")
    
    def clickedStop(self):
        print("stop")
        self.setValue(0)
        self.state=False
        self.commandQuery("stop","1 sec")
        
    def clickedSpeedDown(self):
        print("speeeeed DOWN!!")
        self.speed-=20
        if self.state:
            self.setValue(self.speed)
        self.commandQuery("speedDown","1 sec")
        
        
    def setValue(self,i):
        self.speedBar.setValue(i)
    
    
        
        
app=QApplication([])
win=MyApp()
win.show()
app.exec()