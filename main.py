from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QTimer, QThread, pyqtSignal,QDateTime, Qt
from PyQt5.QtWidgets import  QApplication, QMainWindow, QMessageBox,QDialog,QWidget,QAbstractItemView, QHeaderView, QTableWidgetItem
from PyQt5.QtGui import QPixmap
from windows import Ui_Form
import os, sys
import tempfile
import win32api
import win32print
import cv2
import globVar
from face_recognition import api as face_recognition
import faceOpera

from TCPServer import *
from assignation import *
import teacher_data
import exam_information

# 从自动生成的界面类继承
class SimpleDialogForm(Ui_Form, QtWidgets.QWidget):
    teacher_id = '-1'
    teacher_sex = 's'
    sendmsg = pyqtSignal(str, str, str)
    def __init__(self, parent = None):
        super(SimpleDialogForm, self).__init__()
        self.setupUi(self)  # 在此设置界面
        # 链接按钮动作与函数
        self.faceReco.clicked.connect(self.faceRecogn)
        self.PM_True.clicked.connect(self.messTrue)
        self.PM_Fault.clicked.connect(self.messFault)
        #self.assignment.clicked.connect(self.assignment_)
        self.assignment.setVisible(False)
        self.print.clicked.connect(self.print_)

        # 定义变量
        self.cap = cv2.VideoCapture()
        self.CAM_NUM = 0
        self.id_print = ""
        self.name_print = ""
        self.exam_print = ""
        self.location_print = ""
        self.exPosition_print = ""
        self.flg = 0
        # 初始化定时器
        self.timer_strat = QtCore.QTimer()
        self.timer_camera = QtCore.QTimer()
        self.timer_time = QtCore.QTimer()
        self.timer_facecodeLoad = QtCore.QTimer()
        # 定义时间超时连接
        self.timer_strat.timeout.connect(self.start)
        self.timer_camera.timeout.connect(self.monitorView)
        self.timer_time.timeout.connect(self.showTime)
        self.timer_facecodeLoad.timeout.connect(self.FaceEncodeUpdate)
        # 定义时间任务是一次性任务
        self.timer_strat.setSingleShot(True)
        # 启动时间任务
        self.timer_strat.start()
        self.timer_time.start()
        self.timer_facecodeLoad.start(60000)

        self.PM_True.setEnabled(False)
        self.PM_Fault.setEnabled(False)
        self.assignment.setEnabled(False)
        self.print.setEnabled(False)


    # 系统启动时自动打开摄像头
    def start(self):
        flag = self.cap.open(self.CAM_NUM)
        if flag == False:
            msg = QtWidgets.QMessageBox.warning(self, u"Warning", u"请检测相机与电脑是否连接正确", buttons=QtWidgets.QMessageBox.Ok,
                                                defaultButton=QtWidgets.QMessageBox.Ok)
        else:
            self.registeredIdentity()
            self.timer_camera.start(50)

    # 注册人脸库中的人脸#*************************************************
    def registeredIdentity(self):
        globVar.load_faceEncode()

    def FaceEncodeUpdate(self):
        globVar.update_faceEncode()

    # 显示摄像头捕捉到的画面
    def monitorView(self):
        flag, self.image = self.cap.read()
        global comPic
        show = cv2.resize(self.image, (512, 384))
        comPic = show.copy()
        show = cv2.cvtColor(show, cv2.COLOR_BGR2RGB)
        faceRects = globVar.classfier.detectMultiScale(show, scaleFactor=1.1, minNeighbors=3, minSize=(16, 16))
        if len(faceRects) > 0:  # 大于0则检测到人脸
            faceOrder = 0
            for faceRect in faceRects:  # 单独框出每一张人脸
                x, y, w, h = faceRect
                cv2.rectangle(show, (x, y), (x + w, y + h), globVar.color[faceOrder % 9], 2)
                faceOrder += 1
        showImage = QtGui.QImage(show.data, show.shape[1], show.shape[0], QtGui.QImage.Format_RGB888)
        self.cameraView.setPixmap(QtGui.QPixmap.fromImage(showImage))

    # 显示系统时间
    def showTime(self):
        datetime = QDateTime.currentDateTime()
        text = datetime.toString(Qt.DefaultLocaleLongDate)
        self.timeShower.setText("     " + text)
        # 截屏并人脸识别

    def faceRecogn(self):
        if self.exLevel.currentText() == "请选择等级":
            QMessageBox.information(self, "警告", "请选择考试等级！")
        else:
            self.exLevel.setEnabled(False)
            self.assignment.setEnabled(False)
            self.print.setEnabled(False)
            self.timer_camera.stop()
            # retname:教师工号
            self.retname, top_k_idx = faceOpera.identityRecognition(comPic[:, :, ::-1], globVar.known_face_encodings,
                                                              globVar.known_face_IDs, 0.65)
            print("self.retname", self.retname)
            print("self.top_k_idx", top_k_idx)
            # name_sex只返回一个结果
            if str(self.retname) == '0':
                QMessageBox.information(self, "警告", "没有识别到人脸，请重新识别")
                self.timer_camera.start()
            else:
                self.flg = 0
                name_sex = teacher_data.search_teacher(mydb, self.retname[0])  # 查询姓名性别
                userid = name_sex[0][0]
                username = name_sex[0][1]
                # 显示至界面
                globVar.load_Face(userid)
                identityImage = QtGui.QImage('buffImage.jpg')
                fitImage = identityImage.scaled(256, 256, aspectRatioMode=Qt.KeepAspectRatio)
                self.identityView.setPixmap(QPixmap.fromImage(fitImage))
                self.nameText.setText(username)
                self.IDText.setText(userid)
                self.id_print = userid
                self.name_print = username
                self.teacher_id = name_sex[0][0]
                self.teacher_sex = name_sex[0][2]
                self.faceReco.setEnabled(False)
                self.PM_Fault.setEnabled(True)
                self.PM_True.setEnabled(True)

        # 人脸识别正确

    def messTrue(self):
        self.flg = 0
        if teacher_data.isexist_invigilator_id(mydb,self.teacher_id, self.exLevel.currentText()):
            QMessageBox.information(self, "警告", "您已经分配过考场了！")
            self.PM_Fault.setEnabled(False)
            self.PM_True.setEnabled(False)
            self.identityView.clear()
            self.nameText.clear()
            self.IDText.clear()
            self.timer_camera.start()
            self.faceReco.setEnabled(True)
        else:
            testLevel = self.exLevel.currentText()
            if testLevel == "大学英语四级考试":
                testLevel = "cet4"
            if testLevel == "大学英语六级考试":
                testLevel = "cet6"
            try:
                # （考场号，考试位置，标志）
                print("工号，性别", self.teacher_id, self.teacher_sex)
                exam, location, main_deputy = pre_assignation(mydb, testLevel, self.teacher_id,
                                                              self.teacher_sex)  # 分配考场和职位
                self.exam_print = exam
                self.location_print = location

                if (exam != None):
                    if (main_deputy):
                        self.exNumber.setText(exam)
                        self.exLocation.setText(location)
                        self.exPosition.setText("主监考")
                        self.exPosition_print = "主监考"
                        self.print.setEnabled(True)
                        self.PM_Fault.setEnabled(False)
                        self.PM_True.setEnabled(False)
                        self.assignment.setEnabled(False)
                    else:
                        self.exNumber.setText(exam)
                        self.exLocation.setText(location)
                        self.exPosition.setText("副监考")
                        self.exPosition_print = "副监考"
                        self.print.setEnabled(True)
                        self.PM_Fault.setEnabled(False)
                        self.PM_True.setEnabled(False)
                        self.assignment.setEnabled(False)
                else:
                    msg = QtWidgets.QMessageBox.information(self, u"提示", u"您已经分配考场，请前往考场准备！",
                                                            buttons=QtWidgets.QMessageBox.Ok)
                    self.identityView.clear()
                    self.nameText.clear()
                    self.IDText.clear()
                    self.timer_camera.start()
                    self.assignment.setEnabled(False)
                    self.faceReco.setEnabled(True)

            except:
                QtWidgets.QMessageBox.critical(self, u"错误", u"考场分配失败！\n请检查是否已无待分配考场！",
                                               buttons=QtWidgets.QMessageBox.Ok)

                self.identityView.clear()
                self.nameText.clear()
                self.IDText.clear()
                self.timer_camera.start()
                self.assignment.setEnabled(False)
                self.faceReco.setEnabled(True)


        # 人脸错误，重新进行人脸识别

    def messFault(self):
        print("self.flg",self.flg)
        self.flg =  self.flg+1
        if self.flg==1:
            # name_sex只返回一个结果
            name_sex = teacher_data.search_teacher(mydb, self.retname[1])  # 查询姓名性别
            userid = name_sex[0][0]
            username = name_sex[0][1]
            # 显示至界面
            globVar.load_Face(userid)
            identityImage = QtGui.QImage('buffImage.jpg')
            fitImage = identityImage.scaled(256, 256, aspectRatioMode=Qt.KeepAspectRatio)
            self.identityView.setPixmap(QPixmap.fromImage(fitImage))

            self.nameText.setText(username)
            self.IDText.setText(userid)

            self.id_print = userid
            self.name_print = username
            # self.teacher_id = userid
            self.teacher_id = name_sex[0][0]
            self.teacher_sex = name_sex[0][2]
        if self.flg == 2:
            # name_sex只返回一个结果
            name_sex = teacher_data.search_teacher(mydb, self.retname[2])  # 查询姓名性别
            userid = name_sex[0][0]
            username = name_sex[0][1]
            # 显示至界面
            globVar.load_Face(userid)
            identityImage = QtGui.QImage('buffImage.jpg')
            fitImage = identityImage.scaled(256, 256, aspectRatioMode=Qt.KeepAspectRatio)
            self.identityView.setPixmap(QPixmap.fromImage(fitImage))

            self.nameText.setText(username)
            self.IDText.setText(userid)

            self.id_print = userid
            self.name_print = username
            # self.teacher_id = userid
            self.teacher_id = name_sex[0][0]
            self.teacher_sex = name_sex[0][2]
            self.PM_Fault.setText("重新识别！")
        if self.flg == 3:
            QMessageBox.information(self, "警告", "您有可能不在教师名单！")
            self.PM_Fault.setText("身份信息错误")

            self.faceReco.setEnabled(True)
            self.PM_True.setEnabled(False)
            self.PM_Fault.setEnabled(False)
            self.identityView.clear()
            self.nameText.clear()
            self.IDText.clear()
            self.timer_camera.start()
        # 分配考场pippip
    def print_(self):
        self.assignment.setEnabled(False)

        print(self.name_print + " " + self.exam_print + " " + self.location_print + " " + self.exPosition_print)
        if self.exPosition_print == "主监考":
            b = "领卷"
        if self.exPosition_print == "副监考":
            b = "领备品"
        # file = docx.Document()
        # p = file.add_paragraph()
        # run = p.add_run(str(self.name_print) + " " + str(self.exam_print) + " " + str(self.location_print) + " " + str(self.exPosition_print))
        # file.save("test.docx")
        fo = open("教师信息.txt", "w")
        a = "                  "+self.name_print + "           " + self.exam_print + "         " + self.location_print + "        " + self.exPosition_print + "          " + b
        fo.write(" \n")
        fo.write(" \n")
        fo.write(" \n")
        fo.write(" \n")
        fo.write(" \n")
        fo.write(" \n")
        fo.write(" \n")
        fo.write(" \n")
        fo.write(" \n")
        fo.write(" \n")
        fo.write(" \n")
        fo.write(" \n")
        fo.write(" \n")
        fo.write(" \n")
        fo.write("                   "+"姓名" + "          " + "考场号" + "       " + "考场位置" + "          " + "身份" + "            " +"任务\n")
        fo.write(a)
        fo.write(" \n")
        fo.write(" \n")
        fo.write(" \n")
        fo.write(" \n")
        fo.write(" \n")
        fo.write(" \n")
        fo.write(" \n")
        fo.write(" \n")
        fo.write(" \n")
        fo.write(" \n")
        fo.write(" \n")
        fo.write(" \n")
        fo.write(" \n")
        fo.write(" \n")
        fo.write(" \n")
        fo.write(" \n")
        fo.write(" \n")
        fo.write(" \n")
        fo.write(" \n")
        fo.write(" \n")
        fo.write(" \n")
        fo.write("----------------------沿虚线撕开交给考务人员------------------\n")
        fo.write(" \n")
        fo.write(" \n")
        fo.write(" \n")
        fo.write(" \n")
        fo.write(" \n")
        fo.write(" \n")
        fo.write(" \n")
        fo.write(" \n")
        fo.write(" \n")
        fo.write(" \n")
        fo.write(" \n")
        fo.write(" \n")
        fo.write(" \n")
        fo.write(" \n")
        fo.write(" \n")
        fo.write(" \n")
        fo.write(" \n")
        fo.write(" \n")
        fo.write(
            "                   " + "姓名" + "          " + "考场号" + "       " + "考场位置" + "          " + "身份" + "            " + "任务\n")
        fo.write(a)
        fo.close()
        filename = "教师信息.txt"
        open(filename, "r")
        # 可以尝试filename中有pdf文件。
        win32api.ShellExecute(
            0,
            "print",
            filename,
            #
            # If this is None, the default printer will
            # be used anyway.
            #
            '/d:"%s"' % win32print.GetDefaultPrinter(),
            ".",
            0
        )

        self.print.setEnabled(False)
        self.PM_True.setEnabled(False)
        self.faceReco.setEnabled(True)
        self.identityView.clear()
        self.nameText.clear()
        self.IDText.clear()
        self.exNumber.setText('XXX')
        self.exLocation.setText('待分配')
        self.exPosition.setText('待分配')
        self.timer_camera.start()

    def closeEvent(self, event):
        reply = QtWidgets.QMessageBox.question(self, '警告', '您即将退出大型考试管理系统,\n您确认要退出吗？',
                                               QtWidgets.QMessageBox.Yes, QtWidgets.QMessageBox.No)
        if reply == QtWidgets.QMessageBox.Yes:
            server.stop()
            event.accept()
        else:
            event.ignore()

# 主函数
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    main = SimpleDialogForm()  # 创建一个主窗体（必须要有一个主窗体）
    main.showMaximized()  # 主窗体显示
    sys.exit(app.exec_())
