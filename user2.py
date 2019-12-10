from TCPServer import *
from assignation import *
import database_comment
import teacher_data
import exam_information

from time import sleep
import numpy as np

def teachers_id():
    results=teacher_data.search_teacher_all(mydb)
    teachers=[]
    for i in results:
        teachers.append(i[0])
    return teachers

if __name__ == '__main__':
    teachers=teachers_id()
    #print(teachers)
    for i in range(1000):
        teacher= np.random.choice(teachers)#随机选取教师
        #print(teacher)
        name_sex=teacher_data.search_teacher(mydb,teacher)#查询姓名性别
        #print(name_sex)
        exam,main_deputy = pre_assignation(mydb,'cet4',teacher,name_sex[0][2])#分配考场和职位
        if(exam!=None):
            if(main_deputy):
                ptr = name_sex[0][1] + ' 作为主监考员被分配到 ' + exam + ' 考场'
                print(ptr)
            else:
                ptr = name_sex[0][1] + ' 作为副监考员被分配到 ' + exam + ' 考场'
                print(ptr)
        sleep(5)