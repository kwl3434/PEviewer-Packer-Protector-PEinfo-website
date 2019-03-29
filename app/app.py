from flask import Flask,render_template,redirect, url_for, request
app = Flask(__name__)

@app.route('/')
def index_():
    return render_template('index.html',error=error)

if __name__ == '__main__':
    app.run(host='0.0.0.0')
