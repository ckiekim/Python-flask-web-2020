from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('08.carousel.html')

@app.route('/table')
def table():
    return render_template('08.filterable_table.html')

if __name__ == '__main__':
    app.run(debug=True)