from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('02.index.html')

@app.route('/welcome')
def welcome():
    return render_template('02.welcome.html')

if __name__ == '__main__':
    app.run(debug=True)