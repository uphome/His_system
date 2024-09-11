from flask import Blueprint, render_template, redirect, url_for, request, flash
import random
import time
import TollData
# 创建一个蓝图对象
toll_bp = Blueprint('toll_bp', __name__)


@toll_bp.route('/Toll',methods=['GET', 'POST'])
def Toll():
    if request.method == 'POST':
        if 'Setorder' in request.form:
            Name=request.form['username']
            random.seed(time.time())
            ID=random.randint(1000000, 9999999)
            Gender=request.form['gender']
            Age=request.form['age']
            DoctorID=request.form['DoctorID']
            if TollData.AddToll(ID,Name,Gender,Age,DoctorID):
                flash("挂号成功！")
            else:
                flash("挂号失败！")

    return render_template('Setorder.html')


@toll_bp.route('/Doctor')
def Doctor():
    return 'Doctor!'


@toll_bp.route('/Inspection')
def Inspection():
    return 'Inspection!'


@toll_bp.route('/Pharmacy')
def Pharmacy():
    return 'Pharmacy!'


@toll_bp.route('/superuser')
def superuser():
    return 'System superuser!'

