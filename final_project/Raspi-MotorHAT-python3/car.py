# day2_car.py

from Raspi_MotorHAT import Raspi_MotorHAT, Raspi_DCMotor
from PyQt5 import QtSql
from PyQt5.QtCore import *
from sense_hat import sense_hat
from time import sleep
from pyowm import OWM

self.owm=OWM("22f81e736830f16039f7dbf55aeec7f7")
obs = owm.weather_at_place('Seoul') 

obs = owm.weather_at_coords(37.654, 127.060)
mh = Raspi_MotorHAT(addr=0x6f)
dcMotor = mh.getMotor(3)    
speed = 125 
dcMotor.setSpeed(speed)

servo = mh._pwm
servo.setPWMFreq(60)
sense=sense_hat.SenseHat()
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
    sense.set_pixels(image)
    dcMotor.run(Raspi_MotorHAT.BACKWARD)


def stop():
    global image
    global sense
    image = [
            e, e, e, b, b, e, e, e,
            e, e, b, e, e, b, e, e,
            e, b, e, e, e, e, b, e,
            b, b, b, b, b, b, b, b,
            b, b, b, b, b, b, b, b,
            e, b, e, e, e, e, b, e,
            e, e, b, e, e, b, e, e,
            e, e, e, b, b, e, e, e
    ]
    sense.set_pixels(image)
    dcMotor.run(Raspi_MotorHAT.RELEASE)
    sleep(2)
    global obs
    weather = obs.get_weather()
    sense.show_message(weater.get_status(),text_colour=(255, 255, 0))
    sleep(2)


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
        self.db=QtSql.QSqlDatabase.addDatabase('QMYSQL','commandDB')
        self.db.setHostName("3.34.124.67")
        self.db.setDatabaseName("15_8")
        self.db.setUserName("15_8")
        self.db.setPassword("1234")
        self.ok=self.db.open()
        print(self.ok)
        self.pollingQuery()
        
    def pollingQuery(self):
        while True:
            sleep(3)
            self.query=QtSql.QSqlQuery("select * from command2 where is_finish = 0 order by time asc limit 1",db=self.db)
            self.query.next()
            self.record=self.query.record()
            str="%s | %10s | %10s | %4d" % (self.record.value(0).toString(),self.record.value(1), self.record.value(2),self.record.value(3))
            global command
            global func
            if self.record.value(1) in command:
                print(str)
                func[command.index(self.record.value(1))] ()
                self.commandQuery(self.record.value(1),self.record.value(0))

    def commandQuery(self,cmd, time_key):
        str='update command2 set is_finish = 1 where time = "%s" and cmd_string = "%s" and is_finish = 0'%(self.record.value(0).toString('yyyy-MM-dd hh:mm:ss'), cmd)
        self.query.prepare(str);
        self.query.exec()
        
class sensingThread(QThread):
    def __init__(self):
        super().__init__()
        self.sense=sense_hat.SenseHat()
    
    def run(self):
        self.db=QtSql.QSqlDatabase.addDatabase('QMYSQL','senseDB')
        self.db.setHostName("3.34.124.67")
        self.db.setDatabaseName("15_8")
        self.db.setUserName("15_8")
        self.db.setPassword("1234")
        self.ok=self.db.open()
        print(self.ok)
        self.commandQuery()
    
    def commandQuery(self):
        while True:
            sleep(3)
            pressure=self.sense.get_pressure()
            temp=self.sense.get_temperature()
            humidity=self.sense.get_humidity()
            
            pressure=round(pressure,2)
            temp=round(temp,2)
            humidity=round(humidity,2)
            self.query=QtSql.QSqlQuery("select * from sensing2",db=self.db)
            str="insert into sensing2 (time,num1,num2,num3, meta_string, is_finish) values (:time, :num1, :num2, :num3, :meta, :finish)"
            self.query.prepare(str);
            time=QDateTime().currentDateTime()
            self.query.bindValue(":time",time)
            self.query.bindValue(":num1",pressure)
            self.query.bindValue(":num2",temp)
            self.query.bindValue(":num3",humidity)
            self.query.bindValue(":meta","")
            self.query.bindValue(":finish",0)
            self.query.exec()


def main():
    
    
    try:
        th2=sensingThread()
        th2.start()
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