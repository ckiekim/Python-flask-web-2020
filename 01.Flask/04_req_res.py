from flask import Flask, render_template, request
from flask import Response, make_response
app = Flask(__name__)

# query parameter 처리
@app.route('/area')
def area():
    pi = request.args.get('pi', '3.14')     # pi 값이 주어지지 않으면 3.14를 주어라
    radius = request.values['radius']
    s = float(pi) * float(radius) * float(radius)
    return f'pi={pi}, radius={radius}, area={s}'

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('03.login.html')
    else:
        uid = request.form['uid']
        pwd = request.values['pwd']
        return f'uid={uid}, pwd={pwd}'

@app.route('/response')
def response_fn():
    custom_res = Response('Custom Response', 200, {'test': 'ttt'})
    return make_response(custom_res)

if __name__ == '__main__':
    app.run(debug=True)