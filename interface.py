from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QSizePolicy
from input_data import write_input
from main import apprentissage
import threading

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np
import subprocess as sp


def threadFunction(interface, nbEpoch, errorPlot, update_status_bar):
    apprentissage(errorPlot, update_status_bar)
    interface.errorPlot.plot()
    interface.update_error_data()
    interface.resetButtonState()


class Canvas(FigureCanvas):
    def __init__(self, parent=None, width=5, height=5, dpi=100, nbEpoch=10):
        # Cette fonction initialise le graphique

        fig = Figure(figsize=(width, height), dpi=dpi)

        self.axes = fig.add_subplot(111)

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
        self.axes.set_ylim(ymin=0, ymax=100)

    def plot(self):
        # Cette fonction affiche les resultats sur le graphique

        self.axes.clear()
        self.axes.set_title('Erreur en fonction de l\'epoch')
        self.axes.set_xlabel('Nombre d\'epoch')
        self.axes.set_ylabel('Pourcentage d\'erreur (%)')

        self.axes.plot(self.x_data, self.data_train, label='Train data')
        self.axes.plot(self.x_data, self.data_vc, label='VC data')
        self.axes.plot(self.x_data, self.data_test, label='Test data')
        self.axes.legend()
        self.draw()

    def fillData(self, data_train, data_vc, data_test, nbEpoch):
        # Cette fonction remplis les numpy (tableaux) des donnees recoltees

        self.update_number_of_data(nbEpoch)
        self.data_vc = data_vc
        self.data_test = data_test
        self.data_train = data_train

    def update_number_of_data(self, number_of_data):
        # Cette fonction change le nombre de epoch sur le graphique et ajuste l'axe des x
        self.number_of_data = number_of_data
        self.x_data = np.arange(stop=self.number_of_data+1, start=1)
        self.axes.set_xlim(xmax=self.number_of_data)


class Ui_InterfaceWindow():

    def clickedRunButton(self):
        # Cette fonction est utilisee lorsque l'utilisateur clique sur le bouton
        self.runButton.setText("Loading...")
        self.runButton.setEnabled(False)

        if (self.learningRateRadioOui.isChecked()):
            adaptatifLearningRate = 1
        else:
            adaptatifLearningRate = 0

        # configuration des inputs
        write_input(input=self.inputComboBox.currentText(),
                    layer=self.layerSpin.value(),
                    nbLayer1=self.nbLayer1Spin.value(),
                    nbLayer2=self.nbLayer2Spin.value(),
                    funct=self.funcComboBox.currentText(),
                    corrFact=self.corrFactSpin.value(),
                    b=1,
                    output=self.outputSpinBox.value(),
                    epoch=self.epochSpin.value(),
                    adapt=adaptatifLearningRate,
                    moment=self.momemtum.value())

        nbEpoch = self.epochSpin.value()

        # Creer un thread pour lancer la fonction d'apprentissage, ceci permet au code de continuer a rouler
        threadApprentissage = threading.Thread(target=threadFunction,
                                               args=(self, nbEpoch, self.errorPlot, self.update_status_bar))
        threadApprentissage.start()

    def changedLayersValue(self):
        # Cette fonction affiche ou fait disparaitre le choix du nombre de neuronne pour les autres couches
        if self.layerSpin.value() == 1:
            self.nbLayer2Spin.hide()
            self.label_7.hide()
        else:
            self.nbLayer2Spin.show()
            self.label_7.show()

    def setupUi(self, InterfaceWindow):
        # Initialise les differents elements de l'interface graphique (QT Creator)

        InterfaceWindow.setObjectName("InterfaceWindow")
        InterfaceWindow.resize(830, 520)
        self.centralwidget = QtWidgets.QWidget(InterfaceWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.parametreGroupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.parametreGroupBox.setGeometry(QtCore.QRect(10, 10, 301, 361))
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
        self.runButton.setGeometry(QtCore.QRect(10, 330, 89, 25))
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
        self.layerSpin.setMaximum(10)
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
        self.corrFactSpin.setGeometry(QtCore.QRect(130, 60, 69, 26))
        self.corrFactSpin.setMaximum(1.0)
        self.corrFactSpin.setSingleStep(0.05)
        self.corrFactSpin.setProperty("value", 0.1)
        self.corrFactSpin.setObjectName("corrFactSpin")
        self.label_13 = QtWidgets.QLabel(self.parametreGroupBox)
        self.label_13.setGeometry(QtCore.QRect(10, 270, 221, 17))
        self.label_13.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.label_13.setObjectName("label_13")
        self.label_14 = QtWidgets.QLabel(self.parametreGroupBox)
        self.label_14.setGeometry(QtCore.QRect(10, 300, 221, 17))
        self.label_14.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.label_14.setObjectName("label_14")
        self.momemtum = QtWidgets.QDoubleSpinBox(self.parametreGroupBox)
        self.momemtum.setGeometry(QtCore.QRect(130, 270, 69, 26))
        self.momemtum.setMaximum(1.0)
        self.momemtum.setSingleStep(0.05)
        self.momemtum.setProperty("value", 0.5)
        self.momemtum.setObjectName("momemtum")
        self.learningRateRadioOui = QtWidgets.QRadioButton(
            self.parametreGroupBox)
        self.learningRateRadioOui.setGeometry(QtCore.QRect(180, 300, 69, 26))
        self.learningRateRadioOui.setChecked(True)
        self.learningRateRadioOui.setObjectName("learningRateRadioOui")
        self.learningRateRadioNon = QtWidgets.QRadioButton(
            self.parametreGroupBox)
        self.learningRateRadioNon.setGeometry(QtCore.QRect(220, 300, 69, 26))
        self.learningRateRadioNon.setChecked(False)
        self.learningRateRadioNon.setObjectName("learningRateRadioNon")

        # ----------ERROR PLOT ------------------
        self.errorPlot = Canvas(InterfaceWindow, width=5,
                                height=4.9, nbEpoch=self.epochSpin.value())
        self.errorPlot.move(330, 10)

        # ------------Display results-----------
        self.resultGroupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.resultGroupBox.setGeometry(QtCore.QRect(10, 380, 301, 120))
        self.resultGroupBox.setObjectName("resultGroupBox")
        self.label_10 = QtWidgets.QLabel(self.resultGroupBox)
        self.label_10.setGeometry(QtCore.QRect(10, 30, 290, 17))
        self.label_10.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.label_10.setObjectName("label_10")
        self.label_11 = QtWidgets.QLabel(self.resultGroupBox)
        self.label_11.setGeometry(QtCore.QRect(10, 60, 290, 17))
        self.label_11.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.label_11.setObjectName("label_11")
        self.label_12 = QtWidgets.QLabel(self.resultGroupBox)
        self.label_12.setGeometry(QtCore.QRect(10, 90, 290, 17))
        self.label_12.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.label_12.setObjectName("label_12")

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
        # Ajuste les texts des elements de l'interface graphique (QR Creator)
        _translate = QtCore.QCoreApplication.translate
        InterfaceWindow.setWindowTitle(
            _translate("InterfaceWindow", "MainWindow"))
        self.parametreGroupBox.setTitle(
            _translate("InterfaceWindow", "Paramètres"))
        self.label_2.setText(_translate(
            "InterfaceWindow", "Nombre de neuronne de la couche 1 :"))
        self.label_3.setText(_translate("InterfaceWindow", "Nombre d\'epoch"))
        self.label_4.setText(_translate(
            "InterfaceWindow", "Fichier d\'output"))
        self.label_5.setText(_translate(
            "InterfaceWindow", "Fonction d\'activation"))
        self.label_6.setText(_translate("InterfaceWindow", "Input"))
        self.runButton.setText(_translate("InterfaceWindow", "Run"))
        self.funcComboBox.setItemText(0, _translate("InterfaceWindow", "tanh"))
        self.funcComboBox.setItemText(1, _translate("InterfaceWindow", "sig"))
        self.inputComboBox.setItemText(0, _translate("InterfaceWindow", "40"))
        self.inputComboBox.setItemText(1, _translate("InterfaceWindow", "50"))
        self.inputComboBox.setItemText(2, _translate("InterfaceWindow", "60"))
        self.label_7.setText(_translate(
            "InterfaceWindow", "Nombre de neuronne des autres couches :"))
        self.label_8.setText(_translate(
            "InterfaceWindow", "Nombre de couches"))
        self.label_9.setText(_translate(
            "InterfaceWindow", "Taux d\'apprentissage"))
        self.label_13.setText(_translate(
            "InterfaceWindow", "Momemtum: "))
        self.label_14.setText(_translate(
            "InterfaceWindow", "Taux d\'apprentissage adaptatif: "))
        self.learningRateRadioOui.setText("Oui")
        self.learningRateRadioNon.setText("Non")

        # results
        self.resultGroupBox.setTitle(
            _translate("InterfaceWindow", "Résultats"))
        self.update_error_data()

    def resetButtonState(self):
        # Remet le bouton Run a son etat initial
        self.runButton.setText("Run")
        self.runButton.setEnabled(True)

    def update_status_bar(self, message):
        # Permet d'afficher l'etat d'avancement du code
        self.statusbar.showMessage(message)

    def update_error_data(self):
        # Affiche les Taux d'erreur final
        train_data = int(
            self.errorPlot.data_train[len(self.errorPlot.data_train)-1])
        vc_data = int(self.errorPlot.data_vc[len(self.errorPlot.data_vc)-1])
        test_data = int(
            self.errorPlot.data_test[len(self.errorPlot.data_test)-1])
        self.label_10.setText(
            "Pourcentage d\'erreur de l\'apprentissage: " + str(train_data) + "%")
        self.label_11.setText(
            "Pourcentage d\'erreur de la validation croisée: " + str(vc_data) + "%")
        self.label_12.setText(
            "Pourcentage d\'erreur des tests: " + str(test_data) + "%")


if __name__ == "__main__":
    # fonction main lorsqu'on utilise l'interface graphique
    import sys
    app = QtWidgets.QApplication(sys.argv)
    InterfaceWindow = QtWidgets.QMainWindow()
    ui = Ui_InterfaceWindow()
    ui.setupUi(InterfaceWindow)
    InterfaceWindow.show()
    sys.exit(app.exec_())
