from flask import Flask,render_template,redirect
app = Flask(__name__)

@app.route('/')
def index_():
    return render_template('drag.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0')
