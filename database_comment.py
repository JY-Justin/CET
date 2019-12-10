import xlrd
def SearchTable(database, sql_comment, sql_value=None, excel=False):
    mycursor = database.cursor()
    # sql = "SELECT * FROM sites WHERE name = %s"
    # na = ("RUNOOB",)
    if (sql_value == None):
        mycursor.execute(sql_comment)
    else:
        mycursor.execute(sql_comment, sql_value)
    myresult = mycursor.fetchall()
    return myresult
    if (excel):
        fields = mycursor.description
        return fields, myresult
    else:
        value = []
        for x in myresult:
            value.append(x)
        print(myresult)
        database.commit()
        return myresult


def AddTable(database, sql_comment, sql_val):
    mycursor = database.cursor()
    # sql = "INSERT INTO sites (name, url) VALUES (%s, %s)"
    # val = [
    #     ('Google', 'https://www.google.com'),
    #     ('Github', 'https://www.github.com'),
    #     ('Taobao', 'https://www.taobao.com'),
    #     ('stackoverflow', 'https://www.stackoverflow.com/')
    # ]
    print("sql_val：",sql_val)
    #print(len(sql_val))
    if (len(sql_val) > 1):
        print("传进去数据个数",len(sql_val),sql_val)
        try:
            mycursor.executemany(sql_comment, sql_val)
        except:
            print('主键冲突')
    else:
        print(len(sql_val), sql_val[0])
        try:
            mycursor.execute(sql_comment, sql_val[0])
        except:
            print('主键冲突')

    database.commit()  # 数据表内容有更新，必须使用到该语句
    #print(mycursor.rowcount, "记录插入成功。")


def DeleteTable(database, sql_comment, sql_val=None):
    mycursor = database.cursor()
    # sql = "DELETE FROM sites WHERE name = %s"
    # na = ("stackoverflow",)
    mycursor.execute(sql_comment, sql_val)
    database.commit()
    #print(mycursor.rowcount, " 条记录删除")


def AlterTable(database, sql_comment, sql_val):
    mycursor = database.cursor()
    # sql = "UPDATE sites SET name = %s WHERE name = %s"
    # val = ("Zhihu", "ZH")
    try:

        mycursor.execute(sql_comment, sql_val)

    except Exception as e:
        print('修改失败:{}'.format(e))
    database.commit()
    #print(mycursor.rowcount, " 条记录被修改")
    return mycursor.rowcount


def excelTOmysql(mydb, table, file, Append=False):
    if(Append):
        sql="DELETE FROM " + table
        DeleteTable(mydb,sql)
    sql = "SELECT * FROM  " + table
    results = SearchTable(mydb, sql, excel=True)
    listnames = []
    for field in range(len(results[0])):
        listnames.append(results[0][field][0])

    workbook = xlrd.open_workbook(file)
    worksheet = workbook.sheet_by_name(workbook.sheet_names()[0])
    if (worksheet.row_values(0) == listnames):
        rows = worksheet.nrows
        cols = worksheet.ncols
        sql_values = []

        for i in range(1, rows):
            row_values = worksheet.row_values(i)
            row_values = tuple(row_values)
            sql_values.append(row_values)
        s = '('
        for j in range(cols - 1):
            s = s + '%s,'
        s = s + '%s)'
        sql = 'INSERT INTO  ' + table + ' VALUES  ' + s
        print(sql)
        AddTable(mydb, sql, sql_values)
