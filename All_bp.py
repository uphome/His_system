import io

from flask import Blueprint, render_template, redirect, url_for, request, flash, session, Response
import random
import time

import Captcha_get
import GetData
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


@All_bp.route('/Doctor')
def Doctor():
    return 'Doctor!'


@All_bp.route('/Inspection')
def Inspection():
    return 'Inspection!'


@All_bp.route('/Pharmacy', methods=['GET', 'POST'])
def Pharmacy():
    if request.method == 'POST':
        if 'Medicinealter' in request.form: #修改库存
            #Kindname = ['MedicineID', 'MedicineName', 'Price', 'Number']
            medicineName=request.form['MedicineName']
            medicineID = request.form['MedicineID']
            #TODO ID自动生成
            medicinePrice = str(request.form['Price'])
            medicineNumber = request.form['Number']
            addData=[medicineID,medicineName,medicinePrice,medicineNumber]
            MedicineData.Alter_medicine(addData)
            data = MedicineData.Get_medicine()
            return render_template('Pharmacy.html', data=data)
    if request.method == 'GET': #显示库存
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
