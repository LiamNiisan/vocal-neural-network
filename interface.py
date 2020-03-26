# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'interface.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QSizePolicy
from input_data import write_input
from main import apprentissage
import threading

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np


def threadFunction(interface, nbEpoch, errorPlot, update_status_bar):
    apprentissage(nbEpoch, errorPlot, update_status_bar)
    interface.errorPlot.plot()
    interface.resetButtonState()


class Canvas(FigureCanvas):
    def __init__(self, parent=None, width=5, height=5, dpi=100, nbEpoch=10):
        fig = Figure(figsize=(width, height), dpi=dpi)

        self.axes = fig.add_subplot(111)
        self.axes.set_title('Erreur en fonction de l\'Epoch')
        self.axes.set_ylabel('(%)')
        self.axes.set_xlabel('Epoch')
        self.axes.set_ylim(ymax=100, ymin=0)

        self.number_of_data = 0
        self.x_data = np.array([])
        self.update_number_of_data(nbEpoch)
        self.axes.set_xlim(xmin=1)

        self.data_train = np.zeros(self.number_of_data)
        self.data_vc = np.zeros(self.number_of_data)
        self.data_test = np.zeros(self.number_of_data)

        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

        self.plot()

    def plot(self):
        self.axes.plot(self.x_data, self.data_train, label="Train data")
        self.axes.plot(self.x_data, self.data_vc, label="VC data")
        self.axes.plot(self.x_data, self.data_test, label="Test data")
        self.draw()

    def fillData(self, data_train, data_vc, data_test, nbEpoch):
        self.update_number_of_data(nbEpoch)
        self.data_vc = data_vc
        self.data_test = data_test
        self.data_train = data_train

    def update_number_of_data(self, number_of_data):
        self.number_of_data = number_of_data
        self.x_data = np.arange(stop=self.number_of_data+1, start=1)
        self.axes.set_xlim(xmax=self.number_of_data)



class Ui_InterfaceWindow():

    def clickedRunButton(self):
        self.runButton.setText("Loading...")
        self.runButton.setEnabled(False)

        #configuration des inputs
        write_input(self.inputComboBox.currentText(),
                    self.layerSpin.value(),
                    self.nbLayer1Spin.value(),
                    self.nbLayer2Spin.value(),
                    self.funcComboBox.currentText(),
                    self.corrFactSpin.value(),
                    1,
                    self.outputSpinBox.value())

        nbEpoch = self.epochSpin.value()

        threadApprentissage = threading.Thread(target=threadFunction,
                                               args=(self, nbEpoch, self.errorPlot, self.update_status_bar))
        threadApprentissage.start()

    def changedLayersValue(self):
        if self.layerSpin.value() == 1:
            self.nbLayer2Spin.hide()
            self.label_7.hide()
        else:
            self.nbLayer2Spin.show()
            self.label_7.show()

    def setupUi(self, InterfaceWindow):
        InterfaceWindow.setObjectName("InterfaceWindow")
        InterfaceWindow.resize(830, 450)
        self.centralwidget = QtWidgets.QWidget(InterfaceWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.parametreGroupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.parametreGroupBox.setGeometry(QtCore.QRect(10, 10, 301, 301))
        self.parametreGroupBox.setObjectName("parametreGroupBox")
        self.label_2 = QtWidgets.QLabel(self.parametreGroupBox)
        self.label_2.setGeometry(QtCore.QRect(10, 210, 221, 17))
        self.label_2.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.parametreGroupBox)
        self.label_3.setGeometry(QtCore.QRect(10, 90, 141, 17))
        self.label_3.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self.parametreGroupBox)
        self.label_4.setGeometry(QtCore.QRect(10, 120, 141, 17))
        self.label_4.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(self.parametreGroupBox)
        self.label_5.setGeometry(QtCore.QRect(10, 150, 141, 17))
        self.label_5.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.label_5.setObjectName("label_5")
        self.label_6 = QtWidgets.QLabel(self.parametreGroupBox)
        self.label_6.setGeometry(QtCore.QRect(10, 30, 51, 17))
        self.label_6.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.label_6.setObjectName("label_6")
        self.runButton = QtWidgets.QPushButton(self.parametreGroupBox)
        self.runButton.setGeometry(QtCore.QRect(10, 270, 89, 25))
        self.runButton.setObjectName("runButton")
        self.runButton.clicked.connect(self.clickedRunButton)
        self.nbLayer1Spin = QtWidgets.QSpinBox(self.parametreGroupBox)
        self.nbLayer1Spin.setGeometry(QtCore.QRect(240, 210, 48, 26))
        self.nbLayer1Spin.setMaximum(1000)
        self.nbLayer1Spin.setProperty("value", 100)
        self.nbLayer1Spin.setObjectName("nbLayer1Spin")
        self.funcComboBox = QtWidgets.QComboBox(self.parametreGroupBox)
        self.funcComboBox.setGeometry(QtCore.QRect(160, 150, 86, 25))
        self.funcComboBox.setObjectName("funcComboBox")
        self.funcComboBox.addItem("")
        self.funcComboBox.addItem("")
        self.epochSpin = QtWidgets.QSpinBox(self.parametreGroupBox)
        self.epochSpin.setGeometry(QtCore.QRect(130, 90, 48, 26))
        self.epochSpin.setMaximum(100)
        self.epochSpin.setProperty("value", 10)
        self.epochSpin.setObjectName("epochSpin")
        self.inputComboBox = QtWidgets.QComboBox(self.parametreGroupBox)
        self.inputComboBox.setGeometry(QtCore.QRect(50, 30, 51, 25))
        self.inputComboBox.setObjectName("inputComboBox")
        self.inputComboBox.addItem("")
        self.inputComboBox.addItem("")
        self.inputComboBox.addItem("")
        self.nbLayer2Spin = QtWidgets.QSpinBox(self.parametreGroupBox)
        self.nbLayer2Spin.setGeometry(QtCore.QRect(240, 240, 48, 26))
        self.nbLayer2Spin.setMaximum(1000)
        self.nbLayer2Spin.setProperty("value", 100)
        self.nbLayer2Spin.setObjectName("nbLayer2Spin")
        self.label_7 = QtWidgets.QLabel(self.parametreGroupBox)
        self.label_7.setGeometry(QtCore.QRect(10, 240, 221, 17))
        self.label_7.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.label_7.setObjectName("label_7")
        self.label_8 = QtWidgets.QLabel(self.parametreGroupBox)
        self.label_8.setGeometry(QtCore.QRect(10, 180, 221, 17))
        self.label_8.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.label_8.setObjectName("label_8")
        self.layerSpin = QtWidgets.QSpinBox(self.parametreGroupBox)
        self.layerSpin.setGeometry(QtCore.QRect(160, 180, 48, 26))
        self.layerSpin.setMinimum(1)
        self.layerSpin.setMaximum(2)
        self.layerSpin.setProperty("value", 2)
        self.layerSpin.setObjectName("layerSpin")
        self.layerSpin.valueChanged.connect(self.changedLayersValue)
        self.outputSpinBox = QtWidgets.QSpinBox(self.parametreGroupBox)
        self.outputSpinBox.setGeometry(QtCore.QRect(130, 120, 48, 26))
        self.outputSpinBox.setMinimum(1)
        self.outputSpinBox.setMaximum(2)
        self.outputSpinBox.setProperty("value", 1)
        self.outputSpinBox.setObjectName("outputSpinBox")
        self.label_9 = QtWidgets.QLabel(self.parametreGroupBox)
        self.label_9.setGeometry(QtCore.QRect(10, 60, 221, 17))
        self.label_9.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.label_9.setObjectName("label_9")
        self.corrFactSpin = QtWidgets.QDoubleSpinBox(self.parametreGroupBox)
        self.corrFactSpin.setGeometry(QtCore.QRect(160, 60, 69, 26))
        self.corrFactSpin.setMaximum(1.0)
        self.corrFactSpin.setSingleStep(0.05)
        self.corrFactSpin.setProperty("value", 0.1)
        self.corrFactSpin.setObjectName("corrFactSpin")

        #----------ERROR PLOT ------------------
        self.errorPlot = Canvas(InterfaceWindow, width=5, height=4, nbEpoch=self.epochSpin.value())
        self.errorPlot.move(320, 10)

        InterfaceWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(InterfaceWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 704, 22))
        self.menubar.setObjectName("menubar")
        InterfaceWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(InterfaceWindow)
        self.statusbar.setObjectName("statusbar")
        InterfaceWindow.setStatusBar(self.statusbar)

        self.retranslateUi(InterfaceWindow)
        self.funcComboBox.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(InterfaceWindow)

    def retranslateUi(self, InterfaceWindow):
        _translate = QtCore.QCoreApplication.translate
        InterfaceWindow.setWindowTitle(_translate("InterfaceWindow", "MainWindow"))
        self.parametreGroupBox.setTitle(_translate("InterfaceWindow", "Paramètres"))
        self.label_2.setText(_translate("InterfaceWindow", "Nombre de neuronne couche 1 :"))
        self.label_3.setText(_translate("InterfaceWindow", "Nombre d\'epoch"))
        self.label_4.setText(_translate("InterfaceWindow", "Fichier d\'output"))
        self.label_5.setText(_translate("InterfaceWindow", "Fonction d\'activation"))
        self.label_6.setText(_translate("InterfaceWindow", "Input"))
        self.runButton.setText(_translate("InterfaceWindow", "Run"))
        self.funcComboBox.setItemText(0, _translate("InterfaceWindow", "tanh"))
        self.funcComboBox.setItemText(1, _translate("InterfaceWindow", "sig"))
        self.inputComboBox.setItemText(0, _translate("InterfaceWindow", "40"))
        self.inputComboBox.setItemText(1, _translate("InterfaceWindow", "50"))
        self.inputComboBox.setItemText(2, _translate("InterfaceWindow", "60"))
        self.label_7.setText(_translate("InterfaceWindow", "Nombre de neuronne couche 2 :"))
        self.label_8.setText(_translate("InterfaceWindow", "Nombre de couches"))
        self.label_9.setText(_translate("InterfaceWindow", "Taux d\'apprentissage"))

    def resetButtonState(self):
        self.runButton.setText("Run")
        self.runButton.setEnabled(True)

    def update_status_bar(self, message):
        self.statusbar.showMessage(message)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    InterfaceWindow = QtWidgets.QMainWindow()
    ui = Ui_InterfaceWindow()
    ui.setupUi(InterfaceWindow)
    InterfaceWindow.show()
    sys.exit(app.exec_())
