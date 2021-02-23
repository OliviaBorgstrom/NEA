from PyQt5.QtWidgets import * # noqa
from PyQt5.QtGui import QIcon
from PyQt5 import QtCore
from PyQt5 import QtGui
from Database import fetchLocations
import sys

class ConfirmImport(QDialog):
    def __init__(self,entriestext):
        super(ConfirmImport,self).__init__()
        self.entriestext = entriestext
        #self.setFixedSize(600,600)
        self.setWindowTitle("Confirm")
        important_text = QLabel("You have selected multiple entries, select yes to confirm these, or no to cancel")
        important_text.setWordWrap(True)
        important_text.setAlignment(QtCore.Qt.AlignCenter)
        important_text.setStyleSheet("font: bold 11pt")  # AGENTORANGE
        choice = QDialogButtonBox.Yes | QDialogButtonBox.No

        ballotbox = QDialogButtonBox(choice)
        ballotbox.accepted.connect(self.accept)
        ballotbox.rejected.connect(self.reject)

        self.initscrollarea()

        important_layout = QVBoxLayout()
        important_layout.addWidget(important_text)
        important_layout.addWidget(self.scrollarea)
        important_layout.addWidget(ballotbox)

        self.setLayout(important_layout)
    
    def initscrollarea(self):
        self.scrollarea = QScrollArea()
        containerwidget = QWidget()
        self.textlayout = QVBoxLayout()

        #firstline = QLabel('Date            Name              Glass          Paper          Plastic')
        firstline = QLabel('Date            Name                 Glass     Paper     Plastic')
        firstline.setStyleSheet("font: bold 10pt")
        self.textlayout.addWidget(firstline)

        for i in range(len(self.entriestext)):
            print(self.entriestext[i])
            temptext = '     '.join(self.entriestext[i])
            templabel = QLabel(temptext)
            templabel.setStyleSheet("font: 10pt")
            self.textlayout.addWidget(templabel)

        containerwidget.setLayout(self.textlayout)
        self.scrollarea.setWidget(containerwidget)

        #self.blocklayout.addWidget(self.scrollarea)
        #self.blocklayout.addWidget(self.listsites)

#work on the spacing of the numbers
