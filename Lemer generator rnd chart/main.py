import sys
import random
import math

from statsmodels.distributions.empirical_distribution import ECDF

from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QAction, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, \
    QSpacerItem, QSizePolicy, QPushButton
from PyQt5.QtCore import QSize

from matplotlib.figure import Figure

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar


def calc_Expectation(data, n):
    prob = 1 / n
    sum = 0
    for i in range(0, n):
        sum += (data[i] * prob)

    return "%.3f" % float(sum)


def calc_Variance(data, n):
    mean = sum(data) / n
    deviations = [(x - mean) ** 2 for x in data]
    variance = sum(deviations) / n
    return "%.3f" % float(variance)


class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)

        self.title = 'LR 3'
        self.left = 0
        self.top = 30
        self.width = 1820
        self.height = 980

        self.seed = 1

        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        widget = QWidget(self)
        self.setCentralWidget(widget)
        self.vlay = QVBoxLayout(widget)
        hlay = QHBoxLayout()
        self.vlay.addLayout(hlay)

        # font
        font = QtGui.QFont()
        font.setPointSize(14)
        font10 = QtGui.QFont()
        font10.setPointSize(10)

        self.lengthLabel = QLabel('Длинна последовательности:', self)
        self.lengthLabel.setFont(font)
        self.radioMode1 = QtWidgets.QRadioButton('Встроенный')
        self.radioMode1.setFont(font10)
        self.radioMode1.setChecked(True)
        self.radioMode2 = QtWidgets.QRadioButton('Метод Лемера')
        self.radioMode2.setFont(font10)
        self.expectedVal = QLabel('Математическое ожидание:', self)
        self.expectedVal.setFont(font)
        self.expectedVal_num = QLabel(self)
        self.expectedVal_num.setFont(font10)
        self.expectedVal_num.setStyleSheet("background-color:#fff")
        self.expectedVal_num.setMinimumSize(QtCore.QSize(60, 25))
        self.expectedVal_num.setMaximumSize(QtCore.QSize(60, 25))
        self.variance = QLabel('Дисперсия:', self)
        self.variance.setFont(font)
        self.variance_num = QLabel(self)
        self.variance_num.setFont(font10)
        self.variance_num.setStyleSheet("background-color:#fff")
        self.variance_num.setMinimumSize(QtCore.QSize(60, 25))
        self.variance_num.setMaximumSize(QtCore.QSize(60, 25))
        self.statsLabel = QLabel('Число ПИ: ', self)
        self.statsLabel.setFont(font)
        self.piOutput = QLabel(self)
        self.piOutput.setFont(font)
        self.piOutput.setStyleSheet("background-color:#fff")
        self.piOutput.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        self.piOutput.setMinimumSize(QtCore.QSize(262, 23))
        self.piOutput.setMaximumSize(QtCore.QSize(262, 23))

        self.spinBox = QtWidgets.QSpinBox(self)
        self.spinBox.setMinimumSize(QtCore.QSize(100, 0))
        self.spinBox.setMinimum(100)
        self.spinBox.setMaximum(10000)

        hlay.addWidget(self.lengthLabel)
        hlay.addWidget(self.spinBox)
        hlay.addWidget(self.radioMode1)
        hlay.addWidget(self.radioMode2)
        hlay.addWidget(self.expectedVal)
        hlay.addWidget(self.expectedVal_num)
        hlay.addWidget(self.variance)
        hlay.addWidget(self.variance_num)

        hlay.addItem(QSpacerItem(1000, 10, QSizePolicy.Expanding))

        startButton = QPushButton('Запуск', self)
        startButton.setMinimumSize(QSize(200, 40))
        clearButton = QPushButton('Очистить', self)
        clearButton.setMinimumSize(QSize(200, 40))
        startButton.clicked.connect(self.start)
        clearButton.clicked.connect(self.clear)

        hlay2 = QHBoxLayout()
        hlay2.addWidget(self.statsLabel)
        hlay2.addWidget(self.piOutput)
        hlay2.addWidget(startButton)
        hlay2.addWidget(clearButton)
        hlay2.addItem(QSpacerItem(1000, 10, QSizePolicy.Expanding))
        self.vlay.addLayout(hlay2)

    def start(self):
        if self.radioMode1.isChecked():
            # calc PI
            in_circle = 0
            throws = 0
            while throws < self.spinBox.value():
                xPos = random.uniform(-1.0, 1.0)
                yPos = random.uniform(-1.0, 1.0)
                if math.hypot(xPos, yPos) <= 1:  # SQRT(х * х + у * у).
                    in_circle += 1
                throws += 1
            pi = (4.0 * in_circle) / self.spinBox.value()
            self.piOutput.setText(str(pi))

            # histogram
            data = [random.randint(0, 99) for i in range(self.spinBox.value())]
            self.m = WidgetPlot(self, num_seq=data)
            self.vlay.addWidget(self.m)
            self.expectedVal_num.setText(calc_Expectation(data, self.spinBox.value()))
            self.variance_num.setText(calc_Variance(data, self.spinBox.value()))

        if self.radioMode2.isChecked():
            # calc PI
            in_circle = 0
            throws = 0
            while throws < self.spinBox.value():
                xPos = self.Lemer(self.seed)
                yPos = self.Lemer(self.seed)
                if math.hypot(xPos, yPos) <= 1:  # SQRT(х * х + у * у).
                    in_circle += 1
                throws += 1
            pi = (4.0 * in_circle) / self.spinBox.value()
            self.piOutput.setText(str(pi))

            # histogram
            data = [self.LemerN(self.seed) for i in range(self.spinBox.value())]  # LemerN n default is 100
            self.m = WidgetPlot(self, num_seq=data)
            self.vlay.addWidget(self.m)
            self.expectedVal_num.setText(calc_Expectation(data, self.spinBox.value()))
            self.variance_num.setText(calc_Variance(data, self.spinBox.value()))

    def Lemer(self, seed):
        a = 1664525
        b = 1013904223
        c = 90000

        val = (a * seed + b) % c
        uniform_val = val / c  # [0,1)
        self.seed = uniform_val
        return uniform_val

    def LemerN(self, seed, n=100):
        a = 1664525
        b = 1013904223
        n -= 1

        int_val = (a * seed + b) % n  # n is the right border
        self.seed = int_val
        return int_val

    def clear(self):
        self.seed = 1
        self.m.close()
        self.piOutput.clear()
        self.expectedVal_num.clear()
        self.variance_num.clear()


class WidgetPlot(QWidget):
    def __init__(self, *args, num_seq=None, **kwargs):
        QWidget.__init__(self, *args, **kwargs)
        self.setLayout(QVBoxLayout())
        self.canvas = PlotCanvas(self, width=10, height=8)
        self.canvas.plot(num_sec_c=num_seq)
        self.canvas2 = PlotCanvas(self, width=10, height=8)
        self.canvas2.plot2(num_sec_c=num_seq)
        self.toolbar = NavigationToolbar(self.canvas, self)
        self.toolbar2 = NavigationToolbar(self.canvas2, self)
        self.layout().addWidget(self.toolbar)
        self.layout().addWidget(self.canvas)
        self.layout().addWidget(self.toolbar2)
        self.layout().addWidget(self.canvas2)


class PlotCanvas(FigureCanvas):
    def __init__(self, parent=None, width=10, height=8, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        FigureCanvas.__init__(self, fig)
        self.setParent(parent)
        FigureCanvas.setSizePolicy(self, QSizePolicy.Expanding, QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

    def plot(self, num_sec_c):
        ax = self.figure.add_subplot(111)
        ax.hist(num_sec_c, bins=100, linewidth=0.5, ec="k")  # , width=4
        ax.set_title('f(x)')
        self.draw()

    def plot2(self, num_sec_c):
        ax = self.figure.add_subplot(111)
        ecdf = ECDF(num_sec_c) # cdf
        ax.plot(ecdf.x, ecdf.y, color='green')
        #ax.hist(num_sec_c, bins=100, linewidth=0.5, cumulative=True, histtype='step', color='green', )
        ax.set_title('F(x)')
        self.draw()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    sys.exit(app.exec_())
