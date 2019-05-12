#-*- coding: utf-8 -*-
import subprocess
import os
import sys
import commands

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

from flask import Flask, render_template, request, make_response
from flask import send_file
from werkzeug import secure_filename

from functools import wraps, update_wrapper
from datetime import datetime

app = Flask(__name__)
main='main.html'
pack='pack_protector'
howto='howtouse.html'
total='total.html'
peinfo='peinfo'
peview='peview'
jpg1='1.JPG'
jpg2='2.JPG'
jpg3='3.JPG'
jpg4='4.JPG'
jpg5='5.JPG'

#업로드 HTML 렌더링

@app.route('/')
def main():
    return render_template('main.html',src1=howto)

@app.route('/total')
def total():
    return render_template('total.html',src1=pack,src2=peinfo, src3=peview)

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/howtouse')
def howtouse():
    return render_template('howtouse.html')

@app.route('/peinfo')
def peinfo_e():
    return render_template('peinfo.html')

@app.route('/peview')
def peview_e():
    return render_template('peview.html',data='peviewer')
def peview_ee(Data):
    return render_template('peview.html',data=Data)

@app.route('/pack_protector', methods = ['GET','POST'])
def render_file():
    return render_template('pack_protector.html',ff="Upload File..")

#파일 업로드 처리
@app.route('/upload', methods = ['GET', 'POST'])
def upload_file():
   if request.method == 'POST':
      f = request.files['file']
      global F
      F=f.filename;
      #저장할 경로 + 파일명
      f.save(secure_filename(f.filename))
      os.system('./viruscheck '+f.filename)
      TXT = open("/root/TorF.txt",'r');
      line = TXT.readline()
      TXT.close()
      if line=='None':
	os.system('chown hide '+f.filename)
      	return render_template('pack_protector.html',ff=f.filename)
      else:
	os.system('rm '+f.filename);
	return "Virus detected"
	

@app.route('/pack_download', methods = ['GET', 'POST'])
def pack_download_file():
   if request.method == 'POST':
	f=request.form['fname']
	if f=="Upload":
		return "Please Upload File first"
	elif f[0]=='/' or f[0]=='.' or f[0]==' ' or f[0]==';':
		return "Warning 112"
	else:
  		path="/PEviewer-Packer-Protector-PEinfo-website/app/"+f+".7z"
        	os.system('upx '+f)
	        os.system('7z a '+f+'.7z '+f)
		os.system('rm '+f)
        	return send_file(path,as_attachment=True)

@app.route('/unpack_download', methods = ['GET', 'POST'])
def unpack_download_file():
   if request.method == 'POST':
	f=request.form['fname']
	if f=="Upload File..":
		return "Please Upload File first"
	elif f[0]=='/' or f[0]=='.' or f[0]==' ' or f[0]==';':
		return "Warning 112"
	else:
        	path="/PEviewer-Packer-Protector-PEinfo-website/app/"+f+".7z"
        	os.system('upx -d '+f)
        	os.system('7z a '+f+'.7z '+f)
		os.system('rm '+f)
        	return send_file(path,as_attachment=True)
	
if __name__ == '__main__':
    #서버 실행
   app.run(threaded=True, host='0.0.0.0', port=80)

