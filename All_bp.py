import io
import re
from datetime import datetime
from flask import Blueprint, render_template,  request, flash, session, Response, jsonify
import random
import time
import Captcha_get
import GetData
import Inspection_data
import MedicineData
import TollData
import UserSet

program_price = {'核磁共振': 200, 'X光': 100, '粪便检验': 200, '血常规': 100, '血生化': 200, '凝血功能检查': 300,
                 '尿液检验': 350, '粪便检验': 400}

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
            data = TollData.GetToll()
            return render_template('Setorder.html', data=data)
    if request.method == 'GET':
        data = TollData.GetToll()
        return render_template('Setorder.html', data=data)
    return render_template('Setorder.html')


@All_bp.route('/Toll/price', methods=['GET', 'POST'])
def toll_price():
    datas_Toll = GetData.Getdata("Toll_order",
                                 ['Id', 'name', 'gender', 'age', 'docterid', 'Datetime', 'text', 'prescription',
                                  'program'])
    datas_Medicine = GetData.Getdata('Medicine_info', ['medicname', 'id', 'price', 'number'])
    patients_tuples = []
    for patient in datas_Toll:
        for key in patient:
            if key == 'Id' or key.isdigit():
                patient_id = patient[key]
                patient_name = patient['prescription']
                patients_tuples.append((patient_id, patient_name))
                break
    program_tuples = []
    for patient in datas_Toll:
        for key in patient:
            if key == 'Id' or key.isdigit():
                patient_id = patient[key]
                patient_name = patient['program']
                program_tuples.append((patient_id, patient_name))
                break
    medicines_dict = {med['medicname']: int(med['price']) for med in datas_Medicine}
    Price = []
    for i in range(0, len(program_tuples)):
        total_proprice = 0
        # TODO 这里的bug在于如果是空 会直接报错 没有验证下面这么写能不能跳过
        if program_tuples is None:
            flash('存在项目为空的状态')
            print('存在项目为空的状态1')
            break
        if program_tuples[i][1] ==None:
            flash("有人没有申请项目！")
            print('存在项目为空的状态111111')
            return render_template('Setorder.html')
        stripped_string = program_tuples[i][1].strip('-')
        project_names = stripped_string.split('-')
        for program in project_names:
            total_proprice += (program_price.get(program) * 1)
        Price.append(
            [datas_Toll[i]['Id'], datas_Toll[i]['name'], datas_Toll[i]['prescription'], datas_Toll[i]['program'],
             total_proprice])
        print('----')
        print(Price)
    for i in range(0, len(patients_tuples)):
        pattern = r'([^*]+)\*(\d+)盒'
        matches = re.findall(pattern, str(patients_tuples[i][1]))
        medicines = []
        total_mecprice = 0
        for match in matches:
            medicine_name = match[0]
            quantity = int(match[1])
            medicines.append((str(medicine_name), int(quantity)))
        for record in medicines:
            if record[0] in medicines_dict.keys():
                total_mecprice += (medicines_dict.get(record[0]) * record[1])
        Price[i][4] = int(total_mecprice) + Price[i][4]
    converted_data = []
    for item in Price:
        converted_item = {
            'Id': item[0],
            'name': item[1],
            'prescription': item[2],
            'program': item[3],
            'cost': item[4]
        }
        converted_data.append(converted_item)
    print(converted_data)
    return render_template('Setorder.html', data_price=converted_data)


@All_bp.route('/Doctor', methods=['GET', 'POST'])
def Doctor():
    # TODO: 这里 修改病历 的诊断 需要在前端的那里改，要像显示然后直接点进去可以进行修改，后端不用改。 诊断功能：添加、修改病人的诊断结果
    # TODO: 这里医生需不需要看见检验结果
    all_datas = GetData.Getdata("Toll_order", ['Id', 'name', 'gender', 'age', 'docterid', 'Datetime', 'text'])
    datas_program = GetData.Getdata("program", ['Name', 'Sex', 'Time', 'Program', 'Result', 'Id'])
    print(all_datas)
    datas = [Data for Data in all_datas if Data['text'] is None ]
    print(datas)
    if request.method == 'GET':
        return render_template('Docter.html', data=datas,programdata=datas_program)
    if request.method == 'POST':
        if 'Postorder' in request.form:
            id = request.form['Kindid']
            for data in all_datas:
                if int(id) == int(data['Id']):
                    name = data['name']
                    sex = request.form['sex']
                    time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    program = request.form['Program']
                    GetData.Adddata('Program', ['Name', 'Sex', 'Time', 'Program', 'Id'], [name, sex, time, program, id])
            add_datas = [program + '-', id]
            GetData.where_addtext('Toll_order', add_datas, 'program', 'Id', 'Onlyone')

            return render_template('Docter.html', data=datas,programdata=datas_program)
        if 'putorder' in request.form:
            result = request.form.getlist('results[]')
            if len(result) == 0:
                flash("输入为空！请重新输入")
                return render_template('Docter.html', data=datas,programdata=datas_program)
            adddata = []
            for i in range(0, len(result)):
                datas[i]['text'] = result[i]
                adddata.append([result[i], str(datas[i]['Id'])])
            if GetData.where_add("Toll_order", adddata, 'Text', 'Id') == 0:
                print("无法保存数据！")
            datas = [Data for Data in datas if Data['text'] is None]
            return render_template('Docter.html', data=datas,programdata=datas_program)






@All_bp.route('/Doctor_prescription', methods=['GET', 'POST'])
def Doctor_prescription():
    # TODO 医生开药方 应该可以多开几种药，同时能对自己开的药可以预览
    print("----------------")
    datas = GetData.Getdata("Toll_order", ['Id', 'name', 'gender', 'age', 'docterid', 'Datetime', 'text'])
    datas = [Data for Data in datas if Data['text'] is not None]
    if 'order' in request.form:
        mecnumber = request.form.getlist('results[]')
        mecid = request.form.getlist('kind[]')
        Medicine_info = session['Medicine_info']
        matched_medicines = {}
        for i, mecid_value in enumerate(mecid):
            for medicine in Medicine_info:
                if medicine['id'] == mecid_value:
                    matched_medicines[mecid_value] = [medicine['id'], medicine['medicname'], medicine['price'],
                                                      mecnumber[i]]
                    break
        all_mec = [matched_medicines[key] for key in mecid if key in matched_medicines]
        Toler = []
        for i in range(0, len(datas)):
            text = all_mec[i][1] + '*' + all_mec[i][3] + '盒——'
            Toler.append([text, datas[i]['Id']])
        GetData.where_addtext('Toll_order', Toler, 'prescription', 'Id', 'Some')
        all_mecdic = []
        # 修改库存逻辑
        for item in all_mec:
            converted_dict = {
                'MedicineName': item[1],
                'MedicineID': item[0],
                'Price': item[2],
                'Number': item[3]
            }
            all_mecdic.append(converted_dict)
        session['all_mec'] = all_mecdic
        Medicine_info = MedicineData.Get_medicine()
        for i in all_mecdic:
            update_dict = {i['MedicineID']: i['Number']}
            for medicine in Medicine_info:
                if medicine['MedicineID'] in update_dict:
                    medicine['Number'] = str(int(medicine['Number']) - int(update_dict[medicine['MedicineID']]))
        # 判断药品不足
        alter_Medicine_info = []
        for i in Medicine_info:
            if int(i['Number']) < 0:
                flash(i['MedicineName'] + '不足！还差' + str(-int(i['Number'])) + '请联系药房人员补货！')
                i['Number'] = 0
            alter_Medicine_info.append([i['Number'], i['MedicineID']])
        GetData.where_add('Medicine_info', alter_Medicine_info, 'Number', 'MedicineID')

    return render_template('Docter.html', datas=datas)


@All_bp.route('/Inspection', methods=['GET', 'POST'])
def Inspection():
    data = []
    for row in GetData.Getdata('Program', ['Name', 'Sex', 'Time', 'Program', 'Result']):
        if row['Result'] is None:
            data.append(row)
    if request.method == 'GET':
        return render_template('Inspection.html', data=data)
    if request.method == 'POST':
        if 'Setorder' in request.form:
            add_Data = {}
            result = request.form.getlist('results[]')
            if len(result) == 0:
                return render_template('Inspection.html')
            for i in range(0, len(result)):
                index = str(data[i]['Time'])
                add_Data[index] = result[i]
            if len(add_Data):
                Inspection_data.Add_inspection('Program', add_Data)
                data = []
                for row in GetData.Getdata('Program', ['Name', 'Sex', 'Time', 'Program', 'Result']):
                    if row['Result'] is None:
                        data.append(row)
                return render_template('Inspection.html', data=data)
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


@All_bp.route('/superuser',methods=['GET', 'POST'])
def superuser():
    print(request.method)
    if 'GET' == request.method:
        datas = GetData.Getdata('loginuser', ['name', 'password', 'kind'])
        dic = {0: '收费人员', 1: '医生', 2: '检验科室人员', 3: '药房人员', 4: '系统超级用户', }
        for data in datas:
            data['kind'] = dic[int(data['kind'].strip())]
            data['name'] = data['name'].strip()
            data['password'] = data['password'].strip()
        return render_template('superuser.html', datas=datas)
    if 'POST' == request.method:
        if 'signup' in request.form:
            username = request.form['username']
            password = request.form['password']
            Kind = request.form['Kind']
            if username != '' and password != '' and int(Kind) != '' and 4 >= int(Kind) >= 0:
                print('格式合格')
                if UserSet.Adduser(username, password, Kind):
                    flash("成功注册")
                    datas = GetData.Getdata('loginuser', ['name', 'password', 'kind'])
                    dic = {0: '收费人员', 1: '医生', 2: '检验科室人员', 3: '药房人员', 4: '系统超级用户', }
                    for data in datas:
                        data['kind'] = dic[int(data['kind'].strip())]
                        data['name'] = data['name'].strip()
                        data['password'] = data['password'].strip()
                    return render_template('superuser.html', datas=datas)

                else:
                    flash("注册失败")


            else:
                flash("请按照格式进行注册！")
        else:
            datas = GetData.Getdata('loginuser', ['name', 'password', 'kind'])
            dic = {0: '收费人员', 1: '医生', 2: '检验科室人员', 3: '药房人员', 4: '系统超级用户', }
            for data in datas:
                data['kind'] = dic[int(data['kind'].strip())]
                data['name'] = data['name'].strip()
                data['password'] = data['password'].strip()
    return render_template('superuser.html')


@All_bp.route('/captcha', methods=['GET'])
def show_image():
    img, text = Captcha_get.generate_captcha()
    #session['captcha_text'] = '1'
    session['captcha_text'] = text
    print(text)
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format='PNG')
    img_byte_arr = img_byte_arr.getvalue()
    return Response(img_byte_arr, mimetype='image/png')


@All_bp.route('/api/Kindname', methods=['GET'])
def get_kindname():
    datas = GetData.Getdata("Toll_order",
                            ['Id', 'name', 'gender', 'age', 'docterid', 'Datetime', 'text', 'prescription',
                             'program'])
    options_datas = []
    for data in datas:
        options_data = {}
        options_data["value"] = data["Id"]
        options_data["text"] = data["name"]
        options_datas.append(options_data)
    return jsonify(options_datas)


@All_bp.route('/api/kinds', methods=['GET'])
def get_kinds():
    session['text'] = []
    datas = GetData.Getdata('Medicine_info', ['medicname', 'id', 'price', 'number'])
    session['Medicine_info'] = datas
    options_datas = []
    for data in datas:
        options_data = {}
        options_data["value"] = data["id"]
        options_data["text"] = data["medicname"]
        options_datas.append(options_data)
    return jsonify(options_datas)
