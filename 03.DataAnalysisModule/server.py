from flask import Flask
from bp5_stock.simple import simple_bp
from bp5_stock.stock import stock_bp

app = Flask(__name__)
app.register_blueprint(simple_bp, url_prefix='/simple')
app.register_blueprint(stock_bp, url_prefix='/stock')

@app.route('/')
def index():
    return 'Index Page'

if __name__ == '__main__':
    app.run(debug=True)