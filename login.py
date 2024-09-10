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
        #print('数据库数据为：')
        #print(Uer)
        username = request.form['username']
        password = request.form['password']
        index=1;
        for key in Uer.keys():
            if key == username and Uer[username] == password:
                # 登录成功，这里只是简单重定向到根URL，实际应用中可能需要设置会话等
                index = 0;
                return redirect(url_for('success'))
        if index:
                flash("账户或密码错误 请重新输入")

    return render_template('login.html')


@app.route('/success')
def success():
    return 'Login successful!'


app.run(debug=True)