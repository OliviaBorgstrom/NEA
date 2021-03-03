from PyQt5.QtWidgets import *  # noqa
from PyQt5 import QtCore
from PyQt5 import QtGui

class AreYouSure(QDialog):
    def __init__(self,anyEntries,amountOfEntries):
        super(AreYouSure,self).__init__()
        self.setFixedSize(300,150)
        self.setWindowTitle("Confirm")
        if anyEntries:
            self.archive = True  # will still not archive if No is selected
            text = '''The location you are about to delete has ''' + str(amountOfEntries) + ''' entries attributed to it.\nIf you select 'Yes' to delete, these will be archived.\nAre you sure you want to delete this location?'''
            important_text = QLabel(text)
        else:
            self.archive = False
            important_text = QLabel("Are you sure you want to delete this location?")
            
        important_text.setWordWrap(True)
        important_text.setAlignment(QtCore.Qt.AlignCenter)
        important_text.setStyleSheet("font: bold 10pt AGENTORANGE")
        choice = QDialogButtonBox.Yes | QDialogButtonBox.No
        ballotbox = QDialogButtonBox(choice)
        ballotbox.accepted.connect(self.accept)
        ballotbox.rejected.connect(self.reject)
        ballotbox.move(0,0)

        important_layout = QVBoxLayout()
        important_layout.addWidget(important_text)
        important_layout.addWidget(ballotbox)
        #important_layout.setAlignment(QtCore.Qt.AlignCenter)

        self.setLayout(important_layout)
