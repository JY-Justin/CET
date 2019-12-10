import database_comment
import xlwt
# 查询考场信息

def Insert_re_invigilation(mydb,values):

    set_sql = 'INSERT INTO re_invigilation values (%s,%s,%s,%s,%s)'
    database_comment.AddTable(mydb, sql_comment=set_sql, sql_val=values)


def search_all_exam(mydb, exam_table, exam_id):

    if (exam_table == 'CET4' or exam_table == 'cet4'):
        exam_table = 'cet4'
    elif (exam_table == 'CET6' or exam_table == 'cet6'):
        exam_table = 'cet6'
    exam_id = (str(exam_id),)
    sql = 'SELECT DISTINCT  * FROM ' + exam_table + ' WHERE exam_id=%s'
    val = database_comment.SearchTable(mydb, sql_comment=sql, sql_value=exam_id)
    if (len(val) == 0):
        print('没有这个考场信息')
    return val

#初始监考表
def init_invigialtion(mydb,exam_table='cet4'):

    get_sql='SELECT level,exam_id,peoples,main_invigilation,' \
            'deputy_invigilation,exam_location FROM '+ exam_table
    #print(get_sql)
    values = database_comment.SearchTable(mydb,get_sql)
    if(len(values)==0):
        print(exam_table+'表中没有信息')
    else:
        set_sql='INSERT INTO invigilation values (%s,%s,%s,%s,%s,%s)'
        database_comment.AddTable(mydb,sql_comment=set_sql,sql_val=values)


# 获取主监考池和副监考池
def get_invigilation_pool(mydb, exam_table, main_invigilation=True, deputy_invigilation=False):
    print('4')
    if (exam_table == 'CET4' or exam_table == 'cet4'):
        exam_table = 'cet4'
    elif (exam_table == 'CET6' or exam_table == 'cet6'):
        exam_table = 'cet6'

    rooms=[]
    if (main_invigilation and deputy_invigilation):
        print('只能选择一个监考位置')
    if (main_invigilation):
        #主监考为空时进行插入
        sql = 'SELECT DISTINCT  exam_id FROM '+exam_table+' WHERE main_invigilation is NULL'
        #print(sql)
        val = database_comment.SearchTable(mydb, sql_comment=sql)
        for i in val:
            if(isinstance(i,tuple)):
                rooms.append(i[0])
        return rooms
    if (deputy_invigilation):
        sql = 'SELECT DISTINCT  exam_id FROM '+exam_table+' WHERE deputy_invigilation is NULL'
        val = database_comment.SearchTable(mydb, sql_comment=sql)
        for i in val:
            if (isinstance(i, tuple)):
                rooms.append(i[0])
        return rooms
    else:
        print('必须选择一个监考位置')

#根据考场号添加考场表主副监考
def alter_exam(mydb,exam_table,exam_id,teacher_id,main_invigilation=True):

    if (exam_table == 'CET4' or exam_table == 'cet4'):
        exam_table = 'cet4'
    elif (exam_table == 'CET6' or exam_table == 'cet6'):
        exam_table = 'cet6'
    if(main_invigilation):
        sql="UPDATE "+exam_table+" SET main_invigilation= %s WHERE exam_id = %s AND main_invigilation IS NULL"
        val=(str(teacher_id),str(exam_id))
        #print(sql,val)
        rows = database_comment.AlterTable(mydb,sql_comment=sql,sql_val=val)
        if(rows!=0):
            return True
    else:
        sql = "UPDATE " + exam_table + " SET deputy_invigilation= %s WHERE exam_id = %s AND deputy_invigilation IS NULL"
        val = (str(teacher_id), str(exam_id))
        #print(sql, val)
        rows = database_comment.AlterTable(mydb, sql_comment=sql, sql_val=val)
        if (rows != 0):
            return True


#根据考场号查询主副监考
def search_invigilation(mydb,exam_table,exam_id,main_invigilation=True):
    print('6')
    if (exam_table == 'CET4' or exam_table == 'cet4'):
        exam_table = 'cet4'
    elif (exam_table == 'CET6' or exam_table == 'cet6'):
        exam_table = 'cet6'

    if(main_invigilation):
        sql="SELECT main_invigilation FROM "+ exam_table+" WHERE exam_id= %s"
        exam_id=(str(exam_id),)
        #print(sql,exam_id)
        person = database_comment.SearchTable(mydb,sql,exam_id)
        return person
    else:
        sql = "SELECT deputy_invigilation FROM " + exam_table + " WHERE exam_id= %s"
        exam_id = (str(exam_id),)
        person = database_comment.SearchTable(mydb,sql, exam_id)
        return person

#查询监考信息表
def select_invigilation_table(mydb,exam_level,exam_id):
    print('7')
    sql="SELECT * FROM invigilation WHERE level=%s AND exam_id =%s"
    val=(str(exam_level),str(exam_id))
    temp=database_comment.SearchTable(mydb,sql_comment=sql,sql_value=val)
    print(temp)

#统计监考信息
#id:教师信息
#main_i:工号
#main_n:教师姓名
#m=标志
def add_invigilation_table(mydb,id,main_i,main_n,m=True):
    print('8')
    if(m):
        sql = "UPDATE invigilation SET main_invigilation = %s,main_name=%s WHERE exam_id=%s and exam_level=%s"
    else:
        sql = "UPDATE invigilation SET deputy_invigilation = %s,deputy_name=%s WHERE exam_id=%s and exam_level=%s"
    #id[0][6]:考试地点序号
    #id[0][1]:考试类型
    vel = (main_i,main_n,id[0][6],id[0][1])

    database_comment.AlterTable(mydb,sql,vel)

#导出Excel
def Export_Excel(mydb,table,path):
    print('9')
    sql="SELECT * FROM "+table
    results=database_comment.SearchTable(mydb,sql,excel=True)
    #print(results)

    #创建Excel
    excel=xlwt.Workbook()
    sheet = excel.add_sheet("sheet1")

    #添加数据到Excel
    for field in range(len(results[0])):
        sheet.write(0,field,results[0][field][0])
        #print(results[0][field][0])

    for row in range(1,len(results[1])+1):
        for col in range(0, len(results[0])):
            #print(results[1][row - 1][col])
            sheet.write(row, col, '%s' % results[1][row - 1][col])

    excel.save(path)
#考生
#初始考生信息表


