from TCPServer import *
from assignation import *
import database_comment
import teacher_data
import numpy as np
from time import sleep
from PyQt5 import QtCore, QtGui, QtWidgets

def teachers_id():
    results = teacher_data.search_teacher_all(mydb)
    teachers = []
    for i in results:
        teachers.append(i[0])
    return teachers

def teacher_male():
    teachers = teachers_id()
    teacher = np.random.choice(teachers)   # 随机选取教师
    name_sex = teacher_data.search_teacher(mydb, teacher)  # 查询姓名性别
    print(name_sex)
    if(len(name_sex[0][2])==0):
        name_sex[0][2] = '男'
    exam, location, main_deputy = pre_assignation(mydb, 'cet4', teacher,  name_sex[0][2])
    if (exam != None):
        if(main_deputy):
            ptr = name_sex[0][1] + ' 作为主监考员被分配到 ' + exam + ' 考场'
            print(ptr)
        else:
            ptr = name_sex[0][1] + ' 作为副监考员被分配到 ' + exam + ' 考场'
            print(ptr)

def teacher_female():
    teachers = teachers_id()
    teacher = np.random.choice(teachers)  # 随机选取教师
    print(teacher)
    name_sex = teacher_data.search_teacher(mydb, teacher)  # 查询姓名性别
    if (len(name_sex[0][2]) == 0):
        name_sex[0][2] = '男'
        exam, location, main_deputy = assignation.pre_assignation(mydb, 'cet4', teacher, name_sex[0][2])
    if (exam != None):
        if (main_deputy):
            ptr = name_sex[0][1] + ' 作为主监考员被分配到 ' + exam + ' 考场'
            print(ptr)
        else:
            ptr = name_sex[0][1] + ' 作为副监考员被分配到 ' + exam + ' 考场'
            print(ptr)

if __name__ == '__main__':
    timer_t1 = QtCore.QTimer()
    timer_t2 = QtCore.QTimer()
    timer_t1.timeout.connect(lambda:teacher_male())
    timer_t2.timeout.connect(lambda:teacher_female())
    timer_t1.start(60)
    timer_t2.start(40)

