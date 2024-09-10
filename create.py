from flask import Flask, render_template
app = Flask(__name__)


@app.route('/')
def home():
    # 假设这是你要在表格中展示的数据
    data = [
        {'name': 'Alice', 'age': 24, 'city': 'New York'},
        {'name': 'Bob', 'age': 27, 'city': 'Los Angeles'},
        {'name': 'Charlie', 'age': 22, 'city': 'Chicago'}
    ]
    data1 = [
        {'name': 'Alice', 'age': 24, 'home': 'New York'},
        {'name': 'Bob', 'age': 27, 'home': 'Los Angeles'},
        {'name': 'Charlie', 'age': 22, 'home': 'Chicago'}
    ]

    return render_template('index.html', data=data1)



if __name__ == '__main__':
    app.run(debug=True)