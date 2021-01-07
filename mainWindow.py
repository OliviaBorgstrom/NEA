from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon
from PyQt5 import QtCore
from PyQt5 import QtGui
from Database import fetchLocations,fetchSitedata
from datetime import datetime,timedelta
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
        self.pointer+= 1

    def pop(self,data):
        self.body.pop(pointer)
        self.pointer-=1

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
        self.fstack = stack() #a stack for currently applied filters
        
        self.locations = fetchLocations("Localhost")
        self.rawsitedata = fetchSitedata("Localhost") #might changefrom rawsitedata
        
        self.sitedata= [(str(site[0]),site[1],str(site[2]),str(site[3]),str(site[4])) for site in self.rawsitedata] # might not want here
        self.currentTableData = self.sitedata

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
        timeIntervals = ["All","This Year","This Quarter","This Month","Past 7 Days"]
        self.locations.insert(0,'All')
        self.filters = [['Location:',self.locations],['From the past:',timeIntervals]] 
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
        self.setCurrentTableData(data)

    
    def setCurrentTableData(self, data):
        self.currentTableData = data

    def timeFilterSignal(self): #this year, past 7 days, this month, *this quarter*
        print(self.times.currentText(),'has been selected')
        self.thismonth = datetime.today().replace(day=1,hour = 0, minute= 0, second= 0, microsecond= 0)
        self.sevendaysago = (datetime.today()-timedelta(days= 7)).replace(hour = 0, minute= 0, second= 0, microsecond= 0)
        self.thisyear = datetime.today().replace(day=1,month=1,hour = 0, minute= 0, second= 0, microsecond= 0)
  
        if self.times.currentIndex() == 0:
    
            #print(self.sites.currentIndex())
            if self.sites.currentIndex() != 0 :
                filtering = [self.sites.currentText() in entry for entry in self.sitedata]
                FilteredData = self.generateFilteredData(filtering,self.sitedata)
                self.appendToTable(FilteredData)
       
            else:
                self.appendToTable(self.sitedata)
       
        else:
            if self.currentTableData != self.sitedata: #checking if a site filter is applied
                print(self.timeSwitcher())
                filtering = [self.timeSwitcher() <= datetime.strptime(self.currentTableData[i][0], '%Y-%m-%d') for i in range(len(self.currentTableData))]
                FilteredData = self.generateFilteredData(filtering,self.currentTableData)
            else: #if no site filter applied
                print(self.timeSwitcher())
                filtering = [self.timeSwitcher() <= datetime.strptime(self.sitedata[i][0], '%Y-%m-%d') for i in range(len(self.currentTableData))]
                FilteredData = self.generateFilteredData(filtering,self.currentTableData)
            
            self.appendToTable(FilteredData)
       
            #date = self.currentTableData[0][0]
            #datetimeobj = datetime.strptime(date, '%Y-%m-%d')


    def timeSwitcher(self):
        currenttext = self.times.currentText()
        switcher= {
            'This Year':self.thisyear,
            'Past 7 Days':self.sevendaysago,
            'This Month': self.thismonth
        }
        return switcher.get(currenttext,'Error: unknown time frame')


    #def siteFilterSignal(self): #Lots of if statements, could implement a case, need a current filters applied thing
        #pass
        #print(self.sites.currentText(),'has been selected')
        #print(self.sites.currentIndex())
        #if self.sites.currentIndex() == 0:
            #if self.times.currentIndex() != 0 :
                #filtering = [self.timeSwitcher() <= datetime.strptime(self.currentTableData[i][0], '%Y-%m-%d') for i in range(len(self.currentTableData))]
                #FilteredData = self.generateFilteredData(filtering,self.currentTableData)
                #self.appendToTable(FilteredData)
    
            #else:
                #self.appendToTable(self.sitedata)
            
        #else:
            #if self.times.currentIndex() != 0:
                #filtering = [self.sites.currentText() in entry for entry in self.currentTableData] #check if there is another filter applies
                #FilteredData = self.generateFilteredData(filtering,self.currentTableData)
                #break
            #else:
                #filtering = list(map((lambda: self.sites.currentText() in self.sitedata[i]),self.sitedata))
                #filtering = [self.sites.currentText() in entry for entry in self.sitedata]
                #FilteredData = self.generateFilteredData(filtering,self.sitedata)
                #print(filtering)
            
            #self.appendToTable(FilteredData)

    
    def generateFilteredData(self,boollist): #change this to include type
        FilteredData =[]
        for i in range(len(boollist)):
            if boollist[i]:
                FilteredData.append(self.sitedata[i])
                #print(FilteredData)
        return FilteredData

    #def applyFilter(type):
        #if fstack.isEmpty():
            #generateFilteredData(self.sitedata,type)
        #else:
            #if len(fstack) == 2 AND NOT type IN fstack.topitem(): #find how to check that the top item is not from the same filter as the new one
                #temp = fstack.topitem()
                #fstack.pop()
                #if self.type.currentText == 'All': 
                    #fstack.push(temp)
                    #then apply the top filter to sitedata
                #else:
                    
                    #generateFilteredData(self.currentTableData,type)
                    #fstack.push(newfilter) #find out how to generate new filter

    def applyFilters(self):
        sitefilter = self.sites.currentText()
        timefilter = self.sites.currentText()
        if sitefilter == 'All':
            sitebool = ''
        
        sfilter = [sitebool in entry for entry in self.sitedata]
        print(sfilter)


        if timefilter == 'All':
            timebool = datetime.today() 
            tfilter = [timebool >= datetime.strptime(self.sitedata[i][0], '%Y-%m-%d') for i in range(len(self.sitedata))]
        else:
            timebool = self.timeSwitcher()
            tfilter = [timebool <= datetime.strptime(self.sitedata[i][0], '%Y-%m-%d') for i in range(len(self.sitedata))]

        print(tfilter)
        combinedfilter = self.combine(tfilter,sfilter)
        print(combinedfilter)
        filteredData = self.generateFilteredData(combinedfilter)
        self.appendToTable(filteredData)

    def combine(self,list1,list2):
        combined = []
        for i in range (len(list1)):  #should be same length
            if list1[i] and list2[i]:
                combined.append(True)
            else:
                combined.append(False)
        return combined

            
#QApplication.setStyle(QtGui.QStyleFactory.create('cleanlooks'))    #work on making the appearance 'cleaner'
app = QApplication(sys.argv)
mainWindow = TabWidget()
mainWindow.show()
app.exec()

#parameterise database, use filter map reduce, improve filtering method so that it isnt linear (need better time complexity)
#date filter is buggy
#location set to ALL when a time is set does not work 
#setting the date FIRST and then setting a location filer doesnt work either
#rework filters to be a stack
#rather than a stack another idea would be to just apply the filters simultaneously creating one bool list which can then
#just be applied to stack data
