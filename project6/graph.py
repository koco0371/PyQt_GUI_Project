from PyQt5.QtWidgets import *
from PyQt5.uic import *
from matplotlib import pyplot
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg

class MyApp(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi("hi.ui",self)
        self.main()
    
    def main(self):
        self.figure=pyplot.Figure()
        self.canvas=FigureCanvasQTAgg(self.figure)
        self.lay.addWidget(self.canvas)
        self.graph1=self.figure.add_subplot(1,2,1)
        self.graph2=self.figure.add_subplot(1,2,2)
    
    def chart1(self):
        line=[1,2,3]
        self.graph1.plot(line,[10,50,30])
        self.graph1.plot(line,[5,34,50])
        self.graph1.plot(line,[13,36,43])
        self.canvas.draw()
                         

    def chart2(self):
        line=[1,2,3]
        self.graph2.bar(line,[10,50,30])
        self.canvas.draw()
    
app=QApplication([])
win=MyApp()
win.show()
app.exec()
    