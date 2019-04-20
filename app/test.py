#-*- coding: utf-8 -*-
from flask import Flask, render_template, request
from werkzeug import secure_filename
app = Flask(__name__)

@app.route('/')
def render_file():
   return render_template('upload.html')

@app.route('/upload', methods = ['GET', 'POST'])
def upload_file():
   if request.method == 'POST':
      f = request.files['file']
      #저장할 경로 + 파일명
      f.save(secure_filename(f.filename))
      return 'uploads 디렉토리 -> 파일 업로드 성공!'

if __name__ == '__main__':
   app.run(host='0.0.0.0', port=5000)
