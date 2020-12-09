from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon
import sys
#QApplication, QDialog, QMainWindow, QTabWidget, QWidget, QVBoxLayout, QTableWidget, QLabel, QLineEdit, QPushButton,
#List of used modules 

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
        #filters = ['Location','From past:'] if i decide to add more filters
        #to grab Location list use a SELECT query to the database 
        
        locations = ["Asda Ellis Way","Beeson Street","Boating Lake","Brighton Slipway","Butt Lane Laceby","Conistone Avenue Shops","Cromwell Road (Leisure Centre)"]
            #["Weelsby Primary School","Port Health Office, Estuary House, Wharncliffe Road "] #how do i continue onto next line without breaking it
        #just a dummy list for current testing
        timeIntervals = ["Year","Quarter","Month","Week"]
        
        locationLabel = QLabel('Location:')
        locationDropDown = QComboBox()  ##put this in a seperate method which takes list and makes a drop down
        locationDropDown.addItems(locations)
        
        timeLabel = QLabel('From the past:')
        timeIntervalsDropDown = QComboBox()
        timeIntervalsDropDown.addItems(timeIntervals)
        
        #locationDropDown.setEditable(True)  
        #timeIntervalsDropDown.setEditable(True)

        sideBySide = QGridLayout()
        sideBySide.addWidget(locationLabel,0,0)
        sideBySide.addWidget(timeLabel,0,1)
        sideBySide.addWidget(locationDropDown,1,0)
        sideBySide.addWidget(timeIntervalsDropDown,1,1)

        filtersGroup = QGroupBox("Filter table results")
        filtersGroup.setLayout(sideBySide)
        
        topWidget = QHBoxLayout()
        topWidget.addWidget(filtersGroup) 
        
        bottomWidget = QTableWidget()
        
        viewbox = QVBoxLayout()
        viewbox.addLayout(topWidget)
        viewbox.addWidget(bottomWidget) #add square filters search box in the corner? or QVBoxLayout 

        self.setLayout(viewbox)


app = QApplication(sys.argv)
mainWindow = TabWidget()
mainWindow.show()
app.exec()
