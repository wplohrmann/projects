import sys
import os
import random
import matplotlib
matplotlib.use('Qt5Agg')
from PyQt5 import QtCore, QtWidgets

from numpy import arange, sin, pi
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

progname = os.path.basename(sys.argv[0])
progversion = "0.1"

class LabelInputPair(QtWidgets.QWidget):
    def __init__(self, title, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        l = QtWidgets.QVBoxLayout(self)
        l.addWidget(QtWidgets.QLabel(title))
        l.addWidget(QtWidgets.QTextEdit())

class LabelDropdownPair(QtWidgets.QWidget):
    def __init__(self, title, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        l = QtWidgets.QVBoxLayout(self)
        l.addWidget(QtWidgets.QLabel(title))
        l.addWidget(QtWidgets.QTextEdit())

class KeyValuePair(QtWidgets.QWidget):
    def __init__(self, key, value, parent=None):
        QtWidgets.QWidget.__init__(self)
        l = QtWidgets.QHBoxLayout(self)
        l.addWidget(QtWidgets.QLabel( key + " " + value))

class KeyValueBox(QtWidgets.QWidget):

    def __init__(self, gridValues, title, parent=None):
        QtWidgets.QWidget.__init__(self, parent)

        groupBox = QtWidgets.QGroupBox(title)
        groupBox.setParent(self)
        hbox = QtWidgets.QVBoxLayout(groupBox)
        for i in range(len(gridValues)):
            vbox = QtWidgets.QHBoxLayout()
            hbox.addLayout(vbox)
            for pair in gridValues[i]:
                vbox.addWidget(KeyValuePair(pair[0], pair[1]))

class AccousticKeyvalues(KeyValueBox):

    def __init__(self, parent=None):
        KeyValueBox.__init__(self,
                             [[["0", "0"], ["0", "1"]],
                             [["1", "0"], ["1", "1"]],
                             [["2", "0"]]],
                             "Accoustic Key Values",
                             parent)

class ApplicationWindow(QtWidgets.QMainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.setWindowTitle("application main window")

        self.file_menu = QtWidgets.QMenu('&File', self)
        self.file_menu.addAction('&Quit', self.fileQuit,
                                 QtCore.Qt.CTRL + QtCore.Qt.Key_Q)
        self.menuBar().addMenu(self.file_menu)

        self.help_menu = QtWidgets.QMenu('&Help', self)
        self.menuBar().addSeparator()
        self.menuBar().addMenu(self.help_menu)

        self.help_menu.addAction('&About', self.about)

        self.main_widget = QtWidgets.QWidget(self)

        AccousticKeyvalues(self.main_widget)
        
        self.main_widget.setFocus()
        self.setCentralWidget(self.main_widget)

        self.statusBar().showMessage("All hail matplotlib!", 2000)

    def fileQuit(self):
        self.close()

    def closeEvent(self, ce):
        self.fileQuit()

    def about(self):
        QtWidgets.QMessageBox.about(self, "About",
                                    """embedding_in_qt5.py example
Copyright 2005 Florent Rougon, 2006 Darren Dale, 2015 Jens H Nielsen

This program is a simple example of a Qt5 application embedding matplotlib
canvases.

It may be used and modified with no restriction; raw copies as well as
modified versions may be distributed without limitation.

This is modified from the embedding in qt4 example to show the difference
between qt4 and qt5"""
                                )


qApp = QtWidgets.QApplication(sys.argv)

aw = ApplicationWindow()
aw.setWindowTitle("%s" % progname)
aw.show()
sys.exit(qApp.exec_())
#qApp.exec_()

