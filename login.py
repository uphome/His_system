import io
import os
from flask import Flask, render_template, request, redirect, url_for, flash, Response, session, send_from_directory
import UserSet
from All_bp import All_bp

app = Flask(__name__)
secret_key = os.urandom(24).hex()
app.config['SECRET_KEY'] = secret_key
app.register_blueprint(All_bp)
#TODO 整体代码结构要调整
#TODO 添加装饰器 用来判断用户是否有权限进入该网页
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if 'signin' in request.form:
            if request.form['captcha'] == session['captcha_text']:
                Uer = UserSet.Getuser();
                username = request.form['username']
                password = request.form['password']
                Kind = request.form['Kind']
                for index in Uer.keys():
                    if Kind == index:
                        for index1 in Uer[index].keys():
                            if index1 == username and Uer[index][index1] == password:
                                url_array = ['All_bp.Toll', 'All_bp.Doctor', 'All_bp.Inspection', 'All_bp.Pharmacy',
                                             'All_bp.superuser']
                                return redirect(url_for(url_array[int(Kind)]))

            flash("输入信息错误 请重新输入")
    if request.method == 'GET':
        return render_template('login.html')
    return render_template('login.html')


@app.route('/favicon.ico')  # 设置icon
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),  # 对于当前文件所在路径,比如这里是static下的favicon.ico
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')



#TODO 用局域网其他设备都可以访问
#app.run(host='10.150.163.75', port=5001)

