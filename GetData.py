from datetime import datetime

import pyodbc


# TODO 将大部分的写入数据库的函数写成一个
def Getdata(Dataname, Kindname):
    conn_str = (
        r'DRIVER={ODBC Driver 17 for SQL Server};'
        r'SERVER=localhost;'
        r'DATABASE=His_info;'
        r'Trusted_Connection=yes;'
    )
    # 创建连接
    conn = pyodbc.connect(conn_str)

    # 创建一个Cursor对象并执行SQL查询
    try:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM dbo.' + Dataname)
        # 获取所有记录
        rows = cursor.fetchall()
        data = []
        appendix = {}
        for row in rows:
            for i in range(0, len(Kindname)):
                appendix[Kindname[i]] = row[i]
            data.append(appendix)
            appendix = {}
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


# Getdata('Medicine_info', ['MedicineName', 'MedicineID', 'Price', 'Number'])
def where_add(Dataname, AddDatas,Set,Where):
    conn_str = (
        r'DRIVER={ODBC Driver 17 for SQL Server};'
        r'SERVER=localhost;'
        r'DATABASE=His_info;'
        r'Trusted_Connection=yes;'
    )
    # 创建连接
    conn = pyodbc.connect(conn_str)
    if (conn == 1):
        print("链接成功!")
    try:
        cursor = conn.cursor()
        sql = ('UPDATE '+ Dataname+ ' SET '+Set+' = ?  WHERE '+Where+' = ?')
        for AddData in AddDatas:
            cursor.execute(sql, AddData)
        print('数据成功写入!')
        conn.commit()
    except pyodbc.Error as e:
        print(f"数据库操作失败: {e}")
        conn.rollback()
        return 0
    finally:
        cursor.close()
        conn.close()
        return 1


def where_addtext(dataname, add_datas,set_field,  where_field,index):
    conn_str = (
        r'DRIVER={ODBC Driver 17 for SQL Server};'
        r'SERVER=localhost;'
        r'DATABASE=His_info;'
        r'Trusted_Connection=yes;'
    )
    try:
        # 创建连接
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()

        # 构造SQL更新语句

        sql = f"""  
                    UPDATE {dataname}  
                    SET {set_field} = ISNULL({set_field}, '') + ?  
                    WHERE {where_field} = ?  
                    """

        # 执行批量更新
        if index == "Some":
            for append_text, condition_value in add_datas:
               cursor.execute(sql, (append_text, condition_value))
        if index == "Onlyone":
            cursor.execute(sql, add_datas)
        # 提交事务
        conn.commit()
        print('数据成功写入!')
        return 1  # 表示操作成功

    except pyodbc.Error as e:
        print(f"数据库操作失败: {e}")
        conn.rollback()  # 回滚事务
        return 0  # 表示操作失败

    finally:
        # 关闭游标和连接
        cursor.close()
        conn.close()

def Adddata(Dataname, Kindname, AddData):
    conn_str = (
        r'DRIVER={ODBC Driver 17 for SQL Server};'
        r'SERVER=localhost;'
        r'DATABASE=His_info;'
        r'Trusted_Connection=yes;'
    )
    # 创建连接
    conn = pyodbc.connect(conn_str)
    if (conn == 1):
        print("链接成功!")
    try:
        cursor = conn.cursor()
        sql1 = sql2 =sql3= ''

        for i in range(0, len(Kindname) - 1):
            sql1 = sql1 + Kindname[i] + ','
            sql2 = '?,' + sql2
            sql3 = sql3 + '\''+AddData[i] +'\','
        sql1 = sql1 + Kindname[-1]
        sql2 = sql2 + '?'
        sql3 = sql3 + '\''+AddData[-1] +'\''
        sql = ('INSERT INTO dbo.' + Dataname + ' (' + sql1 + ') VALUES (' + sql2 + ')')
        print(sql3)
        cursor.execute(sql,AddData)
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
