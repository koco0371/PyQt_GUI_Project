# day2_car.py

from Raspi_MotorHAT import Raspi_MotorHAT, Raspi_DCMotor
from PyQt5 import QtSql
from PyQt5.QtCore import *
from sense_hat import sense_hat
import time


mh = Raspi_MotorHAT(addr=0x6f)
dcMotor = mh.getMotor(3)    
speed = 125 
dcMotor.setSpeed(speed)

servo = mh._pwm
servo.setPWMFreq(60)
sense=SenseHat()
w=[150,150,150]
b=[0,0,255]
e=[0,0,0]
image=[]


def go():
    global image
    global sense
    image = [
        e, e, e, b, e, e, e, e,
        e, e, e, b, e, e, e, e,
        e, e, e, b, e, e, e, e,
        e, e, e, b, e, e, e, e,
        e, e, e, b, e, e, e, e,
        e, b, b, b, b, b, e, e,
        e, e, b, b, b, e, e, e,
        e, e, e, b, e, e, e, e
    ]
    sense.set_pixels(image)
    dcMotor.run(Raspi_MotorHAT.FORWARD)


def back():
    global image
    global sense
    image = [
        e, e, e, e, b, e, e, e,
        e, e, e, b, b, b, e, e,
        e, e, b, b, b, b, b, e,
        e, e, e, e, b, e, e, e,
        e, e, e, e, b, e, e, e,
        e, e, e, e, b, e, e, e,
        e, e, e, e, b, e, e, e,
        e, e, e, e, b, e, e, e
    ]
    dcMotor.run(Raspi_MotorHAT.BACKWARD)


def stop():
    dcMotor.run(Raspi_MotorHAT.RELEASE)


def speedUp():
    global speed
    speed = 255 if speed >= 235 else speed+20 
    dcMotor.setSpeed(speed)


def speedDown():
    global speed
    speed=0 if speed <= 20  else speed-20  
    dcMotor.setSpeed(speed)
    
def steer(angle=0): 
    if angle <= -60: 
        angle = -60
    if angle >= 60:
        angle = 60
    pulse_time = 200+(614-200)//180*(angle+90)  

    servo.setPWM(0,0,pulse_time)


def steer_right():
    global image
    global sense
    image = [
            e, e, e, e, e, e, e, e,
            e, e, e, e, e, e, e, e,
            e, e, b, e, e, e, e, e,
            e, b, b, e, e, e, e, e,
            b, b, b, b, b, b, b, b,
            e, b, b, e, e, e, e, e,
            e, e, b, e, e, e, e, e,
            e, e, e, e, e, e, e, e
    ]
    sense.set_pixels(image)
    steer(30)


def steer_left():
    global image
    global sense
    image = [
        e, e, e, e, e, e, e, e,
        e, e, e, e, e, e, e, e,
        e, e, e, e, e, b, e, e,
        e, e, e, e, e, b, b, e,
        b, b, b, b, b, b, b, b,
        e, e, e, e, e, b, b, e,
        e, e, e, e, e, b, e, e,
        e, e, e, e, e, e, e, e
    ]
    sense.set_pixels(image)
    steer(-30)


def steer_center():
    steer(0)
    

func = [go, back, stop, speedUp, speedDown, steer_right, steer_left, steer_center]
command = ['go', 'back', 'stop', 'speedUp', 'speedDown', 'right', 'left', 'center']

class pollingThread(QThread):
    def __init__(self):
        super().__init__()
    
    def run(self):
        self.db=QtSql.QSqlDatabase.addDatabase('QMYSQL')
        self.db.setHostName("3.34.124.67")
        self.db.setDatabaseName("15_8")
        self.db.setUserName("15_8")
        self.db.setPassword("1234")
        self.ok=self.db.open()
        print(self.ok)
        self.pollingQuery()
        
    def pollingQuery(self):
        while True:
            time.sleep(0.1)
            self.query=QtSql.QSqlQuery("select * from command2 where is_finish = 0 order by time asc limit 1")
            self.query.next()
            self.record=self.query.record()
            str="%s | %10s | %10s | %4d" % (self.record.value(0).toString(),self.record.value(1), self.record.value(2),self.record.value(3))
            print(str)
            global command
            global func
            if self.record.value(1) in command:
                func[command.index(self.record.value(1))] ()
                self.commandQuery(self.record.value(1),self.record.value(0))

    def commandQuery(self,cmd, time_key):
        str='update command2 set is_finish = 1 where time = "%s" and cmd_string = "%s" and is_finish = 0'%(self.record.value(0).toString('yyyy-MM-dd hh:mm:ss'), cmd)
        self.query.prepare(str);
        self.query.exec()


def main():
    
    
    try:
        th=pollingThread()
        th.start()
            
    except KeyboardInterrupt:
        print("\nTerminate..")
    except:
        print("\n Error")
    finally:   
        mh.getMotor(1).run(Raspi_MotorHAT.RELEASE)
        mh.getMotor(2).run(Raspi_MotorHAT.RELEASE)
        mh.getMotor(3).run(Raspi_MotorHAT.RELEASE)
        mh.getMotor(4).run(Raspi_MotorHAT.RELEASE)

if __name__ == "__main__":
    main()