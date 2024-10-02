import io
from datetime import datetime

from flask import Blueprint, render_template, redirect, url_for, request, flash, session, Response
import random
import time

import Captcha_get
import GetData
import Inspection_data
import MedicineData
import TollData

# 创建一个蓝图对象
All_bp = Blueprint('All_bp', __name__)


# 1:收费人员 2:医生 3:检验科室人员 4:药房人员 5:系统超级用户

@All_bp.route('/Toll', methods=['GET', 'POST'])
def Toll():
    if request.method == 'POST':
        if 'Setorder' in request.form:
            Name = request.form['username']
            random.seed(time.time())
            ID = random.randint(1000000, 9999999)
            Gender = request.form['gender']
            Age = request.form['age']
            DoctorID = request.form['DoctorID']
            if TollData.AddToll(ID, Name, Gender, Age, DoctorID):
                flash("挂号成功！")
            else:
                flash("挂号失败！")
            # data=GetData.Getdata('Toll_order',['ID', 'Name', 'Gender', 'Age', 'DoctorId','current_time'])
            data = TollData.GetToll()
            return render_template('Setorder.html', data=data)
    if request.method == 'GET':
        data = TollData.GetToll()
        return render_template('Setorder.html', data=data)
    return render_template('Setorder.html')


@All_bp.route('/Doctor', methods=['GET', 'POST'])
def Doctor():
    #TODO: 这里 修改病历 的诊断 需要在前端的那里改，要像显示然后直接点进去可以进行修改，后端不用改。 诊断功能：添加、修改病人的诊断结果
    datas = GetData.Getdata("Toll_order",['Id','name','gender','age','docterid','Datetime','text'])
    datas = [Data for Data in datas if Data['text'] is None]
    if request.method == 'GET':
        return render_template('Docter.html',data=datas)
    if request.method == 'POST':
        if 'Postorder' in request.form:
            name = request.form['username']
            sex = request.form['sex']
            time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            program = request.form['Program']
            GetData.Adddata('Program', ['Name', 'Sex', 'Time', 'Program'], [name, sex, time, program])
            return render_template('Docter.html',data=datas)
        if 'putorder' in request.form:
            result = request.form.getlist('results[]')
            if len(result) == 0:
                flash("输入为空！请重新输入")
                return render_template('Docter.html',data=datas)
            adddata = []
            for i in range(0, len(result)):
                datas[i]['text']=result[i]
                adddata.append([result[i], str(datas[i]['Id'])])
            if GetData.where_add("Toll_order",adddata) == 0:
                print("无法保存数据！")
            datas = [Data for Data in datas if Data['text'] is None]
            return render_template('Docter.html', data=datas)
@All_bp.route('/Inspection', methods=['GET', 'POST'])
def Inspection():
    data = []
    for row in GetData.Getdata('Program', ['Name', 'Sex', 'Time', 'Program', 'Result']):
        if row['Result'] is None:
            data.append(row)
    if request.method=='GET':
        return render_template('Inspection.html', data=data)
    if request.method=='POST':
        if 'Setorder' in request.form:
            add_Data = {}
            result = request.form.getlist('results[]')
            if len(result)== 0:
                return render_template('Inspection.html')
            print(result)
            for i in range(0, len(result)):
                index = str(data[i]['Time'])
                add_Data[index] = result[i]
            if len(add_Data):
                Inspection_data.Add_inspection('Program', add_Data)
                data=[]
                for row in GetData.Getdata('Program', ['Name', 'Sex', 'Time', 'Program', 'Result']):
                    if row['Result'] is None:
                        data.append(row)
                return render_template('Inspection.html',data=data)
    return render_template('Inspection.html', data=data)


@All_bp.route('/Pharmacy', methods=['GET', 'POST'])
def Pharmacy():
    if request.method == 'POST':
        if 'Medicinealter' in request.form:  # 修改库存
            # Kindname = ['MedicineID', 'MedicineName', 'Price', 'Number']
            medicineName = request.form['MedicineName']
            medicineID = request.form['MedicineID']
            medicinePrice = str(request.form['Price'])
            medicineNumber = request.form['Number']
            addData = [medicineID, medicineName, medicinePrice, medicineNumber]
            MedicineData.Alter_medicine(addData)
            data = MedicineData.Get_medicine()
            return render_template('Pharmacy.html', data=data)
    if request.method == 'GET':  # 显示库存
        data = MedicineData.Get_medicine()
        return render_template('Pharmacy.html', data=data)
    return render_template('Pharmacy.html')


@All_bp.route('/superuser')
def superuser():
    return 'System superuser!'


@All_bp.route('/captcha', methods=['GET'])
def show_image():
    img, text = Captcha_get.generate_captcha()
    session['captcha_text'] = '1'
    # session['captcha_text'] = text
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format='PNG')
    img_byte_arr = img_byte_arr.getvalue()
    return Response(img_byte_arr, mimetype='image/png')
