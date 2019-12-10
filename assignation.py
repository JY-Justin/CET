import teacher_data
import exam_information
import numpy as np
import database_comment


#分配算法

def assignation(mydb,exam_table,teacher_id,teacher_sex):
    main_pool=exam_information.get_invigilation_pool(mydb,exam_table,main_invigilation=True,deputy_invigilation=False)
    deputy_pool=exam_information.get_invigilation_pool(mydb,exam_table,main_invigilation=False,deputy_invigilation=True)
    #print(main_pool)
    np.random.shuffle(main_pool)
    np.random.shuffle(deputy_pool)
    if (teacher_sex == '男' and len(deputy_pool) != 0 or teacher_sex == '女' and len(main_pool) == 0):

        exam_id = np.random.choice(deputy_pool)
        IsAchive = exam_information.alter_exam(mydb,exam_table=exam_table,exam_id=exam_id,
                                    teacher_id=teacher_id,main_invigilation=False)
        if(IsAchive):
            return exam_id,False

    elif (teacher_sex == '男' and len(deputy_pool) == 0 or teacher_sex == '女' and len(main_pool) != 0):

        exam_id = np.random.choice(main_pool)
        IsAchive = exam_information.alter_exam(mydb, exam_table=exam_table, exam_id=exam_id,
                                    teacher_id=teacher_id, main_invigilation=True)
        if (IsAchive):
            return exam_id,True

    else:
        print('the room is empty')

#预分配，防止多次分配
def pre_assignation(mydb,exam_table,teacher_id,teacher_sex):
    if (exam_table == 'CET4' or exam_table == 'cet4'):
        exam_table = 'cet4'
    elif (exam_table == 'CET6' or exam_table == 'cet6'):
        exam_table = 'cet6'

    sql='SELECT exam_id FROM '+exam_table+' WHERE main_invigilation=%s OR deputy_invigilation=%s'
    sql_val=(str(teacher_id),str(teacher_id))
    results=database_comment.SearchTable(mydb,sql,sql_val)

    if(len(results)==0):
       exam,main_deputy = assignation(mydb=mydb, exam_table=exam_table, teacher_id=teacher_id, teacher_sex=teacher_sex)
       if(exam!=None):
           exam_select=exam_information.search_all_exam(mydb,exam_table,exam)
           location=exam_select[0][10]
           tes = teacher_data.search_teacher(mydb,teacher_id)
           exam_information.add_invigilation_table(mydb,exam_select,teacher_id,tes[0][1],main_deputy)
           return exam,location,main_deputy
    return None,False,None

#删除某一考场主或副监考
def delete_addignation(mydb,exam_table,exam_id,main_invigilation=True):
    person=exam_information.search_invigilation(mydb,exam_table,exam_id,main_invigilation)
    if(person=="" and main_invigilation):
        print('这个考场还没有主监考老师')
    elif(person=="" and not main_invigilation):
        print('这个考场还没有副监考老师')
    else:
        exam_information.alter_exam(mydb, exam_table=exam_table, exam_id=exam_id,
                                    teacher_id="", main_invigilation=main_invigilation)

#main
def start(mydb):
    person=teacher_data.search_teacher_all(mydb)
    for i in person:
        assignation(mydb, exam_table='cet4', id=i[0], sex=i[2])
    #assignation(mydb,exam_table='cet4',id=person[0][0],sex=person[0][2])
    #delete_addignation(mydb,'cet4','061',True)

#start(mydb)
#exam_information.select_invigilation_table(mydb,'大学英语四级考试','001')
#exam_information.add_invigilation_table(mydb,'cet4')
#exam_information.Export_Excel(mydb,'invigilation','a.xls')