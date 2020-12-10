from flask import Flask, render_template
import os
app = Flask(__name__)

@app.route('/')
def index():
    img_file = os.path.join(app.root_path, 'static/img/이미지.jpg')
    mtime = int(os.stat(img_file).st_mtime)
    return render_template('05.index.html', mtime=mtime)

if __name__ == '__main__':
    app.run(debug=True)