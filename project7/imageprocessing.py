from PyQt5.QtWidgets import *
from PyQt5.uic import *
from PyQt5.QtGui import *
import cv2
import numpy

class MyApp(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi("hi.ui",self)
        self.main()
    
    def main(self):
        self.img=cv2.imread('bg.jpg')
        self.img=self.processingImage(self.img)
        self.printImage(self.img,self.pic)
        
    def processingImage(self,img):
        return img
    
    def printImage(self,imgBGR,pic):
        imgRGB=cv2.cvtColor(imgBGR,cv2.COLOR_BGR2RGB)
        h,w,byte=imgRGB.shape
        img=QImage(imgRGB,w,h,byte*w,QImage.Format_RGB888)
        pic.setPixmap(QPixmap(img))


app=QApplication([])
win=MyApp()
win.show()
app.exec()