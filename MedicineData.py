from datetime import datetime

import pyodbc

import GetData


def Get_medicine():
    data = GetData.Getdata('Medicine_info', ['MedicineName', 'MedicineID', 'Price', 'Number'])
    return data
def Add_medicine():
    return 0
def Alter_medicine(AddData): #特殊函数
    Dataname='Medicine_info'
    Kindname=['MedicineName', 'MedicineID', 'Price', 'Number']
    conn_str = (
        r'DRIVER={ODBC Driver 17 for SQL Server};'
        r'SERVER=localhost;'
        r'DATABASE=His_info;'
        r'Trusted_Connection=yes;'
    )
    # 创建连接
    conn = pyodbc.connect(conn_str)
    if conn != 1:
        print("链接失败!")
    try:
        cursor = conn.cursor()
        sql1 = sql2 = sql3 = ''

        for i in range(0, len(Kindname) - 1):
            sql1 = sql1 + Kindname[i] + ','
            sql2 = '?,' + sql2
            sql3 = sql3 + '\'' + AddData[i] + '\','
        sql1 = sql1 + Kindname[-1]
        sql2 = sql2 + '?'
        sql3 = sql3 + '\'' + AddData[-1] + '\''
        sql = ('INSERT INTO dbo.' + Dataname + ' (' + sql1 + ') VALUES (' + sql2 + ')')
        str = ('MERGE INTO dbo.' + Dataname + ' AS target USING (VALUES (' + sql3 + ')) AS source (MedicineID, MedicineName, Price, Number) ON target.MedicineID = source.MedicineID WHEN MATCHED THEN UPDATE SET MedicineName = source.MedicineName, Price = source.Price, Number = source.Number WHEN NOT MATCHED THEN INSERT (MedicineID, MedicineName, Price, Number) VALUES (source.MedicineID, source.MedicineName, source.Price, source.Number);')

        cursor.execute(str)
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
