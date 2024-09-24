import pyodbc


def Add_inspection(Dataname,  AddData):
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
        sql_update = (' UPDATE dbo.' + Dataname + ' SET Result = ? WHERE Time = ?  ')
        for data ,values in AddData.items():
            cursor.execute(sql_update, [values,data])
            conn.commit()
        print('挂号数据成功写入!')

    except pyodbc.Error as e:
        print(f"数据库操作失败: {e}")
        conn.rollback()
        return 0
    finally:
        cursor.close()
        conn.close()
        return 1