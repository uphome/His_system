import os
from flask import Flask, render_template, request, redirect, url_for, flash
import Getuser
from Toll import toll_bp

app = Flask(__name__)
secret_key = os.urandom(24).hex()
app.config['SECRET_KEY'] = secret_key
app.register_blueprint(toll_bp)



# ... 其他代码将在这里添加
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        Uer = Getuser.Getuser();
        print(Uer)
        username = request.form['username']
        password = request.form['password']
        Kind = request.form['Kind']
        print(request.form)


        cort=1;

        for index in Uer.keys():
            if Kind ==index :
                for index1 in Uer[index].keys():
                    if index1 ==username and Uer[index][index1] == password   :
                        cort = 0;

                        #TODO 不同的kind对应着不同的界面
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
#TODO 报错信息 会一直显示不会消失BUG
    return render_template('login.html')



app.run(debug=True)