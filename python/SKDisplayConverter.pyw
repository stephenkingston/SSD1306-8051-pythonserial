from PyQt5 import QtCore, QtGui, QtWidgets
import serial
import serial.tools.list_ports
from os import SEEK_END
from os import startfile
from time import sleep
from threading import Timer

grayQImage = None
COMPorts = None
bw_values = None
invert = 0
baud = 9600
activePort = ''

class Ui_MainWindow(object):

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(640, 480)
        MainWindow.setMinimumSize(QtCore.QSize(640, 480))
        MainWindow.setMaximumSize(QtCore.QSize(640, 480))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.dumpBox = QtWidgets.QGroupBox(self.centralwidget)
        self.dumpBox.setGeometry(QtCore.QRect(25, 320, 580, 100))
        self.dumpBox.setObjectName("dumpBox")

        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(20, 50, 341, 251))
        self.label.setFrameShape(QtWidgets.QFrame.Box)
        self.label.setText("")
        self.label.setObjectName("label")
        self.label2 = QtWidgets.QLabel(self.centralwidget)
        self.label2.setGeometry(QtCore.QRect(375, 50, 256, 128))
        self.label2.setFocusPolicy(QtCore.Qt.NoFocus)
        self.label2.setFrameShape(QtWidgets.QFrame.Box)
        self.label2.setText("")
        self.label2.setObjectName("label2")
        self.BrowseButton = QtWidgets.QPushButton(self.centralwidget)
        self.BrowseButton.setGeometry(QtCore.QRect(500, 10, 121, 31))
        self.BrowseButton.setObjectName("BrowseButton")
        self.FilePath = QtWidgets.QLineEdit(self.centralwidget)
        self.FilePath.setGeometry(QtCore.QRect(20, 10, 470, 31))
        self.FilePath.setObjectName("FilePath")
        self.pushButton_I2C = QtWidgets.QPushButton(self.dumpBox)
        self.pushButton_I2C.setGeometry(QtCore.QRect(380, 20, 190, 35))
        self.pushButton_I2C.setObjectName("pushButton_I2C")

        self.checkCOM = QtWidgets.QPushButton(self.dumpBox)
        self.checkCOM.setGeometry(QtCore.QRect(200, 55, 120, 36))
        self.checkCOM.setText("List COM Ports")
        self.checkCOM.clicked.connect(self.ListCOMPorts)

        self.labelCOM = QtWidgets.QLabel(self.dumpBox)
        self.labelCOM.setGeometry(QtCore.QRect(20, 60, 170, 30))
        self.labelCOM.setText("")
        self.labelCOM.setAlignment(QtCore.Qt.AlignRight)
        self.labelCOM.setObjectName("label")

        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setGeometry(QtCore.QRect(410, 190, 181, 122))
        self.groupBox.setObjectName("groupBox")
        self.horizontalSlider = QtWidgets.QSlider(self.groupBox)
        self.horizontalSlider.setGeometry(QtCore.QRect(17, 30, 151, 28))
        self.horizontalSlider.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider.setObjectName("horizontalSlider")
        self.horizontalSlider.setMaximum(255)
        self.horizontalSlider.setMinimum(0)
        self.horizontalSlider.setTickInterval(25)
        self.horizontalSlider.setSingleStep(1)
        self.horizontalSlider.setValue(128)

        self.progressBar = QtWidgets.QProgressBar(self.centralwidget)
        self.progressBar.setGeometry(QtCore.QRect(30, 430, 601, 20))
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName("progressBar")
        self.progressBar.setDisabled(True)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 640, 18))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.comboBox = QtWidgets.QComboBox(self.dumpBox)
        self.comboBox.setDisabled(True)
        self.comboBox.resize(300, 30)
        self.comboBox.move(20, 20)

        self.InvertColors = QtWidgets.QCheckBox(self.groupBox)
        self.InvertColors.setDisabled(True)
        self.InvertColors.resize(200, 30)
        self.InvertColors.move(28, 70)
        self.InvertColors.setText("Invert Colors")
        self.InvertColors.stateChanged.connect(self.setCheckBoxState)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.BrowseButton.clicked.connect(self.setImage)
        self.horizontalSlider.valueChanged.connect(self.SliderValueChanged)
        self.pushButton_I2C.clicked.connect(self.SendImageToMicro)

        self.horizontalSlider.setDisabled(True)
        self.pushButton_I2C.setDisabled(True)
        self.FilePath.setDisabled(True)

        self.comboBox.currentIndexChanged.connect(self.PortSelectionChanged)
        self.ListCOMPorts()

        self.saveTXT = QtWidgets.QPushButton(self.dumpBox)
        self.saveTXT.setText("Save .txt image array")
        self.saveTXT.setGeometry(QtCore.QRect(380, 55, 190, 35))
        self.saveTXT.setDisabled(True)
        self.saveTXT.clicked.connect(self.saveAsText)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "SKDisplayConverter"))
        self.BrowseButton.setText(_translate("MainWindow", "Browse.."))
        self.FilePath.setPlaceholderText(_translate("MainWindow", "Select your input image file.."))
        self.pushButton_I2C.setText(_translate("MainWindow", "Send to Display"))
        self.groupBox.setTitle(_translate("MainWindow", "Threshold Slider"))
        self.dumpBox.setTitle(_translate("MainWindow", "Send to micro-controller"))

    def SendImageToMicro(self):
        global activePort
        image = ""
        self.progressBar.setDisabled(False)
        for i in range(0, 64):
            for j in range(0, 128):
                self.progressBar.setValue(25)
                image = image + str(bw_values[i][j])
        self.comboBox.currentText()
        connection = serial.Serial()
        connection.baudrate = baud
        connection.timeout = 10
        try:
            connection.port = str(activePort)
            connection.open()
            self.progressBar.setValue(40)
            img = self.ImageToBinary()
            for x in range(0, 128):
                for byt in img[x*64:(x+1)*64]:
                    connection.write(byt.to_bytes(1, byteorder='big'))
            self.progressBar.setValue(100)
            self.labelCOM.setText("Image sent successfully.")
        except Exception as e:
            self.labelCOM.setText("Connection failed. {}".format(e))
            print(e)
        connection.close()

    def ImageToBinary(self):
        global bw_values
        bitstring = ''
        bytesToSend = []

        for row in range(1, 9):
            for column in range(1, 129):
                bitstring = ''
                for line in range(1, 9):
                    bitstring = bitstring + str(bw_values[(row*8)-line][column-1])
                bytesToSend.append((int(bitstring, 2)))
        return bytesToSend

    def PortSelectionChanged(self):
        global activePort
        index = self.comboBox.currentIndex()
        activePort = COMPorts[index][0]

    def ListCOMPorts(self):
        global COMPorts
        COMPorts = list(serial.tools.list_ports.comports())
        i = 0
        self.comboBox.setDisabled(False)
        self.comboBox.clear()
        for port in COMPorts:
            self.comboBox.addItem(str(port))
            i = i+1
        self.labelCOM.setText("Found {} device(s)".format(i))

        if i == 0:
            self.comboBox.setDisabled(True)

    def SliderValueChanged(self):
        global invert
        global grayQImage
        global bw_values
        gray_pixmap = QtGui.QPixmap.fromImage(grayQImage)
        w = gray_pixmap.width()
        h = gray_pixmap.height()
        bw_qimage = QtGui.QImage(128, 64, QtGui.QImage.Format_Grayscale8)
        if invert == 1:
            light = QtGui.QColor(0, 0, 0)
            dark = QtGui.QColor(255, 255, 255)
            bw_qimage.fill(light)
            bw_values = [[1 for j in range(0, 128)] for i in range(0, 64)]
        else:
            light = QtGui.QColor(255, 255, 255)
            dark = QtGui.QColor(0, 0, 0)
            bw_qimage.fill(light)
            bw_values = [[0 for j in range(0, 128)] for i in range(0, 64)]

        for x in range(0, h):
            for y in range(0, w):
                try:
                    c = grayQImage.pixel(y, x)
                    colors = QtGui.QColor(c).getRgb()
                    value = colors[1]

                    if value < self.horizontalSlider.value():
                        bw_qimage.setPixelColor(y, x, dark)
                        bw_values[x][y] = 1 - invert
                    else:
                        bw_qimage.setPixelColor(y, x, light)
                        bw_values[x][y] = 1 * invert
                except:
                    bw_values[x].append(0)

        bw_pixmap = QtGui.QPixmap.fromImage(bw_qimage)

        self.label2.setPixmap(bw_pixmap.scaled(self.label2.width(), self.label2.height(), QtCore.Qt.KeepAspectRatio))
        self.label2.setAlignment(QtCore.Qt.AlignCenter)

    def setImage(self):
        filename, _ = QtWidgets.QFileDialog.getOpenFileName(None, "Select Image", "",
                                                                "Image files (*.png *.jpeg *.jpg *.bmp)")
        self.FilePath.setText(filename)
        global grayQImage

        if filename:
            self.horizontalSlider.setDisabled(False)
            self.pushButton_I2C.setDisabled(False)
            self.InvertColors.setDisabled(False)
            pixmap = QtGui.QPixmap(filename)
            pixmap_disp = pixmap.scaled(self.label.width(), self.label.height(), QtCore.Qt.KeepAspectRatio)
            self.label.setPixmap(pixmap_disp)
            self.label.setAlignment(QtCore.Qt.AlignCenter)

            Q_image = QtGui.QPixmap.toImage(pixmap)
            grayQImage = Q_image.convertToFormat(QtGui.QImage.Format_Grayscale8)
            grayQImage = grayQImage.scaled(128, 64, QtCore.Qt.KeepAspectRatio)
            self.FilePath.setDisabled(True)
            self.saveTXT.setDisabled(False)
            self.SliderValueChanged()
        
    def setCheckBoxState(self):
        global invert
        if self.InvertColors.isChecked():
            invert = 1
        else:
            invert = 0
        self.SliderValueChanged()

    def saveAsText(self):
        self.saveTXT.setDisabled(True)
        img = self.ImageToBinary()
        try:
            file = open("imageArray.txt", "wb+")
            first = True
            for x in range(0, 128):
                for byt in img[x * 64:(x + 1) * 64]:
                    if first:
                        file.write(bytes("const unsigned char image[] = {", 'utf-8'))
                        first = False
                    file.write(bytes(str(byt), 'utf-8'))
                    file.write(bytes(", ", 'utf-8'))
            for i in range(0, 2):
                file.seek(-1, SEEK_END)
                file.truncate()
            file.write(bytes('};', 'utf-8'))
            file.close()
            self.saveTXT.setText("Saved successfully!")
            timer = Timer(1, self.ButtonStateChange)
            timer.start()
            startfile("imageArray.txt")
        except Exception as e:
            self.labelCOM.setText("{}".format(e))

    def ButtonStateChange(self):
        self.saveTXT.setDisabled(False)
        self.saveTXT.setText("Save .txt image array")

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())