#-*- coding: utf-8 -*-
import subprocess
import os
import sys
from flask import Flask, render_template, request
from flask import send_file
from werkzeug import secure_filename
app = Flask(__name__)
menu='menubar.html'
pack='pack_protector.html'
#업로드 HTML 렌더링

@app.route('/')
def home():
   return render_template('total.html',src1=menu, src2=pack, methods = ['GET','POST'])
@app.route('/menubar.html')
def index():
    return render_template('menubar.html')

@app.route('/pack_protector.html', methods = ['GET','POST'])
def render_file():
    return render_template('pack_protector.html')

#파일 업로드 처리
@app.route('/upload', methods = ['GET', 'POST'])
def upload_file():
   if request.method == 'POST':
      global f
      f = request.files['file']
      #저장할 경로 + 파일명
      f.save(secure_filename(f.filename))
      os.system('./viruscheck '+f.filename)
      return render_template('pack_protector.html')

@app.route('/pack_download', methods = ['GET'])
def pack_return_file():
    try:
        path="/PEviewer-Packer-Protector-PEinfo-website/app/"+f.filename
        os.system('upx '+f.filename)
        return send_file(path,as_attachment=True)
    except Exception as e:
        return "Please upload the file first."

@app.route('/unpack_download', methods = ['GET'])
def unpack_return_file():
    try:
        path="/PEviewer-Packer-Protector-PEinfo-website/app/"+f.filename
        os.system('upx -d '+f.filename)
        return send_file(path,as_attachment=True)
    except Exception as e:
        return "Please upload the file first."

if __name__ == '__main__':
    #서버 실행
   app.run(host='0.0.0.0', port=5000)

