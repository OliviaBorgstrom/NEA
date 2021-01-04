from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon
from PyQt5 import QtCore
from PyQt5 import QtGui
from Database import fetchLocations,fetchSitedata
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

        createbox.addWidget(chooseFromLabel,0)
        createbox.addLayout(datesRow,1)
        createbox.addLayout(sitesRow,2)
        createbox.addWidget(createButton,3)

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
        self.viewbox = QVBoxLayout()
        self.locations = fetchLocations("Localhost")
        self.sitedata = fetchSitedata("Localhost")
        self.sitedata= [(str(site[0]),site[1],str(site[2]),str(site[3]),str(site[4])) for site in self.sitedata] # might not want here
        
        self.topWidget = self.initTopWidget() 
        self.bottomWidget = self.initBottomWidget()
    
        self.viewbox.addLayout(self.topWidget)
        self.viewbox.addLayout(self.bottomWidget) #add square filters search box in the corner? or QVBoxLayout 

        self.setLayout(self.viewbox)
        
    def initTopWidget(self):
        topWidget = QHBoxLayout()
        
        #locations = ["Asda Ellis Way","Beeson Street","Boating Lake","Brighton Slipway","Butt Lane Laceby",
            #"Conistone Avenue Shops","Cromwell Road (Leisure Centre)","Weelsby Primary School",
            #"Port Health Office, Estuary House, Wharncliffe Road "]  #just a dummy list for testing
        timeIntervals = ["All","Year","Quarter","Month","Week"]
        self.locations.insert(0,'All')
        filters = [['Location:',self.locations],['From the past:',timeIntervals]] 
        #list of dropdown labels and the items to include in them
        filtersGroup = QGroupBox("Filter table results")
        self.sideBySide = self.CreateGridLayout(filters)
        
        filtersGroup.setLayout(self.sideBySide)
        topWidget.addWidget(filtersGroup)
        
        return topWidget
    

    def CreateGridLayout(self,items):
        self.times = QComboBox()
        self.sites = QComboBox()
       
        labels = []
        dropdowns = [self.sites,self.times] 
        for i in range(len(items)):
            label = QLabel(items[i][0])
            labels.append(label) 
            dropdowns[i].addItems(items[i][1])
            #dropdowns[i].currentIndexChanged.connect(self.filterSignal())
    
        self.times.currentIndexChanged.connect(self.timeFilterSignal)
        self.sites.currentIndexChanged.connect(self.siteFilterSignal)
        
        sideBySide = QGridLayout()
        for i in range(len(dropdowns)):
            sideBySide.addWidget(labels[i],0,i)
            sideBySide.addWidget(dropdowns[i],1,i)
        
        return sideBySide
        
    def initBottomWidget(self):
        bottomWidget = QGridLayout()    #set some tooltips, move all inits to self?
        self.dataTable = QTableWidget()
    
        self.dataTable.setColumnCount(5)
        self.dataTable.setRowCount(30)
        self.dataTable.setHorizontalHeaderLabels(["Date", "Location", "Glass %", "Paper %", "Plastic %"])
        self.dataTable.horizontalHeader().setSectionResizeMode(1)
        self.dataTable.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.appendToTable(self.sitedata)
        self.dataTable.resizeColumnsToContents()
        bottomWidget.addWidget(self.dataTable, 0, 0)
        
        return bottomWidget

    def appendToTable(self,data):
        self.dataTable.clearContents()
        for i in range(len(data)):
            for j in range(len(data[i])):
                self.dataTable.setItem(i,j,QTableWidgetItem(data[i][j]))

    def timeFilterSignal(self):
        print(self.times.currentText(),'has been selected')
    
    def siteFilterSignal(self):
        print(self.sites.currentText(),'has been selected')
        if self.sites.currentIndex() == 0:
            self.appendToTable(self.sitedata)
        
        else:
            #filtering = list(map((lambda: self.sites.currentText() in self.sitedata[i]),self.sitedata))
            filtering = [self.sites.currentText() in entry for entry in self.sitedata]
            print(filtering)
            FilteredData = self.generateFilteredData(filtering)
            self.appendToTable(FilteredData)
    
    def generateFilteredData(self,boollist):
        FilteredData =[]
        for i in range(len(boollist)):
            if boollist[i]:
                FilteredData.append(self.sitedata[i])
                print(FilteredData)
        return FilteredData
            
#QApplication.setStyle(QtGui.QStyleFactory.create('cleanlooks'))    #work on making the appearance 'cleaner'
app = QApplication(sys.argv)
mainWindow = TabWidget()
mainWindow.show()
app.exec()

#parameterise database, use filter map reduce 