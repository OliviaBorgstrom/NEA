from PyQt5.QtWidgets import QApplication, QDialog, QTabWidget, QWidget
from PyQt5.QtGui import QIcon
import sys

class TabWidget(QDialog):
    
    def __init__(self):
        super().__init__()

        self.setWindowTitle("NEL Wastebase")
        self.setWindowIcon(QIcon("gearicon.jpg"))

        #tabs = [[homeTab(),"home"],[createTab(),'create'],[importTab(),'import'],[viewTab(),'view']]
        #for i in range(len(tabs)):
        tabmenu = QTabWidget
        tabmenu.addTab(homeTab(),'home')
        tabmenu.addTab(createTab(),'create')
        tabmenu.addTab(importTab(),'import')
        tabmenu.addTab(viewTab(),'view')
        #tabmenu is a PyQt5 widget which allows for tabs to be set out
        
        mainbox = QVBoxlayout().addWidget(tabmenu) 
        self.setLayout(mainbox)
        #mainbox is the encompassing layout for the whole window, the tabs are added to a box.


class homeTab(QTabWidget):
    def __init__(self):
        super().__init__()

class createTab(QTabWidget):
    def __init__(self):
        super().__init__()

class importTab(QTabWidget):
    def __init__(self):
        super().__init__()

class viewTab(QTabWidget):
    def __init__(self):
        super().__init__()


app = QApplication(sys.argv)
mainWindow = TabWidget()
mainWindow.show()
app.exec()
