import os
from flask import Flask, render_template, request, redirect, url_for, flash
import Getuser

app = Flask(__name__)
secret_key = os.urandom(24).hex()
app.config['SECRET_KEY'] = secret_key




# ... 其他代码将在这里添加
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        Uer = Getuser.Getuser();
        print(Uer)
        username = request.form['username']
        password = request.form['password']
        Kind = request.form['Kind']

        cort=1;

        for index in Uer.keys():
            print(index)
            if Kind ==index :
                for index1 in Uer[index].keys():
                    print(index1)
                    if Uer[index][index1] == password   :
                        cort = 0;
                        return redirect(url_for('success'))
        if cort:
                flash("账户或密码错误 请重新输入")
#TODO 报错信息 会一直显示不会消失BUG
    return render_template('login.html')


@app.route('/success')
def success():
    return 'Login successful!'


app.run(debug=True)