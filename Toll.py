import io

from flask import Blueprint, render_template, redirect, url_for, request, flash, session, Response
import random
import time

import Captcha_get
import TollData
from datetime import datetime

# 创建一个蓝图对象
All_bp = Blueprint('All_bp', __name__)


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
            data = TollData.GetToll();
            return render_template('Setorder.html', data=data)
    return render_template('Setorder.html')


@All_bp.route('/Doctor')
def Doctor():
    return 'Doctor!'


@All_bp.route('/Inspection')
def Inspection():
    return 'Inspection!'


@All_bp.route('/Pharmacy')
def Pharmacy():
    return 'Pharmacy!'


@All_bp.route('/superuser')
def superuser():
    return 'System superuser!'


@All_bp.route('/captcha', methods=['GET'])
def show_image():
    img, session['captcha_text'] = Captcha_get.generate_captcha()
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format='PNG')
    img_byte_arr = img_byte_arr.getvalue()
    return Response(img_byte_arr, mimetype='image/png')
