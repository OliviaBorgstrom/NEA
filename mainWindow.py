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
        self.topWidget = self.initTopWidget()
        
        bottomWidget = QTableWidget()
        
        viewbox = QVBoxLayout()
        viewbox.addLayout(self.topWidget)
        viewbox.addWidget(bottomWidget) #add square filters search box in the corner? or QVBoxLayout 

        self.setLayout(viewbox)
    
    def initTopWidget(self):
        topWidget = QHBoxLayout()
        
        locations = ["Asda Ellis Way","Beeson Street","Boating Lake","Brighton Slipway","Butt Lane Laceby"
            "Conistone Avenue Shops","Cromwell Road (Leisure Centre)","Weelsby Primary School",
            "Port Health Office, Estuary House, Wharncliffe Road "]  #just a dummy list for testing
        timeIntervals = ["Year","Quarter","Month","Week"]
        filters = [['Location:',locations],['From the past:',timeIntervals]] 
        print(filters)
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


        

app = QApplication(sys.argv)
mainWindow = TabWidget()
mainWindow.show()
app.exec()
