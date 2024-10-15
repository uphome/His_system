# 简易HIS信息系统


---
#### 项目描述：
这是一个简单的“医院挂号收费开药信息系统（Hospital Information System）简称HIS系统）”。  
具有挂号 开药 诊断等基础功能。前端界面的设计也是能看就行。 


---
#### 相关说明：
> 涉及语言：python HTML5  
> 框架搭建：Flask  
> 数据存储：SQLsever  


#### 组成部分：
整个项目由五个部分组成：*登录*，*收费*，*医生*，*检验*，*药房管理*，以及*用户管理*。

---
## 登录：

从前端获得输入的数据，然后进行逻辑判断。
逻辑判断需要判断用户名与密码是否匹配以及验证码验证。
### 判断逻辑：

```python
 Uer = UserSet.Getuser();
                username = request.form['username']
                password = request.form['password']
                Kind = request.form['Kind']
                for index in Uer.keys():
                    if Kind == index:
                        for index1 in Uer[index].keys():
                            if index1 == username and Uer[index][index1] == password:
                                url_array = ['All_bp.Toll', 
                                             'All_bp.Doctor', 
                                             'All_bp.Inspection', 
                                             'All_bp.Pharmacy',
                                             'All_bp.superuser']
                                return redirect(url_for(url_array[int(Kind)])) #输入的密码与验证码正确 则跳转到相应的板块
```

### 验证码实现：
同时需要对输入的验证码进行对比。验证码是先生成五个字符，然后根据文本生成图片。字体文件直接在网上找的。并不复杂,挡不住图片识别。

**效果如下图：**  
![img.png](C:\Users\huwang\Downloads\1728977354342.png)

**代码实现**
```python
def generate_captcha(size=(120, 40), chars=string.ascii_letters + string.digits, captcha_length=5):
    # 随机生成验证码文本
    captcha_text = ''.join(random.choice(chars) for _ in range(captcha_length))
    # 创建一个新图片
    image = Image.new('RGB', size, (255, 255, 255))
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype("chaptcha_ttf\imageCaptchaFont.ttf", 24)
    # 绘制文本
    draw.text((10, 10), captcha_text, font=font, fill=(0, 0, 0))
    #draw.text((10, 10), captcha_text, fill=(0, 0, 0))
    # 添加一些噪点
    for _ in range(25):
        draw.point((random.randint(0, size[0]), random.randint(0, size[1])), fill=(0, 0, 0))
    image = image.filter(ImageFilter.GaussianBlur(radius=1.5))
    return image, captcha_text
```

>改进：这里逻辑判断是自己写的，不过可以用**Flask**自带的这方面的，可能考虑到的情况更加的全以及安全性更高。
> 同时，验证码的字体也可以用稍微复杂的。验证方式 也可**邮件**验证码或者**短信**验证码。
> 
---
## 收费
我觉得在我现有的知识基础下，这个部分是最难写的。为了功能的写出，也是采用了不太优美的方法。  

### 挂号：
这里直接从前端获得数据之后，需要将挂号的数据写入到数据库中，使用了`pyodbc`来对
SQLsever进行读写操作。

#### 代码实现：
```python
        if 'Setorder' in request.form:
            Name = request.form['username']
            random.seed(time.time())
            ID = random.randint(1000000, 9999999) #随机病历ID
            Gender = request.form['gender']
            Age = request.form['age']
            DoctorID = request.form['DoctorID']
            if TollData.AddToll(ID, Name, Gender, Age, DoctorID):
                flash("挂号成功！")
            else:
                flash("挂号失败！")
            data = TollData.GetToll() # 写入自定义函数
            return render_template('Setorder.html', data=data)

```

#### 数据库链接：
```python

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
    except pyodbc.Error as e:
        print(f"数据库操作失败: {e}")
        # 如果出现错误，则回滚事务
        conn.rollback()
    finally:
        # 关闭Cursor和连接
        cursor.close()
        conn.close()
        return data

```
项目里类似的函数还有很多，因为，不同的功能需求需要不同的写入读取规则，很难复用。  


### 收费：
这里 思路是对存入数据库的处方进行分析，得到所开的药以及进行了那些检验项目。然后读取药品数据库的信息进行计费。
#### 代码实现
```python

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
```

这里的实现逻辑并不优雅。代码逻辑有很大的提升空间。

---

## 医生：
医生板块主要涉及到**检验申请** **开药方 写处方**。主要从前端读取输入数据，然后处理之后与数据库进行交互。

### 检验申请：
```python
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
```
不再赘述，逻辑简单。

### 写处方：
```python
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

```
这里在前端有一些java语言，就不摆出来了，在仓库中，想看的可以看看。其他的不在赘述。

### 开药方：
```python

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
```
这里的，我在读取数据之后，直接对数据库的数据进行修改了，这样的话，方便很多了，就不用在下一个板块进行修改。

## 检验：
这个板块主要是对**检验项目**的一个处理，以及对**项目结果**的输入。

**代码实现：**
```python

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
```
简单的读取数据并处理，然后在进行一个数据的输入。

## 药房：
这里主要是对存储的药房中的药品进行**数量管理**，以及药物**增加**与**删除**。
```python

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

```
内容逻辑简单，不在赘述。

## 超级用户：
这里是管理用户，用户的**注册与删除**。原本的验证阶段放到前面的登录模块做了。

```python

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
```
这里 主要是**读写数据库中的数据**并处理，然后传递给**后端**。

## 总结：
这个项目比较简单，因为实现的功能不多。虽然简单，但是这是我第一次接触到这方面，因此有很多的可以优化甚至是修改的地方。
同时，整体的代码结构需要修改，一些方法的实现可以更好。对于Flask的使用方法还需要深入，对于python 以及html5的一些语言特性也要更好的掌握。