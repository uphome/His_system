import pyodbc
from datetime import datetime

def AddToll(ID, Name, Gender,Age,DocterId):
    conn_str = (
        r'DRIVER={ODBC Driver 17 for SQL Server};'
        r'SERVER=localhost;'
        r'DATABASE=His_info;'
        r'Trusted_Connection=yes;'
    )
    # 创建连接
    conn = pyodbc.connect(conn_str)
    if conn:
        print("链接成功!")
    else:
        print("链接失败!")
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    try:
        cursor = conn.cursor()
        sql = ('INSERT INTO dbo.Toll_order (ID, Name, Gender,Age,DocterId,Datatime) VALUES (?, ?, '
               '?, ?, ?,?)')
        cursor.execute(sql,(ID, Name, Gender,Age,DocterId,current_time))
        print('挂号数据成功写入!')
        conn.commit()
    except pyodbc.Error as e:
        print(f"数据库操作失败: {e}")
        conn.rollback()
        return 0
    finally:
        cursor.close()
        conn.close()
        return 1


def GetToll():
    conn_str = (
        r'DRIVER={ODBC Driver 17 for SQL Server};'
        r'SERVER=localhost;'  
        r'DATABASE=His_info;'
        r'Trusted_Connection=yes;'
    )
    # 创建连接
    conn = pyodbc.connect(conn_str)
    if conn:
        print("链接成功!")
    else:
        print("链接失败!")

    # 创建一个Cursor对象并执行SQL查询
    try:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM dbo.Toll_order')
        # 获取所有记录
        rows = cursor.fetchall()
        data=[]
        for row in rows:
            data.append({'ID': row[0], 'Name': row[1], 'Gender':row[2], 'Age': row[3], 'DoctorId': row[4],'current_time':row[5]})


        # 数据预处理

        # 1:收费人员 2:医生 3:检验科室人员 4:药房人员 5:系统超级用户
    except pyodbc.Error as e:
        print(f"数据库操作失败: {e}")
        # 如果出现错误，则回滚事务
        conn.rollback()
    finally:
        # 关闭Cursor和连接
        cursor.close()
        conn.close()
        return data
