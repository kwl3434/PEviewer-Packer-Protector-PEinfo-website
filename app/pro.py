from flask import Flask, render_template, request, Response

app = Flask(__name__)

def event_stream():
    event = "Hello!"
    yield 'data: %s\n\n' % event

@app.route('/stream')
def stream():
    return Response(event_stream(), mimetype="text/event-stream")

if __name__ == "__main__":
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
