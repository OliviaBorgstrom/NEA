from PyQt5.QtWidgets import * # noqa
from PyQt5.QtGui import QIcon
from PyQt5 import QtCore
from PyQt5 import QtGui
from Database import fetchLocations,fetchSitedata
from datetime import datetime,timedelta
from QDialog_Edit import EditDialog
from QDialog_Add import AddDialog
import sys
import os
import platform
#QApplication, QDialog, QMainWindow, QTabWidget, QWidget, QVBoxLayout, QTableWidget, QLabel, QLineEdit, QPushButton,
#List of used modules

class stack(object):
    def __init__(self):
        self.pointer = -1
        self.body = []

    def push(self,data):
        self.body.append(data)
        self.pointer += 1

    def pop(self,data):
        self.body.pop(pointer)
        self.pointer -= 1

    def topitem(self):
        return self.body[self.pointer]

    def isEmpty(self):
        return self.body == []

    def __len__(self):
        return len(self.body)

    def __str__(self):
        return (str(self.body))[1:-1].replace(" ","")

    def getcurrentpointer(self):
        return self.pointer

class TabWidget(QWidget):
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("NEL Wastebase")
        self.setWindowIcon(QIcon("gearicon.jpg"))
        self.setGeometry(300,150,700,500)  # x,y,width,height
        self.tabmenu = QTabWidget()
        #tabmenu.setTabsClosable(True)
        tabs = [[homeTab(self),"home"],[createTab(),'create'],[importTab(),'import'],[viewTab(),'view']]
        for i in range(len(tabs)):
            self.tabmenu.addTab(tabs[i][0],tabs[i][1])
    
        # tabmenu is a PyQt5 widget which allows for tabs to be set out
        mainbox = QVBoxLayout()
        mainbox.addWidget(self.tabmenu)
        self.setLayout(mainbox)
    
    def inserthelp(self):
        self.tabmenu.insertTab(4,helpTab(self),"help")
        self.tabmenu.setCurrentIndex(4)
    
    def closehelp(self):
        self.tabmenu.removeTab(4)
        self.tabmenu.setCurrentIndex(0)

        # mainbox is the encompassing layout for the whole window, the tabs are added to a box.

class homeTab(QWidget):
    def __init__(self,tabobject):
        super().__init__()
        homebox = QVBoxLayout()
        # WelcomeLabel.resize(, 25)
        #WelcomeLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.initWelcomeGroup(tabobject)
        self.initImportGroup()
        self.initSettingsGroup()

        homebox.addWidget(self.welcomegroup)
        homebox.addWidget(self.importgroup)
        homebox.addWidget(self.settingsgroup)
    
        self.setLayout(homebox)

    def initWelcomeGroup(self,tabobject):
        print(tabobject)
        self.welcomegroup = QGroupBox('Welcome to the NELincs Waste Manager')
        #self.welcomegroup.setStyleSheet(("font: bold 10pt AGENTORANGE"))

        HButtons = QHBoxLayout()
        Seereports = QPushButton('See past reports')
        Seereports.clicked.connect(self.openfile)
        
        Gethelp = QPushButton('How to get started?')
        Gethelp.clicked.connect(tabobject.inserthelp)
        SiteSettings = QPushButton('Manage your sites')
        
        HButtons.addWidget(Seereports)
        HButtons.addWidget(Gethelp)
        HButtons.addWidget(SiteSettings)

        self.welcomegroup.setLayout(HButtons)

    def initImportGroup(self):
        self.importgroup = QGroupBox('Import some new data')
        HButtons = QHBoxLayout()
        
        fromFile = QPushButton('Import from file')
        
        autoDetect = QPushButton('Automatically detect your files')
        
        HButtons.addWidget(fromFile)
        HButtons.addWidget(autoDetect)

        self.importgroup.setLayout(HButtons)

    def initSettingsGroup(self):
        self.settingsgroup = QGroupBox('Some general settings')
        HButtons = QHBoxLayout()
        
        #fromFile = QPushButton('')
        
        #autoDetect = QPushButton('Automatically detect your files')
        
        #HButtons.addWidget(fromFile)
        #HButtons.addWidget(autoDetect)

        self.importgroup.setLayout(HButtons)
        
    def openfile(self):
        if platform.system() == 'Linux':    # for my cross system development
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

    def initButtonRow(self,label,items):  # initialises layouts for dates and sites
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

class viewTab(QWidget):  # done now other than some improvements and potentially an 'Add' button
    def __init__(self):
        super().__init__()
        #filters = ['Location','From past:'] if i decide to add more filters
        #to grab Location list use a SELECT query to the database
        self.viewbox = QVBoxLayout()
        self.fstack = stack()  # a stack for currently applied filters

        self.rawlocations = fetchLocations("Localhost")
        self.rawsitedata = fetchSitedata("Localhost")  # might changefrom rawsitedata

        self.formatFromDB(self.rawlocations,self.rawsitedata)
        self.currentTableData = self.sitedata

        self.topWidget = self.initTopWidget()
        self.bottomWidget = self.initBottomWidget()

        self.viewbox.addLayout(self.topWidget)
        self.viewbox.addLayout(self.bottomWidget)  # add square filters search box in the corner? or QVBoxLayout

        self.setLayout(self.viewbox)
        
    def initTopWidget(self):
        topWidget = QHBoxLayout()
        
        timeIntervals = ["All","This Year","This Quarter","This Month","Past 7 Days"]
        self.locations.insert(0,'All')
        self.filters = [['Location:',self.locations],['From:',timeIntervals]]
        #list of dropdown labels and the items to include in them
        filtersGroup = QGroupBox("Filter table results")
        self.sideBySide = self.CreateGridLayout(self.filters)
        
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
            #dropdowns[i].currentIndexChanged.connect(self.applyFilters())
    
        self.times.currentIndexChanged.connect(self.applyFilters)
        self.sites.currentIndexChanged.connect(self.applyFilters)
        
        sideBySide = QGridLayout()
        for i in range(len(dropdowns)):
            sideBySide.addWidget(labels[i],0,i)
            sideBySide.addWidget(dropdowns[i],1,i)
        
        return sideBySide
        
    def initBottomWidget(self):
        bottomWidget = QGridLayout()    # set some tooltips, move all inits to self?
        self.dataTable = QTableWidget()
    
        self.dataTable.setColumnCount(5)
        self.dataTable.setRowCount(30)
        self.dataTable.setHorizontalHeaderLabels(["Date", "Location", "Glass %", "Paper %", "Plastic %"])
        self.dataTable.horizontalHeader().setSectionResizeMode(1)
        self.dataTable.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.dataTable.cellClicked.connect(self.rowclicked)
       
        self.currententryIDs = [self.rawsitedata[i][0] for i in range(len(self.sitedata))]  # be wary with this because if they arent correct order, the method will not work # noqa
        self.appendToTable(self.sitedata)

        self.dataTable.resizeColumnsToContents()
        
        self.editButton = QPushButton('Edit')
        self.validRowSelected = False
        self.editButton.setToolTip('Select a row then press edit')
        self.editButton.setFixedSize(QtCore.QSize(120,30))
        self.editButton.clicked.connect(self.refresh(self.executeEdit))

        self.addButton = QPushButton('Add')
        self.addButton.setToolTip('Manually type a new Entry')
        self.addButton.setFixedSize(QtCore.QSize(120,30))
        self.addButton.clicked.connect(self.refresh(self.executeAdd))
       
        bottomWidget.addWidget(self.dataTable, 0, 0)
        bottomWidget.addWidget(self.editButton,1,0)
        bottomWidget.addWidget(self.addButton,1,1)
        
        return bottomWidget

    def refresh(self,func):
        def wrapper():
            func()
            self.rawsitedata = fetchSitedata("Localhost")
            self.formatFromDB(self.rawlocations,self.rawsitedata)
            self.applyFilters()
        return wrapper
    
    def rowclicked(self, row):
        try:
            self.currentRowSelected = self.currentTableData[row]
        except:
            self.validRowSelected = False
        else:
            self.validRowSelected = True
            self.selectedEntryID = self.currententryIDs[row]  # it needs the selected entryID to know what change in the database # noqa
            #print("Row %d was clicked" % (row))
            #print(self.currentRowSelected)

    #@refresh
    def executeEdit(self):
        if not self.validRowSelected:
            return
        else:
            self.Ewindow = EditDialog(self.currentRowSelected,self.locations, self.selectedEntryID, self.siteIDs)
            self.Ewindow.exec()
    
    def executeAdd(self):
        self.Awindow = AddDialog(self.locations, self.siteIDs)
        self.Awindow.exec()
    
    def appendToTable(self,data):
        self.dataTable.clearContents()
        for i in range(len(data)):
            for j in range(len(data[i])):
                self.dataTable.setItem(i,j,QTableWidgetItem(data[i][j]))
        self.setCurrentTableData(data)

    def setCurrentTableData(self, data):
        self.currentTableData = data
    
    def formatFromDB(self,locationdata, sitedata):
        self.locations,self.siteIDs = [location[1] for location in locationdata],[location[0] for location in locationdata]
        self.sitedata = [(str(site[1]),site[2],str(site[3]),str(site[4]),str(site[5])) for site in sitedata]
        #print(self.locations)
        #print(self.sitedata)

    def timeSwitcher(self):
        currenttext = self.times.currentText()
        switcher = {
            'This Year':self.thisyear,
            'Past 7 Days':self.sevendaysago,
            'This Month': self.thismonth,
            'This Quarter': self.thisquarter
        }
        return switcher.get(currenttext,'Error: unknown time frame')

    def generateFilteredData(self,boollist):
        FilteredData = []
        self.currententryIDs = []
        for i in range(len(boollist)):
            if boollist[i]:
                self.currententryIDs.append(self.rawsitedata[i][0])  # entryid used here too
                FilteredData.append(self.sitedata[i])
        return FilteredData

    def applyFilters(self):
        # print(self.times.currentText(),'has been selected')
        self.thismonth = datetime.today().replace(day=1,hour=0, minute=0, second=0, microsecond=0)
        self.sevendaysago = (datetime.today() - timedelta(days=7)).replace(hour=0, minute=0, second=0, microsecond=0)
        self.thisyear = datetime.today().replace(day=1,month=1,hour=0, minute=0, second=0, microsecond=0)
        self.thisquarter = (datetime.today() - timedelta(days=92)).replace(hour=0, minute=0, second=0, microsecond=0)
       
        sitefilter = self.sites.currentText()
        timefilter = self.times.currentText()

        if sitefilter == 'All':
            sfilter = []
            for i in range(len(self.sitedata)):
                sfilter.append(True)
        else:
            sfilter = [sitefilter in entry for entry in self.sitedata]

        if timefilter == 'All':
            tfilter = []
            for i in range(len(self.sitedata)):
                tfilter.append(True)
        else:
            timebool = self.timeSwitcher()
            tfilter = [timebool <= datetime.strptime(self.sitedata[i][0], '%Y-%m-%d') for i in range(len(self.sitedata))]
        #print(tfilter,sfilter)
        combinedfilter = self.combine(tfilter,sfilter)
        filteredData = self.generateFilteredData(combinedfilter)
        self.appendToTable(filteredData)

    def combine(self,list1,list2):
        combined = []
        for i in range(len(list1)):  # should be same length
            if list1[i] and list2[i]:
                combined.append(True)
            else:
                combined.append(False)
        return combined

class helpTab(QWidget):
    def __init__(self,tabobject):
        super().__init__()
        self.closetab = QPushButton('Close and contine')
        self.closetab.clicked.connect(tabobject.closehelp)
        self.vbox = QVBoxLayout()
        self.vbox.addWidget(self.closetab)
        self.setLayout(self.vbox)

#QApplication.setStyle(QtGui.QStyleFactory.create('cleanlooks'))    #work on making the appearance 'cleaner'
app = QApplication(sys.argv)
mainWindow = TabWidget()
#mainWindow.inserthelp()
mainWindow.show()
app.exec()

#use filter map reduce, improve filtering method so that it isnt linear (need better time complexity)
#add tooltips for hovering over an entry


#add a thing which shows up when someone trys to press edit without selecting anything first
#need to make the page refresh when a dialog is closed - done but also refresesh on cancel or no changes
#make to add the 'Add feature' for adding an entry

#if it has 0 bins it shouldnt be editable at that site
#change the button in help to a cross? if possible
