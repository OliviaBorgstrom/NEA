from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon
from PyQt5 import QtCore
import sys
import os
import platform
#QApplication, QDialog, QMainWindow, QTabWidget, QWidget, QVBoxLayout, QTableWidget, QLabel, QLineEdit, QPushButton,
#List of used modules 

class TabWidget(QDialog):
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("NEL Wastebase")
        self.setWindowIcon(QIcon("gearicon.jpg"))
        self.setGeometry(300,150,700,500) #x,y,width,height

        tabmenu = QTabWidget()
        #tabmenu.setTabsClosable(True)
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
        WelcomeLabel = QLabel('Welcome to the NELincs Waste Manager')
        WelcomeLabel.setStyleSheet("font: bold 20pt AGENTORANGE") 
        #WelcomeLabel.resize(, 25)
        WelcomeLabel.setAlignment(QtCore.Qt.AlignCenter)
        
        HButtons = QHBoxLayout()
        Seereports = QPushButton('See past reports')
        Seereports.clicked.connect(self.openfile) 
        
        Gethelp = QPushButton('How to get started?')
        HButtons.addWidget(Seereports)
        HButtons.addWidget(Gethelp)

        homebox.addWidget(WelcomeLabel)
        homebox.addLayout(HButtons)
        self.setLayout(homebox)
        
    def openfile(self):
        if platform.system() == 'Linux':    #for my cross system development 
            os.system('dolphin /home/livi/NEA/Past_Reports') 
        else:
            os.system(r'explorer.exe C:\Users\Livi\Documents\GitHub\NEA\Past_Reports')

        


class createTab(QWidget):
    def __init__(self):
        super().__init__()
        createbox = QVBoxLayout()
        
        chooseFromLabel = QLabel("Create a new report by choosing\nfrom the following:")
        chooseFromLabel.setStyleSheet("font: 18pt AGENTORANGE") 
        chooseFromLabel.setAlignment(QtCore.Qt.AlignLeft)

        datesRow = self.initButtonRow("Use data from the past:",['Week','Month','Quarter','Year'])

        sitesRow = self.initButtonRow("Include:",['All Sites','Choose ...'])

        createButton = QPushButton("Create")
        createButton.setStyleSheet("font: 10pt AGENTORANGE")

        createbox.addWidget(chooseFromLabel)
        createbox.addLayout(datesRow)
        createbox.addLayout(sitesRow)
        createbox.addWidget(createButton)

        self.setLayout(createbox)

    def initButtonRow(self,label,items): #initialises layouts for dates and sites
        HRow = QHBoxLayout()
        HRowlabel = QLabel(label)
        HRowlabel.setStyleSheet("font: 12pt AGENTORANGE")
        HRowButtons = QButtonGroup()
        HButtonslayout = QHBoxLayout()
       
        for i in range(len(items)):
            tempbutton = QPushButton(items[i])
            tempbutton.setStyleSheet("font: 10pt AGENTORANGE")
            tempbutton.setCheckable(True)
            HRowButtons.addButton(tempbutton)
            HButtonslayout.addWidget(tempbutton)
        
        HRowButtons.setExclusive(True)
        print(HRowButtons)
        
        HRow.addWidget(HRowlabel)
        HRow.addLayout(HButtonslayout)
        
        return HRow

class importTab(QWidget):
    def __init__(self):
        super().__init__() 
        importbox = QVBoxLayout()
        ImportLabel = QLabel('Choose an option to import your files')
        ImportLabel.setStyleSheet("font: bold 20pt AGENTORANGE") 
        #WelcomeLabel.resize(, 25)
        ImportLabel.setAlignment(QtCore.Qt.AlignCenter)
        
        HButtons = QHBoxLayout()
        fileImport = QPushButton('Import from file')
        #fileImport.clicked.connect(self.openfile) 
        
        fileAuto = QPushButton('Automatically detect to import')
        HButtons.addWidget(fileImport)
        HButtons.addWidget(fileAuto)

        importbox.addWidget(ImportLabel)
        importbox.addLayout(HButtons)
        self.setLayout(importbox)


class viewTab(QWidget):
    def __init__(self):
        super().__init__()
        #filters = ['Location','From past:'] if i decide to add more filters
        #to grab Location list use a SELECT query to the database 
        self.topWidget = self.initTopWidget()
        
        bottomWidget = QTableView()
        #bottomWidget.setColumnCount(5)
        #bottomWidget.setVerticalHeaderLabels('Date','Location','Glass %','Paper %','Plastic %')
        
        viewbox = QVBoxLayout()
        viewbox.addLayout(self.topWidget)
        viewbox.addWidget(bottomWidget) #add square filters search box in the corner? or QVBoxLayout 

        self.setLayout(viewbox)
    
    def initTopWidget(self):
        topWidget = QHBoxLayout()
        
        locations = ["Asda Ellis Way","Beeson Street","Boating Lake","Brighton Slipway","Butt Lane Laceby",
            "Conistone Avenue Shops","Cromwell Road (Leisure Centre)","Weelsby Primary School",
            "Port Health Office, Estuary House, Wharncliffe Road "]  #just a dummy list for testing
        timeIntervals = ["Year","Quarter","Month","Week"]
        filters = [['Location:',locations],['From the past:',timeIntervals]] 
        #list of dropdown labels and the items to include in them
        filtersGroup = QGroupBox("Filter table results")
        self.sideBySide = self.CreateGridLayout(filters)
        
        filtersGroup.setLayout(self.sideBySide)
        topWidget.addWidget(filtersGroup)
        
        return topWidget
    

    def CreateGridLayout(self,items):
        labels = []
        dropdowns = [] 
        for i in items:
            label = QLabel(i[0])
            labels.append(label) 
            dropdown = QComboBox()
            dropdown.addItems(i[1])
            dropdowns.append(dropdown)
        
        sideBySide = QGridLayout()
        for i in range(len(dropdowns)):
            sideBySide.addWidget(labels[i],0,i)
            sideBySide.addWidget(dropdowns[i],1,i)
        
        return sideBySide
        
    def initBottomWidget(self):
        pass


        
#QApplication.setStyle(QtGui.QStyleFactory.create('cleanlooks'))    #work on making the appearance 'cleaner'
app = QApplication(sys.argv)
mainWindow = TabWidget()
mainWindow.show()
app.exec()
