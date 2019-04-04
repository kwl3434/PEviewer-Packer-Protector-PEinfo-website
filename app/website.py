from flask import Flask
app= Flask(__name__)

@app.route("/")

def message():
	return "Python is awesome!"

app.run(host='0.0.0.0', port=5000)

