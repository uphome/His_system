import pyodbc

def Getuser():
    conn_str = (
        r'DRIVER={ODBC Driver 17 for SQL Server};'
        r'SERVER=localhost;'  
        r'DATABASE=His_info;'
        r'Trusted_Connection=yes;'
    )
    # 创建连接
    conn = pyodbc.connect(conn_str)
    if (conn):
        print("链接成功")

    # 创建一个Cursor对象并执行SQL查询
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM dbo.loginuser')

    # 获取所有记录
    rows = cursor.fetchall()

    # 关闭Cursor和连接
    cursor.close()
    conn.close()
    # 数据预处理
    user_dic = {}
    login_dic = {};

    # 1:收费人员 2:医生 3:检验科室人员 4:药房人员 5:系统超级用户
    for row in rows:
        if (row[2].strip() == '1'):
            user_dic[row[0].strip()] = row[1].strip()
            login_dic['1'] = user_dic
            user_dic={}
        if (row[2].strip() == '2'):
            user_dic[row[0].strip()] = row[1].strip()
            login_dic['2'] = user_dic
            user_dic={}
        if (row[2].strip() == '3'):
            user_dic[row[0].strip()] = row[1].strip()
            login_dic['3'] = user_dic
            user_dic={}
        if (row[2].strip() == '4'):
            user_dic[row[0].strip()] = row[1].strip()
            login_dic['4'] = user_dic
            user_dic={}
        if (row[2].strip() == '5'):
            user_dic[row[0].strip()] = row[1].strip()
            login_dic['5'] = user_dic
            user_dic={}


    return login_dic;

print(Getuser())

