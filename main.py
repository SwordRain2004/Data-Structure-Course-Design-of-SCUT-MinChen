import heapq
import random
import time
import base64
from io import BytesIO
from PIL import Image
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QHeaderView, QMessageBox, QLabel, QGraphicsOpacityEffect
from PyQt5.QtGui import QColor, QPixmap, QIcon, QPalette, QBrush
import sys
import resource_rc

# global parameter
name_of_task = 1
number_of_channel = 4
display_scale = 5
channel = [None for _ in range(number_of_channel)]
frequency = 1
completed = {i: False for i in range(1, 100001)}
completed[0] = True
task_list = []  # heap 存 task
finish_list = []  # heap 存 finished task
error_list = []  # heap 存 error task
counting_of_task = 1
task_ing = []
# widget_line = 0
wrong_bit = 0
# test_time=[7,4,2,3]
"""
name_of_task: int, which is the name of each task
number_of_channel: int, which is the number of channel
channel: list, whose element is task
frequency: the frequency we run the method 'run_for_each_second'
completed: dict, which record the completion status of each task
"""


def base64_to_image(base64_string):
    image_data = base64.b64decode(base64_string)
    image = Image.open(BytesIO(image_data))
    return image


class task:

    def __init__(self, number: int, priority: float, time_consuming: int, and_set: set, or_set: set,
                 break_probability: float, color: list):
        self.number = number
        self.priority = priority
        self.time_consuming = time_consuming
        self.rest_time = time_consuming
        self.and_set = and_set
        self.or_set = or_set
        self.break_probability = break_probability
        self.color = color

        """
        number: int, name of each task
        priority: float, priority of each task
        time_consuming: int, total time of each task
        rest_time: int, rest time of each task
        and_set: set, and dependency of each task
        or_set: set, or dependency of each task
        break_probability: float, the probability of error of each task
        """

    def __lt__(self, other):
        if self.priority < other.priority:
            return True
        else:
            return False


def input_a_task(input_win, priority, time_consuming, and_set, or_set, break_probability, color):
    global name_of_task
    global channel
    global frequency
    global task_list
    global counting_of_task
    if counting_of_task >= 100001:
        display_error = QMessageBox.critical(input_win, "Too Many Task",
                                             'Overflow Error! The number of tasks has reached the upper limitation! Please run the program again!',
                                             QMessageBox.Ok)
        if display_error == QMessageBox.Ok:
            name_of_task = 1
            channel = [None for _ in range(number_of_channel)]
            frequency = 1
            completed = {i: False for i in range(1, 100001)}
            completed[0] = True
            task_list = []  # heap 存 task
            counting_of_task = 1
        return
    if time_consuming < 0 or not 0 <= break_probability <= 100 or min(and_set) < 0 or min(or_set) < 0:
        QMessageBox.critical(input_win, "Parameters Error", 'Please input correct parameters!', QMessageBox.Ok)
        return
    t = task(counting_of_task, priority, time_consuming, and_set, or_set, break_probability, color)
    counting_of_task += 1
    heapq.heappush(task_list, t)


def main():
    global task_list, finish_list, error_list
    task_list, finish_list, error_list = [], [], []
    app = QtWidgets.QApplication(sys.argv)
    controller = Controller()
    controller.show_initial()
    sys.exit(app.exec_())


"""
    进入进程循环：
        # 循环被分为两块，一块用来控制task输入，另一块用于控制任务进程
        ----------------task输入部分----------------
        如果用户输入一个task:
            运行input_a_task函数，并传入对应参数
        ----------------任务进程控制部分------------------
        运行run_for_each_second函数
        sleep 1 秒

"""


class Initial_parameter(QtWidgets.QWidget):
    next_setting = QtCore.pyqtSignal()

    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        InitPa = self
        InitPa.setObjectName("InitPa")
        InitPa.resize(800, 500)
        InitPa.setMaximumSize(800, 500)
        InitPa.setMinimumSize(800, 500)
        palette = QPalette()
        palette.setBrush(QPalette.Background, QBrush(QPixmap(":/b1.jpg")))
        InitPa.setPalette(palette)
        # InitPa.setBackgroundRole(QPalette.Base)
        self.label = QtWidgets.QLabel(InitPa)
        self.label.setGeometry(QtCore.QRect(50, 30, 700, 60))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        font.setBold(True)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.pushButton = QtWidgets.QPushButton(InitPa)
        self.pushButton.setGeometry(QtCore.QRect(315, 315, 170, 50))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.pushButton.setFont(font)
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.initial_setting)
        self.pushButton.setStyleSheet(
            "QPushButton{color: purple}"
            "QPushButton{background-color: rgba(128, 128, 128, 150)}"
            "QPushButton{font: 20pt \"Agency FB\";\n}"
            "QPushButton{border-radius:20px;}")
        self.lineEdit = QtWidgets.QLineEdit(InitPa)
        self.lineEdit.setGeometry(QtCore.QRect(400, 150, 170, 30))
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit.setStyleSheet("QLineEdit{background-color: rgba(255, 255, 255, 150)}")
        self.lineEdit_2 = QtWidgets.QLineEdit(InitPa)
        self.lineEdit_2.setGeometry(QtCore.QRect(400, 200, 170, 30))
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.lineEdit_2.setStyleSheet("QLineEdit{background-color: rgba(255, 255, 255, 150)}")
        self.lineEdit_3 = QtWidgets.QLineEdit(InitPa)
        self.lineEdit_3.setGeometry(QtCore.QRect(400, 250, 170, 30))
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.lineEdit_3.setStyleSheet("QLineEdit{background-color: rgba(255, 255, 255, 150)}")
        self.label_2 = QtWidgets.QLabel(InitPa)
        self.label_2.setGeometry(QtCore.QRect(160, 150, 300, 31))
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(10)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(InitPa)
        self.label_3.setGeometry(QtCore.QRect(160, 200, 300, 31))
        font = QtGui.QFont()
        font.setFamily("Consolas ")
        font.setPointSize(10)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(InitPa)
        self.label_4.setGeometry(QtCore.QRect(160, 250, 300, 31))
        font = QtGui.QFont()
        font.setFamily("Consolas ")
        font.setPointSize(10)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(InitPa)
        self.label_5.setGeometry(QtCore.QRect(250, 100, 350, 30))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.label_5.setFont(font)
        self.label_5.setObjectName("label_5")

        self.retranslateUi(InitPa)
        QtCore.QMetaObject.connectSlotsByName(InitPa)

    def retranslateUi(self, InitPa):
        _translate = QtCore.QCoreApplication.translate
        InitPa.setWindowTitle(_translate("InitPa", "Initial Parameter Setting"))
        self.label.setText(_translate("InitPa", "Welcome to the Distributed Task Scheduling System!"))
        self.pushButton.setText(_translate("InitPa", "Next"))
        self.label_2.setText(_translate("InitPa", "Frequency:"))
        self.label_3.setText(_translate("InitPa", "Channel Number:"))
        self.label_4.setText(_translate("InitPa", "Display Scale:"))
        self.label_5.setText(_translate("InitPa", "Initial Parameter Setting"))

    def initial_setting(self):
        global number_of_channel
        global frequency
        global display_scale
        if self.lineEdit.text().isdigit():
            frequency = int(self.lineEdit.text())
        if self.lineEdit_2.text().isdigit():
            number_of_channel = int(self.lineEdit_2.text())
        if self.lineEdit_3.text().isdigit():
            display_scale = int(self.lineEdit_3.text())
        self.next_setting.emit()


class Board(QtWidgets.QWidget):
    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        displayBoard = self
        displayBoard.setObjectName("displayBoard")
        displayBoard.resize(1600, 1145)
        displayBoard.setMaximumSize(1600, 1145)
        displayBoard.setMinimumSize(1600, 1145)
        palette = QPalette()
        palette.setBrush(QPalette.Background, QBrush(QPixmap(":/b2.jpg")))
        displayBoard.setPalette(palette)
        self.label = QtWidgets.QLabel(displayBoard)
        self.label.setGeometry(QtCore.QRect(70, 40, 649, 81))
        self.label.setObjectName("label")
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(12)
        self.label.setFont(font)
        self.label_2 = QtWidgets.QLabel(displayBoard)
        self.label_2.setGeometry(QtCore.QRect(60, 200, 300, 41))
        self.label_2.setObjectName("label_2")
        self.label_2.setFont(font)
        self.label_3 = QtWidgets.QLabel(displayBoard)
        self.label_3.setGeometry(QtCore.QRect(60, 260, 300, 41))
        self.label_3.setObjectName("label_3")
        self.label_3.setFont(font)
        self.label_4 = QtWidgets.QLabel(displayBoard)
        self.label_4.setGeometry(QtCore.QRect(60, 320, 300, 41))
        self.label_4.setObjectName("label_4")
        self.label_4.setFont(font)
        self.label_5 = QtWidgets.QLabel(displayBoard)
        self.label_5.setGeometry(QtCore.QRect(60, 380, 300, 41))
        self.label_5.setObjectName("label_5")
        self.label_5.setFont(font)
        self.label_6 = QtWidgets.QLabel(displayBoard)
        self.label_6.setGeometry(QtCore.QRect(60, 440, 310, 41))
        self.label_6.setObjectName("label_6")
        self.label_6.setFont(font)
        self.lineEdit = QtWidgets.QLineEdit(displayBoard)
        self.lineEdit.setGeometry(QtCore.QRect(380, 200, 200, 50))
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit.setFont(font)
        self.lineEdit.setStyleSheet("QLineEdit{background-color: rgba(255, 255, 255, 150)}")
        self.lineEdit_2 = QtWidgets.QLineEdit(displayBoard)
        self.lineEdit_2.setGeometry(QtCore.QRect(380, 260, 200, 50))
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.lineEdit_2.setFont(font)
        self.lineEdit_2.setStyleSheet("QLineEdit{background-color: rgba(255, 255, 255, 150)}")
        self.lineEdit_3 = QtWidgets.QLineEdit(displayBoard)
        self.lineEdit_3.setGeometry(QtCore.QRect(380, 320, 200, 50))
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.lineEdit_3.setFont(font)
        self.lineEdit_3.setStyleSheet("QLineEdit{background-color: rgba(255, 255, 255, 150)}")
        self.lineEdit_4 = QtWidgets.QLineEdit(displayBoard)
        self.lineEdit_4.setGeometry(QtCore.QRect(380, 380, 200, 50))
        self.lineEdit_4.setObjectName("lineEdit_4")
        self.lineEdit_4.setFont(font)
        self.lineEdit_4.setStyleSheet("QLineEdit{background-color: rgba(255, 255, 255, 150)}")
        self.lineEdit_5 = QtWidgets.QLineEdit(displayBoard)
        self.lineEdit_5.setGeometry(QtCore.QRect(380, 440, 200, 50))
        self.lineEdit_5.setObjectName("lineEdit_5")
        self.lineEdit_5.setFont(font)
        self.lineEdit_5.setStyleSheet("QLineEdit{background-color: rgba(255, 255, 255, 150)}")
        self.pushButton = QtWidgets.QPushButton(displayBoard)
        self.pushButton.setGeometry(QtCore.QRect(280, 520, 241, 101))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.setFont(font)
        self.pushButton.clicked.connect(self.insertTask)
        self.pushButton.setStyleSheet(
            "QPushButton{color: black}"
            "QPushButton{background-color: rgb(170, 100, 100,)}"
            "QPushButton{font: 22pt \"Agency FB\"}"
            "QPushButton{border-radius:20px;}")
        self.startButton = QtWidgets.QPushButton(displayBoard)
        self.startButton.setGeometry(QtCore.QRect(600, 220, 100, 101))
        self.startButton.setObjectName("startButton")
        self.startButton.setFont(font)
        self.startButton.clicked.connect(self.startRun)
        self.startButton.setStyleSheet(
            "QPushButton{color: rgb(255,255,255)}"
            "QPushButton{background-color: rgb(170, 170, 255)}"
            "QPushButton{font: 9pt \"AcadEref\"}"
            "QPushButton{border: 2px groove gray}"
            "QPushButton{border-style: outset}"
            "QPushButton{border-radius: 30px;}")
        self.endButton = QtWidgets.QPushButton(displayBoard)
        self.endButton.setGeometry(QtCore.QRect(600, 420, 100, 101))
        self.endButton.setObjectName("endButton")
        self.endButton.setFont(font)
        self.endButton.clicked.connect(self.pauseRun)
        self.endButton.setStyleSheet(
            "QPushButton{color: rgb(255,255,255)}"
            "QPushButton{background-color: rgb(170, 170, 255)}"
            "QPushButton{font: 9pt \"AcadEref\"}"
            "QPushButton{border: 2px groove gray}"
            "QPushButton{border-style: outset}"
            "QPushButton{border-radius: 30px;}")

        self.tableWidget = QtWidgets.QTableWidget(displayBoard)
        self.tableWidget.setGeometry(QtCore.QRect(720, 90, 800, 550))
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(number_of_channel)
        self.tableWidget.setRowCount(display_scale)
        self.tableWidget.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.tableWidget.setStyleSheet("QTableWidget{background-color: rgba(255, 255, 255, 150)}")

        # 创建选项卡小控件窗口
        self.tabWidget = QtWidgets.QTabWidget(displayBoard)
        self.tabWidget.setGeometry(QtCore.QRect(114, 700, 700, 350))
        self.tabWidget.setObjectName("tabWidget")
        self.tabWidget.setStyleSheet("QTabWidget{background-color: rgba(255, 255, 255, 100)}")
        self.tab = QtWidgets.QWidget(displayBoard)
        self.tab.setObjectName("tab")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.tab)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(0, 0, 700, 351))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_7 = QtWidgets.QLabel(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_7.setFont(font)
        self.label_7.setAlignment(QtCore.Qt.AlignCenter)
        self.label_7.setObjectName("label_7")
        self.verticalLayout.addWidget(self.label_7)
        self.listWidget_3 = QtWidgets.QListWidget(self.verticalLayoutWidget)
        self.listWidget_3.setObjectName("listWidget_3")
        self.listWidget_3.setStyleSheet("QListWidget{background-color: rgb(229, 255, 204)}")
        self.verticalLayout.addWidget(self.listWidget_3)
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.verticalLayoutWidget_3 = QtWidgets.QWidget(self.tab_2)
        self.verticalLayoutWidget_3.setGeometry(QtCore.QRect(0, 0, 700, 351))
        self.verticalLayoutWidget_3.setObjectName("verticalLayoutWidget_3")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_3)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.label_9 = QtWidgets.QLabel(self.verticalLayoutWidget_3)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_9.setFont(font)
        self.label_9.setAlignment(QtCore.Qt.AlignCenter)
        self.label_9.setObjectName("label_9")
        self.verticalLayout_3.addWidget(self.label_9)
        self.listWidget = QtWidgets.QListWidget(self.verticalLayoutWidget_3)
        self.listWidget.setObjectName("listWidget")
        self.listWidget.setStyleSheet("QListWidget{background-color: rgb(204, 255, 255)}")
        self.verticalLayout_3.addWidget(self.listWidget)
        self.tabWidget.addTab(self.tab_2, "")
        self.tab_3 = QtWidgets.QWidget()
        self.tab_3.setObjectName("tab_3")
        self.verticalLayoutWidget_4 = QtWidgets.QWidget(self.tab_3)
        self.verticalLayoutWidget_4.setGeometry(QtCore.QRect(0, 0, 700, 351))
        self.verticalLayoutWidget_4.setObjectName("verticalLayoutWidget_4")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_4)
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.label_12 = QtWidgets.QLabel(self.verticalLayoutWidget_4)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_12.setFont(font)
        self.label_12.setAlignment(QtCore.Qt.AlignCenter)
        self.label_12.setObjectName("label_12")
        self.verticalLayout_4.addWidget(self.label_12)
        self.listWidget_2 = QtWidgets.QListWidget(self.verticalLayoutWidget_4)
        self.listWidget_2.setObjectName("listWidget_2")
        self.listWidget_2.setStyleSheet("QListWidget{background-color: rgb(255, 153, 153)}")
        self.verticalLayout_4.addWidget(self.listWidget_2)
        self.tabWidget.addTab(self.tab_3, "")

        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.runColor)  # 这个通过调用槽函数来刷新时间
        for i in range(display_scale):
            for j in range(number_of_channel):
                item = QtWidgets.QTableWidgetItem()
                self.tableWidget.setItem(i, j, item)
                item = self.tableWidget.item(i, j)

        self.retranslateUi(displayBoard)
        QtCore.QMetaObject.connectSlotsByName(displayBoard)

    def retranslateUi(self, displayBoard):
        _translate = QtCore.QCoreApplication.translate
        displayBoard.setWindowTitle(_translate("displayBoard", "Display Board"))
        self.label.setText(_translate("displayBoard", "Please enter information of Task " + str(counting_of_task)))
        self.label_2.setText(_translate("displayBoard", "Priority"))
        self.label_3.setText(_translate("displayBoard", "Time Consuming"))
        self.label_4.setText(_translate("displayBoard", "AND Set"))
        self.label_5.setText(_translate("displayBoard", "OR Set"))
        self.label_6.setText(_translate("displayBoard", "Break Probability"))
        self.pushButton.setText(_translate("displayBoard", "Insert"))
        self.startButton.setText(_translate("displayBoard", "Start"))
        self.endButton.setText(_translate("displayBoard", "Pause"))
        self.label_7.setText(_translate("displayBoard", "进行中任务列表"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("displayBoard", "进行中任务"))
        self.label_9.setText(_translate("displayBoard", "已完成任务"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("displayBoard", "已完成任务"))
        self.label_12.setText(_translate("displayBoard", "错误任务列表"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), _translate("displayBoard", "错误任务"))

    def runColor(self):
        global channel
        global task_list
        global number_of_channel
        global wrong_bit
        for i in range(number_of_channel):
            if channel[i] == None:
                keep_task = []
                while len(task_list) > 0:
                    now_task = heapq.heappop(task_list)
                    and_bool = True
                    or_bool = False
                    for j in list(now_task.and_set):
                        and_bool = and_bool and completed[j]
                    for j in list(now_task.or_set):
                        or_bool = or_bool or completed[j]
                    if and_bool and or_bool:
                        channel[i] = now_task
                        tmsg = f"Task {now_task.number}"
                        self.listWidget_3.addItem(tmsg)
                        task_ing.append(tmsg)
                        # widget_line += 1
                        break
                    else:
                        keep_task.append(now_task)
                for j in keep_task:
                    heapq.heappush(task_list, j)

        for i in range(number_of_channel):
            if channel[i] == None: continue
            """若发现某个通道发生报错，运行error_dealing函数"""
            error_code = random.random()
            if error_code <= channel[i].break_probability:
                wrong_bit = 0
                self.pauseRun()
                display_error = (QMessageBox.critical
                                 (self, "Process Break Error", f'Runtime Error! '
                                                               f'The task{channel[i].number} in '
                                                               f'channel {i + 1} encountered an error!'
                                                               f' Press YES to restart the task; '
                                                               f'Press NO to kill this task!',
                                  QMessageBox.Yes | QMessageBox.No))
                if display_error == QMessageBox.Yes:
                    channel[i].rest_time = channel[i].time_consuming
                elif display_error == QMessageBox.No:
                    channel[i].rest_time = 0
                    error_msg = f"{time.asctime()} : Task {channel[i].number} in Channel {i + 1}"
                    error_list.append(error_msg)
                    self.listWidget_2.addItem(error_msg)
                    print(error_list)
                    wrong_bit = 1
                self.startRun()

        for j in range(number_of_channel):
            if channel[j] == None: continue
            for k in range(min(display_scale, channel[j].rest_time)):
                self.tableWidget.item(k, j).setBackground(
                    QtGui.QColor(channel[j].color[0], channel[j].color[1], channel[j].color[2]))
            for k in range(min(display_scale, channel[j].rest_time), display_scale):
                self.tableWidget.item(k, j).setBackground(QtGui.QColor("white"))
            channel[j].rest_time = channel[j].rest_time - 1
            if channel[j].rest_time < 0:
                completed[channel[j].number] = True
                if wrong_bit != 1:
                    finish_msg = f"{time.asctime()} : Task {channel[j].number} in Channel {j + 1}"
                    self.listWidget.addItem(finish_msg)
                fmsg = f"Task {channel[j].number}"
                idx = task_ing.index(fmsg)
                self.listWidget_3.takeItem(idx)
                del task_ing[idx]
                # self.minus_number(idx)
                wrong_bit = 0
                channel[j] = None

    """
    def minus_number(self, i):
        for v in task_ing.values():
            if v > i:
                v -= 1
    """

    def startRun(self):
        self.timer.start(1000 * frequency)

    def pauseRun(self):
        self.timer.stop()

    def insertTask(self):
        priority = int(self.lineEdit.text())
        time_consuming = int(self.lineEdit_2.text())
        if self.lineEdit_3.text() == "":
            and_set = set([0])
        else:
            and_set = set(list(map(int, self.lineEdit_3.text().split())))
        if self.lineEdit_4.text() == "":
            or_set = set([0])
        else:
            or_set = set(list(map(int, self.lineEdit_4.text().split())))
        break_probability = float(self.lineEdit_5.text())
        color = [random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)]
        input_a_task(self, priority, time_consuming, and_set, or_set, break_probability, color)
        self.label.setText(QtCore.QCoreApplication.translate("displayBoard", "Please enter information of Task " + str(
            counting_of_task)))
        self.lineEdit.setText("")
        self.lineEdit_2.setText("")
        self.lineEdit_3.setText("")
        self.lineEdit_4.setText("")
        self.lineEdit_5.setText("")


class Controller:
    def show_initial(self):
        self.InitPa = Initial_parameter()
        self.InitPa.next_setting.connect(self.show_taskinput)
        self.InitPa.show()

    def show_taskinput(self):
        self.mainBoard = Board()
        self.mainBoard.show()
        self.InitPa.close()


if __name__ == '__main__':
    main()
