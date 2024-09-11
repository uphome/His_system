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
            print(Uer)
            username = request.form['username']
            password = request.form['password']
            Kind = request.form['Kind']
            cort = 1;

            for index in Uer.keys():
                if Kind == index:
                    for index1 in Uer[index].keys():
                        if index1 == username and Uer[index][index1] == password:
                            cort = 0;

                            # TODO 不同的kind对应着不同的界面
                            if int(Kind) == 1:
                                return redirect(url_for('toll_bp.Toll'))
                            if int(Kind) == 2:
                                return redirect(url_for('toll_bp.Doctor'))
                            if int(Kind) == 3:
                                return redirect(url_for('toll_bp.Inspection'))
                            if int(Kind) == 4:
                                return redirect(url_for('toll_bp.Pharmacy'))
                            if int(Kind) == 5:
                                return redirect(url_for('toll_bp.superuser'))
            if cort:
                flash("账户或密码错误 请重新输入")
        if 'signup' in request.form:
            username = request.form['username']
            password = request.form['password']
            Kind = request.form['Kind']

            if username != '' and password != '' and int(Kind) != '' and 5 >= int(Kind) >= 1:
                if UserSet.Adduser(username,password,Kind):
                    flash("成功注册")
                else:
                    flash("注册失败")


            else:flash("请按照格式进行注册！")

    return render_template('login.html')
app.run(debug=True)