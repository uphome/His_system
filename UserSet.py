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
        print("链接成功!")
    else:
        print("链接失败!")

    # 创建一个Cursor对象并执行SQL查询
    try:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM dbo.loginuser')
        # 获取所有记录
        rows = cursor.fetchall()
        # 数据预处理
        login_dic = {'1':{},'2':{},'3':{},'4':{},'5':{}};
        for row in rows:
           login_dic[row[2].strip()][row[0].strip()] = row[1].strip()
        # 1:收费人员 2:医生 3:检验科室人员 4:药房人员 5:系统超级用户
    except pyodbc.Error as e:
        print(f"数据库操作失败: {e}")
        # 如果出现错误，则回滚事务
        conn.rollback()
    finally:
        # 关闭Cursor和连接
        cursor.close()
        conn.close()
        return login_dic


def Adduser(Username, Password, Kind):
    conn_str = (
        r'DRIVER={ODBC Driver 17 for SQL Server};'
        r'SERVER=localhost;'
        r'DATABASE=His_info;'
        r'Trusted_Connection=yes;'
    )
    # 创建连接
    conn = pyodbc.connect(conn_str)
    if (conn):
        print("链接成功！")
    else:
        print("链接失败！")

    # 创建一个Cursor对象并执行SQL查询
    try:
        cursor = conn.cursor()
        sql = 'INSERT INTO dbo.loginuser (Username, Password, Kind) VALUES (?, ?, ?)'
        cursor.execute(sql,(Username, Password, Kind))
        print('注册数据成功写入!')
        conn.commit()
    except pyodbc.Error as e:
        print(f"数据库操作失败: {e}")
        # 如果出现错误，则回滚事务
        conn.rollback()
        return 0
    finally:
        cursor.close()
        conn.close()
        return 1

print(Getuser())