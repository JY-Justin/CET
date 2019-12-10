import database_comment

#查询预监考教师是否已分配考场
def select_pre_teacher_flag(mydb, exam_level, teacher_id):
    sql = "SELECT flag FROM pre_invigilation WHERE job_id = %s AND exam_level = %s"
    values = (teacher_id, exam_level)
    return database_comment.SearchTable(mydb, sql, values)
#查询该教师是否在教师表中
def isexist_teacher(mydb, teacher_id):
    sql = "SELECT 1 FROM teacher WHERE job_id = %s limit 1"
    return database_comment.SearchTable(mydb, sql, teacher_id)
#根据教师工号查询是否在监考表中
def isexist_invigilator_id(mydb, teacher_id, exam_level):
    msg = ((exam_level, str(teacher_id), str(teacher_id)))
    sql = "SELECT 1 FROM invigilation WHERE exam_level = %s AND (main_invigilation = %s OR deputy_invigilation = %s)"
    return database_comment.SearchTable(mydb, sql, msg)
#添加监考教师与替换监考教师信息
def insert_invigilator_information(mydb, msg):
    sql = "INSERT INTO re_invigilation VALUES (%s,%s,%s,%s,%s)"
    database_comment.AddTable(mydb, sql_comment=sql, sql_val=msg)
#根据姓名查询监考者工号
def select_invigilator_id_and_name_by_name(mydb, values=None):
    sql = "SELECT job_id, teacher_name FROM pre_invigilation WHERE exam_level = %s AND teacher_name = %s AND flag = 0"
    return database_comment.SearchTable(mydb, sql, values)




#查询教师表中所有信息
def search_teacher_all(mydb):
    sql="SELECT DISTINCT * FROM teacher"
    return database_comment.SearchTable(mydb,sql)


#由工号查询预先确定的监考人员名单
def search_pre_invigilation_teacher(mydb,job_id=None):
    if (job_id == None):
        print("工号为空")
        return
    sql = "SELECT DISTINCT  * FROM pre_invigilation WHERE job_id=%s "
    print("1")
    job_id = (str(job_id))
    print("2")
    # print(job_id)
    return database_comment.SearchTable(mydb, sql, job_id)

#由工号查询教师姓名、性别
def search_teacher(mydb,job_id=None):
    if(job_id==None):
        print("工号为空")
        return
    sql="SELECT DISTINCT  * FROM teacher WHERE job_id=%s"
    job_id=(str(job_id),)
    #print(job_id)
    return  database_comment.SearchTable(mydb,sql,job_id)

#添加教师
def add_teacher(mydb,job_id=None,name=None,sex='男'):
    is_have=search_teacher(mydb,job_id=job_id)
    if (len(is_have)!=0):
        print("该工号已存在")
    elif(job_id==None):
        print("工号不能为空")
    else:
        sql='INSERT INTO teacher VALUES (%s,%s,%s)'
        # values=(job_id,name,sex)
        values=[]
        values.append(job_id)
        values.append(name)
        values.append(sex)
        values=tuple(values)
        v=[]
        v.append(values)
        print(v)
        database_comment.AddTable(mydb,sql_comment=sql,sql_val=v)

#删除教师
def delete_teacher(mydb,job_id=None):
    is_have = search_teacher(mydb, job_id=job_id)
    if (len(is_have) == 0):
        print("该工号不存在")
    elif (job_id == None):
        print("工号不能为空")
    else:
        sql='DELETE  FROM teacher WHERE job_id=%s'
        job_id=[job_id]
        database_comment.DeleteTable(mydb,sql_comment=sql,sql_val=job_id)

#delete_teacher(mydb,job_id='2356')

