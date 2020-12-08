from PyQt5.QtWidgets import QApplication, QDialog, QMainWindow, QTabWidget, QWidget, QVBoxLayout, QTableWidget
from PyQt5.QtGui import QIcon
import sys

class TabWidget(QDialog):
    
    def __init__(self):
        super().__init__()

        self.setWindowTitle("NEL Wastebase")
        self.setWindowIcon(QIcon("gearicon.jpg"))
        self.setGeometry(300,150,700,500) #x,y,width,height

        tabmenu = QTabWidget()
        tabs = [[homeTab(),"home"],[createTab(),'create'],[importTab(),'import'],[viewTab(),'view']]
        for i in range(len(tabs)):
            tabmenu.addTab(tabs[i][0],tabs[i][1])

        # tabmenu is a PyQt5 widget which allows for tabs to be set out
        mainbox = QVBoxLayout()
        mainbox.addWidget(tabmenu)
        self.setLayout(mainbox)
    
        # mainbox is the encompassing layout for the whole window, the tabs are added to a box.


class homeTab(QWidget):
    def __init__(self):
        super().__init__()
        homebox = QVBoxLayout()
        


class createTab(QWidget):
    def __init__(self):
        super().__init__()


class importTab(QWidget):
    def __init__(self):
        super().__init__()


class viewTab(QWidget):
    def __init__(self):
        super().__init__()
        viewbox = QVBoxLayout()
        


app = QApplication(sys.argv)
mainWindow = TabWidget()
mainWindow.show()
app.exec()
