from PyQt5.QtWidgets import * # noqa
from PyQt5.QtGui import QIcon
from PyQt5 import QtCore
from PyQt5 import QtGui
from Database import fetchLocations,fetchSitedata,deleteEntry,addTo
from datetime import datetime,timedelta
from QDialog_Edit import EditDialog
from QDialog_Add import AddDialog
from QDialog_Siteschoose import ChooseDialog
from QDialog_Compare import CompareDialog
from QDialog_Configure import ConfigureDialog
from QDialog_ConfirmImport import ConfirmImport
from Reportclass_structure import Report
import sys
import os
import platform
import bisect

#QApplication, QDialog, QMainWindow, QTabWidget, QWidget, QVBoxLayout, QTableWidget, QLabel, QLineEdit, QPushButton,
#List of used modules

class TabWidget(QWidget):
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("NEL Wastebase")
        self.setWindowIcon(QIcon("gearicon.jpg"))
        self.setFixedSize(700,500)  # x,y,width,height
        self.tabmenu = QTabWidget()
        self.homeTab = homeTab(self)
        self.createTab = createTab()
        self.viewTab = viewTab()
        #tabmenu.setTabsClosable(True)
        #tabs = [[homeTab2(self),"home"],[createTab(),'create'],[viewTab(),'view']]
        tabs = [[self.homeTab,"home"],[self.createTab,'create'],[self.viewTab,'view']]
        for i in range(len(tabs)):
            self.tabmenu.addTab(tabs[i][0],tabs[i][1])
        # tabmenu is a PyQt5 widget which allows for tabs to be set out
        mainbox = QVBoxLayout()
        mainbox.addWidget(self.tabmenu)
        self.setLayout(mainbox)
    
    def inserthelp(self):
        self.tabmenu.insertTab(3,helpTab(self),"help")
        self.tabmenu.setCurrentIndex(3)
    
    def closehelp(self):
        self.tabmenu.removeTab(3)
        self.tabmenu.setCurrentIndex(0)

        # mainbox is the encompassing layout for the whole window, the tabs are added to a box.

class homeTab(QWidget):
    def __init__(self,tabobject):
        super().__init__()
        self.tabobject = tabobject
        self.homebox = QVBoxLayout()
        self.welcomeLabel = QLabel('Welcome to the NELincs Waste Manager')
        self.welcomeLabel.setStyleSheet(("font: bold 18pt AGENTORANGE ; border: 1px solid #DCDCDC"))
        self.welcomeLabel.setAlignment(QtCore.Qt.AlignCenter)
        # WelcomeLabel.resize(, 25)
        self.initActionsGrid()

        self.homebox.addWidget(self.welcomeLabel,0)
        self.homebox.addLayout(self.actionsGrid,1)
    
        self.setLayout(self.homebox)

    def initActionsGrid(self):
        self.actionsGrid = QGridLayout()
        self.actionsGrid.setColumnStretch(0,1)
        self.actionsGrid.setColumnStretch(1,1)
        self.actionsGrid.setRowStretch(0,1)
        self.actionsGrid.setRowStretch(1,1)

        help_text = QLabel('Need some help getting started?')
        report_text = QLabel('View the reports you have created in the past.')
        configure_text = QLabel('Add new sites or remove old ones from the program.')
        import_text = QLabel('Import some new data into the database (shift and click to select multiple)')

        help_button = QPushButton('click here')
        report_button = QPushButton('open file')
        configure_button = QPushButton('configure')
        import_button = QPushButton('import')

        help_button.clicked.connect(self.tabobject.inserthelp)
        report_button.clicked.connect(self.openfile)
        configure_button.clicked.connect(self.configurePressed)
        import_button.clicked.connect(self.importPressed)

        boxes_list = [['Help', help_text, help_button, 0, 0],['Reports', report_text, report_button, 0, 1],
                      ['Configure', configure_text, configure_button, 1, 0],['Import', import_text, import_button, 1, 1]]
        
        for each in boxes_list:
            self.actionsGrid.addWidget(self.createGroup(each),each[3],each[4])
    
    def createGroup(self,info):
        tempgroup = QGroupBox(info[0])
        tempgroup.setAlignment(QtCore.Qt.AlignCenter)
        tempgroup.setStyleSheet(("font: 15pt "))
        text_and_button = QVBoxLayout()
        
        info[1].setWordWrap(True)
        info[1].setAlignment(QtCore.Qt.AlignCenter)
        info[1].setStyleSheet(("font: 13pt "))

        info[2].setFixedSize(QtCore.QSize(120,30))
        info[2].setStyleSheet(("font:  10pt "))
        buttongroup = QVBoxLayout()
        buttongroup.addWidget(info[2])
        buttongroup.setAlignment(QtCore.Qt.AlignCenter)

        text_and_button.addWidget(info[1])
        text_and_button.addLayout(buttongroup)

        tempgroup.setLayout(text_and_button)
        return tempgroup
        
    def openfile(self):
        if platform.system() == 'Linux':    # for my cross system development
            os.system('dolphin /home/livi/NEA/Past_Reports')
        else:
            os.system(r'explorer.exe C:\Users\Livi\Documents\GitHub\NEA\Past_Reports')
    
    def configurePressed(self):
        self.configureWindow = ConfigureDialog(sysuser,syspassword,syshost)
        state = self.configureWindow.exec()
        if state == 1:
            self.tabobject.viewTab.refreshLocations()  # refresh the locations dropdown on the viewtab
        else:
            return
    
    def importPressed(self):
        failed = False
        choose_txt = QFileDialog()
        choose_txt.setFileMode(QFileDialog.ExistingFiles)
        title = 'Choose file(s) to import'
        filter = "Text files (*.txt)"
        fileschosen = choose_txt.getOpenFileNames(self,title,"",filter)
        print(fileschosen)
        entries_str = []
        entries_database = []
        for i in range(len(fileschosen[0])):
            with open(fileschosen[0][i]) as fh:
                data = fh.readline()
                newEntry = data.split('~')
                entries_str.append(newEntry)
                try:
                    forDatabase = [datetime.strptime(newEntry[0], '%Y-%m-%d'),int(newEntry[1]),
                                   int(newEntry[2]),int(newEntry[3]),int(newEntry[4])]
                    entries_database.append(forDatabase)
                except ValueError:
                    errorwin = QMessageBox()
                    errorwin.setIcon(QMessageBox.Critical)
                    errorwin.setText('Unrecognised file format')
                    errorwin.setWindowTitle("Error")
                    errorwin.exec_()
                    failed = True

        if failed:
            self.importPressed()
        else:
            if len(entries_str) == 1:
                addTo(sysuser,syspassword,syshost,forDatabase[0],forDatabase[1],forDatabase[2], forDatabase[3], forDatabase[4])
            elif len(entries_str) > 1:  # if it is longer than one i would like to confirm they want to add
                locations = fetchLocations(sysuser,syspassword,syshost)
                onlyIDs = [location[0] for location in locations]
                for each in entries_str:  # better way to do this?/ is there any way of doing .index on only a specific index of each part of the 2D array
                    temp = each[1]
                    tempIndex = onlyIDs.index(int(each[1]))
                    each[1] = locations[tempIndex][1]
                confirmWin = ConfirmImport(entries_str)
                state = confirmWin.exec()
                if state == 1:
                    for each in entries_database:
                        addTo(sysuser, syspassword, syshost, each[0], each[1], each[2], each[3], each[4])
                else:
                    return
            else:
                return
            self.tabobject.viewTab.refresh2()
        
class createTab(QWidget):
    def __init__(self):
        super().__init__()
        self.datefromclicked = False  # notes if they have ever been pressed
        self.datetoclicked = False
        self.usingpresets = True  # assume they are using presets by default
        self.comparingreport = False  # assume they aren't comparing by default
        self.selectedReport_index = None
        self.selectedpreset = 'Week'
        self.currentmindate = QtCore.QDate.currentDate().addDays(-7)
        self.currentmaxdate = QtCore.QDate.currentDate()
        self.toplayer = QVBoxLayout()
        self.grid_alignleft = QGridLayout()
        self.calendars_group = QGroupBox('Use Data between two dates:')
        self.presetdate_group = QGroupBox('OR')
        self.calendars_box = QGridLayout()
        self.create_align = QHBoxLayout()

        self.initUI()

        self.setLayout(self.toplayer)
    
    def initUI(self):
        chooseFromLabel = QLabel("Create a new report by choosing from the following:")
        chooseFromLabel.setStyleSheet("font: 18pt")
        self.grid_alignleft.addWidget(chooseFromLabel, 0, 0)
        self.grid_alignleft.setColumnStretch(0, 1)
        self.grid_alignleft.setRowStretch(1, 1)

        self.calendar_from = self.initCalendar()
        self.calendar_to = self.initCalendar()

        self.label_from = QLabel('Date From: ')
        self.label_to = QLabel('Date To: ')
        self.calendar_to.setToolTip('You have to select a date from first')
        self.setCalendarDisabled(self.calendar_to)
        self.calendar_from.clicked.connect(self.fromdateSelected)
        self.calendar_to.clicked.connect(self.todateSelected)
        self.calendars_box.addWidget(self.label_from,1,0)
        self.calendars_box.addWidget(self.label_to,1,1)
        self.calendars_box.addWidget(self.calendar_from,0,0)
        self.calendars_box.addWidget(self.calendar_to,0,1)
        self.calendars_group.setLayout(self.calendars_box)

        self.initdatesrow()
        self.presetdate_group.setLayout(self.datesrow)

        self.initsitesrow()

        createButton = QPushButton("Create")
        createButton.setFixedSize(QtCore.QSize(120,30))
        createButton.clicked.connect(self.createButtonClicked)
        self.create_align.addWidget(createButton)
        self.create_align.setAlignment(QtCore.Qt.AlignRight)

        self.toplayer.addLayout(self.grid_alignleft)
        self.toplayer.addWidget(self.calendars_group,1)
        self.toplayer.addWidget(self.presetdate_group,2)
        self.toplayer.addLayout(self.sitesrow,3)
        self.toplayer.addLayout(self.create_align,4)

    def initdatesrow(self):
        self.datesrow = QHBoxLayout()
        self.deselectbutton = QPushButton('Deselect')
        self.deselectbutton.setFixedSize(QtCore.QSize(120,30))
        self.deselectbutton.setToolTip('Deselect this to use the calendar instead')
        self.deselectbutton.clicked.connect(self.deselectbuttonpressed)
        
        self.dateslabel = QLabel('Use data from:')
        self.preset_dates = QComboBox()
        self.preset_dates.addItems(['Past 7 Days','This Month','This Quarter','This Year'])
        self.preset_dates.currentIndexChanged.connect(self.presetdateselected)
        self.datesrow.addWidget(self.dateslabel)
        self.datesrow.addWidget(self.preset_dates)
        self.datesrow.addWidget(self.deselectbutton)

    def initsitesrow(self):
        self.sitesrow = QHBoxLayout()
        self.radiogroup = QButtonGroup()

        self.siteslabel = QLabel('Include:')
        self.allsitesbutton = QRadioButton('All sites')
        self.allsitesbutton.setChecked(True)
        self.choosebutton = QRadioButton('Choose...')

        self.radiogroup.addButton(self.allsitesbutton)
        self.radiogroup.addButton(self.choosebutton)

        self.sitesrow.addWidget(self.siteslabel)
        self.sitesrow.addWidget(self.allsitesbutton)
        self.sitesrow.addWidget(self.choosebutton)

        if len(os.listdir('Past_Reports')) != 0:
            self.comparebutton = QPushButton('Compare with...')
            self.comparebutton.clicked.connect(self.compareButtonClicked)
            self.sitesrow.addWidget(self.comparebutton)

        self.sitesrow.addStretch()

    def initCalendar(self):
        currentMonth = datetime.now().month
        currentYear = datetime.now().year
        currentDay = datetime.now().day
        calendar = QCalendarWidget(self)
        formating = QtGui.QTextCharFormat()
        formating.setForeground(QtGui.QBrush(QtGui.QColor('white'),QtCore.Qt.SolidPattern))
        calendar.setWeekdayTextFormat(QtCore.Qt.Saturday, formating)
        calendar.setWeekdayTextFormat(QtCore.Qt.Sunday, formating)
        calendar.setMaximumDate(QtCore.QDate(currentYear, currentMonth, currentDay))
        calendar.setSelectedDate(QtCore.QDate(currentYear, currentMonth, currentDay))

        return calendar
        
    def fromdateSelected(self):
        if not self.datefromclicked:
            self.setCalendarEnabled(self.calendar_to)
            self.datefromclicked = True
            self.usingpresets = False  # change to false on first time
        else:
            if self.calendar_from.selectedDate() > self.calendar_to.selectedDate():
                self.calendar_to.setSelectedDate(self.calendar_from.selectedDate())  # confused how this works
                self.todateSelected()
            self.calendar_to.setMinimumDate(self.calendar_from.selectedDate())
        qDate = self.calendar_from.selectedDate()
        self.currentmindate = self.calendar_from.selectedDate()
        newtext = 'Date From: ' + '{0}/{1}/{2}'.format(qDate.day(),qDate.month(),qDate.year())
        self.label_from.setText(newtext)
    
    def todateSelected(self):
        if not self.datetoclicked:
            self.datetoclicked = True
        qDate = self.calendar_to.selectedDate()
        newtext = 'Date To: ' + '{0}/{1}/{2}'.format(qDate.day(),qDate.month(),qDate.year())
        self.label_to.setText(newtext)
        self.currentmaxdate = self.calendar_to.selectedDate()

    def setCalendarDisabled(self,calendar):
        calendar.setDisabled(True)
        formating = QtGui.QTextCharFormat()
        formating.setForeground(QtGui.QBrush(QtGui.QColor('grey'),QtCore.Qt.SolidPattern))
        calendar.setWeekdayTextFormat(QtCore.Qt.Saturday, formating)
        calendar.setWeekdayTextFormat(QtCore.Qt.Sunday, formating)
    
    def setCalendarEnabled(self,calendar):
        calendar.setDisabled(False)
        formating = QtGui.QTextCharFormat()
        formating.setForeground(QtGui.QBrush(QtGui.QColor('white'),QtCore.Qt.SolidPattern))
        calendar.setWeekdayTextFormat(QtCore.Qt.Saturday, formating)
        calendar.setWeekdayTextFormat(QtCore.Qt.Sunday, formating)
        self.calendar_to.setMinimumDate(self.calendar_from.selectedDate())
        self.calendar_to_Minim = self.calendar_from.selectedDate()

    def presetdateselected(self):
        if not self.usingpresets:
            self.usingpresets = True
            self.selectedpreset = self.preset_dates.currentText()
            self.setCalendarDisabled(self.calendar_from)
            self.setCalendarDisabled(self.calendar_to)
        else:
            self.selectedpreset = self.preset_dates.currentText()
        self.currentmindate = self.timeSwitcher(self.selectedpreset)

    def timeSwitcher(self,currenttext):  # fix quarter and can also do this a different way like did in calendar
        switcher = {
            'This Year': datetime.today().replace(day=1,month=1,hour=0, minute=0, second=0, microsecond=0),
            'Past 7 Days':(datetime.today() - timedelta(days=7)).replace(hour=0, minute=0, second=0, microsecond=0),
            'This Month': datetime.today().replace(day=1,hour=0, minute=0, second=0, microsecond=0),
            'This Quarter': (datetime.today() - timedelta(days=92)).replace(hour=0, minute=0, second=0, microsecond=0)
        }
        return switcher.get(currenttext,'Error: unknown time frame')
        
    def deselectbuttonpressed(self):
        if not self.usingpresets or not self.datefromclicked:  # if a time hasnt been selected
            return
        else:
            self.usingpresets = False
            self.setCalendarEnabled(self.calendar_from)
            self.setCalendarEnabled(self.calendar_to)

    def compareButtonClicked(self):
        self.CompareWindow = CompareDialog(self.comparingreport,self.selectedReport_index)
        state = self.CompareWindow.exec()
        if state == 1:
            try:
                returned = self.CompareWindow.radiobuttongroup.checkedButton().text()
                self.comparingreport = True
                self.selectedReport_index = self.CompareWindow.radiobuttongroup.checkedId()
                self.selectedReport_text = returned
                print(returned)
            except Exception as e:
                print(e)
                self.comparingreport = False
                print("None selected")
                return
        else:
            return

    def createButtonClicked(self):
        self.rawlocations = fetchLocations(sysuser,syspassword,syshost)  # just need to fetch specific locations here
        self.justnames = [location[1] for location in self.rawlocations]
        comparetoggle = [self.comparingreport]
        if self.comparingreport:
            comparetoggle.append(self.selectedReport_text[:-4])
            print(comparetoggle)

        if self.choosebutton.isChecked():
            self.Cwindow = ChooseDialog(self.justnames)
            state = self.Cwindow.exec()
            
            if state == 1:
                returned = self.Cwindow.selectedlist
                self.chosenlocationdata = [i for i in self.rawlocations if i[1] in returned]
                thingy = Report(comparetoggle,self.currentmaxdate.toPyDate(),self.currentmindate.toPyDate(),self.chosenlocationdata,returned,syshost)
                print(thingy)
                self.comparingreport = False
                #callAnalysis(self.currentmindate.toPyDate(),self.chosenlocationdata,returned,sysuser,syspassword,syshost)
          
            else:
                return

        elif self.allsitesbutton.isChecked():  # else all sites must be selected
            thingy = Report(comparetoggle,self.currentmaxdate.toPyDate(),self.currentmindate.toPyDate(),self.rawlocations,self.justnames,syshost)
            print(thingy)
            self.comparingreport = False
            #allAnalysis()
        
        else:
            return

class viewTab(QWidget):  # done now other than some improvements
    # add a 'filter between dates
    def __init__(self):
        super().__init__()

        '''month numbers of the quarters
           Q1 is 1,2,3 Q2 is 4,5,6
           Q3 is 7,8,9 Q4 is 10,11,12'''

        self.viewbox = QVBoxLayout()
        self.rawlocations = fetchLocations(sysuser,syspassword,syshost)
        self.rawsitedata = fetchSitedata(sysuser,syspassword,syshost)  # might changefrom rawsitedata

        self.formatFromDB(self.rawlocations,self.rawsitedata)
        self.currentTableData = self.sitedata

        self.topWidget = self.initTopWidget()
        self.bottomWidget = self.initBottomWidget()

        self.viewbox.addLayout(self.topWidget)
        self.viewbox.addLayout(self.bottomWidget)  # add square filters search box in the corner? or QVBoxLayout

        self.setLayout(self.viewbox)
        
    def refreshLocations(self):
        self.rawlocations = fetchLocations(sysuser,syspassword,syshost)
        #self.rawlocations = [(each[1],str(each[4]),str(each[3]),str(each[2])) for each in fetchedlocations]
        self.locations = [location[1] for location in self.rawlocations]
        #print(self.locations)
        self.siteIDs = [location[0] for location in self.rawlocations]
        #print(self.siteIDs)
        #print(self.locations)
        self.sites.clear()
        self.locations.insert(0,'All')
        self.sites.addItems(self.locations)

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
        self.editButton.clicked.connect(self.executeEdit)

        self.addButton = QPushButton('Add')
        self.addButton.setToolTip('Manually type a new Entry')
        self.addButton.setFixedSize(QtCore.QSize(120,30))
        self.addButton.clicked.connect(self.executeAdd)

        self.deleteButton = QPushButton('Delete')
        self.deleteButton.setToolTip('Delete an entry')
        self.deleteButton.setFixedSize(QtCore.QSize(120,30))
        self.deleteButton.clicked.connect(self.executeDelete)
        
        alignButtons = QHBoxLayout()
        alignButtons.addWidget(self.editButton)
        alignButtons.addWidget(self.addButton)
        alignButtons.addWidget(self.deleteButton)
        alignButtons.addStretch(1)
        
        bottomWidget.addWidget(self.dataTable, 0, 0)
        bottomWidget.addLayout(alignButtons,1,0)
    
        return bottomWidget

    def refresh2(self):  # change this to be refresh not refresh2
        self.rawsitedata = fetchSitedata(sysuser,syspassword,syshost)
        self.formatFromDB(self.rawlocations,self.rawsitedata)
        self.applyFilters()
 
    def rowclicked(self, row):
        try:
            self.currentRowSelected = self.currentTableData[row]
        except IndexError:
            self.validRowSelected = False
        else:
            self.validRowSelected = True
            self.selectedEntryID = self.currententryIDs[row]  # it needs the selected entryID to know what change in the database # noqa
            #print("Row %d was clicked" % (row))
            #print(self.currentRowSelected)

    def executeEdit(self):
        if not self.validRowSelected:
            return
        else:
            self.Ewindow = EditDialog(self.currentRowSelected,self.locations, self.selectedEntryID, self.siteIDs,sysuser,syspassword,syshost)
            state = self.Ewindow.exec()
            if state == 1:
                self.refresh2()  # refresh the locations dropdown on the viewtab
            else:
                return
    
    def executeAdd(self):
        self.Awindow = AddDialog(self.locations, self.siteIDs,sysuser,syspassword,syshost)
        state = self.Awindow.exec()
        if state == 1:
            self.refresh2()  # refresh the locations dropdown on the viewtab
        else:
            return
    
    def executeDelete(self):
        if not self.validRowSelected:
            return
        else:
            try:  # a try except to catch any errors with the database or the entry not existing
                deleteEntry(sysuser,syspassword,syshost,self.selectedEntryID)
            except:  # not sure what error this would cause
                print("there was an issue deleting that entry")
                return
            else:
                self.refresh2()
    
    def appendToTable(self,data):
        self.dataTable.clearContents()
        for i in range(len(data)):
            for j in range(len(data[i])):
                self.dataTable.setItem(i,j,QTableWidgetItem(data[i][j]))
        self.setCurrentTableData(data)
        #print(self.currententryIDs)

    def setCurrentTableData(self, data):
        self.currentTableData = data
    
    def formatFromDB(self,locationdata, sitedata):
        self.locations,self.siteIDs = [location[1] for location in locationdata],[location[0] for location in locationdata]
        self.sitedata = [(str(site[1]),site[2],str(site[3]),str(site[4]),str(site[5])) for site in sitedata]
        #print(self.locations)
        #print(self.sitedata)
    
    def getlocations(self):  # return locations
        return self.locations

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
    
    def startOfThisQuarter(self):
        thismonth = datetime.now().month
        quarters = [1,4,7,10]
        i = bisect.bisect_right(quarters,thismonth)
        startofQmonth = quarters[i - 1]
        return datetime(int(datetime.now().year), startofQmonth, 1)

    def applyFilters(self):
        # print(self.times.currentText(),'has been selected')
        self.thismonth = datetime.today().replace(day=1,hour=0, minute=0, second=0, microsecond=0)
        self.sevendaysago = (datetime.today() - timedelta(days=7)).replace(hour=0, minute=0, second=0, microsecond=0)
        self.thisyear = datetime.today().replace(day=1,month=1,hour=0, minute=0, second=0, microsecond=0)
        self.thisquarter = self.startOfThisQuarter()
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
        self.explain = QLabel('''Here will be written instructions on how to use the program,
                                 i just havent written them yet''')

        self.closetab = QPushButton('Close and continue')
        self.closetab.clicked.connect(tabobject.closehelp)
        self.vbox = QVBoxLayout()
        self.vbox.addWidget(self.explain)
        self.vbox.addWidget(self.closetab)
        self.setLayout(self.vbox)

#QApplication.setStyle(QtGui.QStyleFactory.create('cleanlooks'))    #work on making the appearance 'cleaner'
if platform.system() == 'Linux':    # for my cross system development
    sysuser = "livi"
    syspassword = "Pass1234"
    syshost = "localhost"
else:
    sysuser = "desktop"
    syspassword = "password"
    syshost = "192.168.0.184"

app = QApplication(sys.argv)
mainWindow = TabWidget()
#mainWindow.inserthelp()
mainWindow.show()
app.exec()

#use filter map reduce, improve filtering method so that it isnt linear (need better time complexity)
#add tooltips for hovering over an entry


#add a thing which shows up when someone trys to press edit without selecting anything first
#need to make the page refresh when a dialog is closed - done but also refresesh on cancel or no changes

#change the button in help to a cross? if possible

#on the add dialog, put lables above the plastic peper glass ect  # do the same on the site dialog
#currently only appends 30 items to the table <=== (need a view more button)

#text shows up when someone presses choose saying they can choose when they click create

# add an 'All' Checkbox at a laterdate. right now it is not needed
# select and deselect all sites easily

# after creating the first report, shouldnt need to restart to see the compare button <-
# maybe make location and sitedata global so it can be used throughout the program rather than fetching every time??

# check the formatting of the text file to make sure that it is a compatible file <-
# use %s %s parameters to check formatting

# change the order of the date edit box on add tab

#need to make the timeframe select thing work

#if self.anydata = False then make an error that there is no data
