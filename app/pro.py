
from flask import Flask, render_template, Response
import time

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('pro.html')

@app.route('/progress')
def progress():
    def generate():
        x = 0
        while x <= 100:
            yield "data:" + str(x) + "\n\n"
            x = x + 10
            time.sleep(0.5)

                                                                        
    return Response(generate(), mimetype= 'text/event-stream')

if __name__ == "__main__":
    app.run(host='0.0.0.0',port=80)
