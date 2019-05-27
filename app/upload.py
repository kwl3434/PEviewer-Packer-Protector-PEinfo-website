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
Data='peview1.html'
peinfo='peinfo'
peview='peview'
context='context.html'
dosheader='DOSHEADER.html'
fileheader='FILEHEADER.html'
sectionheadrsrc='SECTIONHEADRSRC.html'
sectionheadupx0='SECTIONHEADUPX0.html'
sectionheadupx1='SECTIONHEADUPX1.html'
sectionrsrc='SECTIONRSRC.html'
sectionupx0='SECTIONUPX0.html'
sectionupx1='SECTIONUPX1.html'


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

@app.route('/context')
def context():
    return render_template('context.html')

@app.route('/loading')
def loading():
    return render_template('loading.html')

@app.route('/peinfo')
def peinfo_e():
    return render_template('peinfo.html')

@app.route('/peview', methods = ['GET','POST'])
def peview_e():
   return render_template('peview.html')
	#return Response(f.read(), mimetype='text/plain')					 #data='peviewer'
#def peview_ee(Data):
   # return render_template('peview.html',data=Data)

@app.route('/DOSHEADER', methods = ['GET', 'POST'])
def dosheader():
	return render_template('DOSHEADER.html')
@app.route('/FILEHEADER', methods = ['GET', 'POST'])
def fileheader():
	return render_template('FILEHEADER.html')
@app.route('/OPTIONALHEADER', methods = ['GET', 'POST'])
def optionalheader():
	return render_template('OPTIONALHEADER.html')

@app.route('/SECTIONHEADRSRC', methods = ['GET', 'POST'])
def sectionheadrsrc():
	return render_template('SECTIONHEADRSRC.html')
@app.route('/SECTIONHEADUPX0', methods = ['GET', 'POST'])
def sectionheadupx0():
	return render_template('SECTIONHEADUPX0.html')
@app.route('/SECTIONHEADUPX1', methods = ['GET','POST'])
def sectionheadupx1():
	return render_template('SECTIONHEADUPX1.html')

@app.route('/SECTIONUPX0', methods = ['GET','POST'])
def sectionupx0():
	return render_template('SECTIONUPX0.html')
@app.route('/SECTIONUPX1')
def sectionupx1():
	return render_template('SECTIONUPX1.html')
@app.route('/SECTIONRSRC', methods = ['GET','POST'])
def sectionrsrc():
	return render_template('SECTIONRSRC.html')


@app.route('/pack_protector', methods = ['GET','POST'])
def render_file():
    return render_template('pack_protector.html',ff="Upload File..")

#파일 업로드 처리
@app.route('/upload', methods = ['GET', 'POST'])
def upload_file():
   if request.method == 'POST':
      f = request.files['file']
      #저장할 경로 + 파일명
      f.save(secure_filename(f.filename))
      os.system('./viruscheck '+f.filename)
      #os.system('pehash -f html '+f.filename+'> ./templates/peview1.html ')
      #os.system('readpe -f html '+f.filename+'>> ./templates/peview1.html ')
      os.system('pepack -f html '+f.filename+'> ./templates/peinfo1.html ')
      os.system('pesec -f html '+f.filename+'>> ./templates/peinfo1.html ')
      #if f=
      os.system('readpe -f html -h dos '+f.filename+'> ./templates/DOSHEADER.html ')
      #os.system(stubprogram)
      os.system('readpe -f html -h coff '+f.filename+'> ./templates/FILEHEADER.html ')
      os.system('readpe -f html -h optional '+f.filename+'>> ./templates/FILEHEADER.html ')
      os.system('readpe -f html -S UPX0 '+f.filename+'> ./templates/SECTIONHEADUPX0.html ')
      os.system('readpe -f html -S UPX1 '+f.filename+'> ./templates/SECTIONHEADUPX1.html ')
      os.system('readpe -f html -S .rsrc '+f.filename+'> ./templates/SECTIONHEADRSRC.html ')
      os.system('pehash -f html -s UPX0 '+f.filename+'> ./templates/SECTIONUPX0.html ')
      os.system('pehash -f html -s UPX1 '+f.filename+'> ./templates/SECTIONUPX1.html ')
      os.system('pehash -f html -s .rsrc '+f.filename+'> ./templates/SECTIONRSRC.html ')
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
        	return send_file(path,as_attachment=True)

@app.route('/protect_download', methods = ['GET', 'POST'])
def protect_download_file():
   if request.method == 'POST':
	f=request.form['fname']
	if f=="Upload":
		return "Please Upload File first"
	elif f[0]=='/' or f[0]=='.' or f[0]==' ' or f[0]==';':
		return "Warning 112"
	else:
                f_list = f.split('.');
        	#path="/PEviewer-Packer-Protector-PEinfo-website/app/"+f+".7z"
        	os.system('./vmprotect_con '+f)
        	os.system('7z a '+ f_list[0] + '.vmp.7z '+ f_list[0] + ".vmp.exe")
  		path="/PEviewer-Packer-Protector-PEinfo-website/app/"+ f_list[0] + ".vmp.7z";
                #print(path);
                #print(f_list[0]);
        	return send_file(path,as_attachment=True)

if __name__ == '__main__':
    #서버 실행
   app.config['TEMPLATES_AUTO_RELOAD'] = True
   app.run(threaded=True, host='0.0.0.0', port=80)
   
   

