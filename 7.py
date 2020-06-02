from PyQt5.QtWidgets import *

app=QApplication([])
win=QMainWindow()

app.setApplicationName("My Friends")
win.resize(400,400)
bar=win.statusBar()
bar.showMessage("manage human network")

mb=win.menuBar()
menu=mb.addMenu("Menu")
menuAdd=QAction("add",win)
menuRemove=QAction("remove",win)
bye=QAction("Exit",win)
menu.addAction(menuAdd)
menu.addAction(menuRemove)
mb.addAction(bye)

main=QWidget()
win.setCentralWidget(main)
addBtn=QPushButton("add")
rmBtn=QPushButton("remove")
btnLayout=QHBoxLayout()
btnLayout.addWidget(addBtn)
btnLayout.addWidget(rmBtn)

form=QFormLayout()
name=QLineEdit()
form.addWidget(QLabel("manage human network."))
form.addRow("name",name)
form.addRow(btnLayout)

main.setLayout(form)

def add():
    str=name.text()
    if len(str)==0:return
    global names
    if names.count(str)==1:
        bar.showMessage("already friend")
    else:
        bar.showMessage("Welcome, my friend")
        names.append(str)
        print(names)

def remove():
    str=name.text()
    if len(str)==0: return
    global names
    if names.count(str)==0:
        bar.showMessage(str+", he is not my friend")
    else:
        bar.showMessage(str+", he is not my friend anymore")
        names.remove(str)
        print(names)
    
def byebye():
    quit()
    
names=["inho","donghun","carrot","hwan"]

addBtn.clicked.connect(add)
rmBtn.clicked.connect(remove)

menuAdd.triggered.connect(add)
menuRemove.triggered.connect(remove)
bye.triggered.connect(byebye)


win.show()
app.exec()