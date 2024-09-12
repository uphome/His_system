import os
from flask import Flask, render_template, request, redirect, url_for, flash
import UserSet
from Toll import toll_bp

app = Flask(__name__)
secret_key = os.urandom(24).hex()
app.config['SECRET_KEY'] = secret_key
app.register_blueprint(toll_bp)


# ... 其他代码将在这里添加
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if 'signin' in request.form:
            Uer = UserSet.Getuser();
            username = request.form['username']
            password = request.form['password']
            Kind = request.form['Kind']
            print(Kind)

            for index in Uer.keys():
                if Kind == index:
                    for index1 in Uer[index].keys():
                        if index1 == username and Uer[index][index1] == password:
                            url_array=['toll_bp.Toll','toll_bp.Doctor','toll_bp.Inspection','toll_bp.Pharmacy','toll_bp.superuser']
                            return redirect(url_for(url_array[int(Kind)]))


            flash("账户或密码错误 请重新输入")
        if 'signup' in request.form:
            username = request.form['username']
            password = request.form['password']
            Kind = request.form['Kind']

            if username != '' and password != '' and int(Kind) != '' and 5 >= int(Kind) >= 1:
                if UserSet.Adduser(username, password, Kind):
                    flash("成功注册")
                else:
                    flash("注册失败")


            else:
                flash("请按照格式进行注册！")

    return render_template('login.html')


app.run(debug=True)
