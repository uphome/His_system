import pyodbc

def Getuser():
    conn_str = (
        r'DRIVER={ODBC Driver 17 for SQL Server};'
        r'SERVER=localhost;'  # 或者只是服务器名，如果未使用命名实例  
        r'DATABASE=His_info;'
        r'Trusted_Connection=yes;'
    )
    # 创建连接
    conn = pyodbc.connect(conn_str)
    if (conn):
        print("链接成功")

    # 创建一个Cursor对象并执行SQL查询
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM dbo.login_info')

    # 获取所有记录
    rows = cursor.fetchall()

    # 关闭Cursor和连接
    cursor.close()
    conn.close()
    user_dic = {}
    for row in rows:
        user_dic[row[0].strip()] = row[1].strip()
    return user_dic;




