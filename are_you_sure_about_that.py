from PyQt5.QtWidgets import *  # noqa
from PyQt5 import QtCore
from PyQt5 import QtGui

class AreYouSure(QDialog):
    def __init__(self):
        super(AreYouSure,self).__init__()
        self.setFixedSize(200,150)
        self.setWindowTitle("Confirm")
        important_text = QLabel("Are you sure you want to delete this location?")
        important_text.setWordWrap(True)
        important_text.setAlignment(QtCore.Qt.AlignCenter)
        important_text.setStyleSheet("font: bold 10pt AGENTORANGE")
        choice = QDialogButtonBox.Yes | QDialogButtonBox.No

        ballotbox = QDialogButtonBox(choice)
        ballotbox.accepted.connect(self.accept)
        ballotbox.rejected.connect(self.reject)
        ballotbox.move(0,0)

        #buttonalign = QVBoxLayout()
        #buttonalign.addWidget(ballotbox)
        #buttonalign.setAlignment(QtCore.Qt.AlignCenter)

        important_layout = QVBoxLayout()
        important_layout.addWidget(important_text)
        important_layout.addWidget(ballotbox)
        #important_layout.setAlignment(QtCore.Qt.AlignCenter)

        self.setLayout(important_layout)
