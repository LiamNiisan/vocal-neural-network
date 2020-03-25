# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'interface.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets
from input_data import write_input
from main import apprentissage
import threading

def threadFunction(interface):
    apprentissage()
    interface.resetButtonState()

class Ui_InterfaceWindow(object):

    def clickedRunButton(self):
        self.runButton.setText("Loading...")
        self.runButton.setEnabled(False)

        #configuration des inputs
        input = self.inputComboBox.currentText()
        layer = self.layerSpin.value()
        nbLayer1 = self.nbLayer1Spin.value()
        nbLayer2 = self.nbLayer2Spin.value()
        funct = self.funcComboBox.currentText()
        corrFact = self.corrFactSpin.value()
        b = 1
        output = self.outputSpinBox.value()

        write_input(input, layer, nbLayer1, nbLayer2, funct, corrFact, b, output)

        threadApprentissage = threading.Thread(target=threadFunction, args=(self,))
        threadApprentissage.start()
        #self.threadResetButtonState.start()

    def changedLayersValue(self):
        if self.layerSpin.value() == 1:
            self.nbLayer2Spin.hide()
            self.label_7.hide()
        else:
            self.nbLayer2Spin.show()
            self.label_7.show()

    def setupUi(self, InterfaceWindow):
        InterfaceWindow.setObjectName("InterfaceWindow")
        InterfaceWindow.resize(704, 355)
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


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    InterfaceWindow = QtWidgets.QMainWindow()
    ui = Ui_InterfaceWindow()
    ui.setupUi(InterfaceWindow)
    InterfaceWindow.show()
    sys.exit(app.exec_())
