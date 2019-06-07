#-*- coding: utf-8 -*-
import subprocess
import os
import sys
import commands

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

from flask import Flask, render_template, request, make_response, redirect, url_for, flash
#from flaskext.uploads import UploadSet,configure_uploads,ALL
from flask import send_file
from werkzeug import secure_filename

from functools import wraps, update_wrapper
from datetime import datetime

ALLOWED_EXTENSIONS = set(['exe'])

app = Flask(__name__)
UPLOAD_FOLDER = './upload'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
#files = UploadSet('files',ALL)
#app.config['UPLOADED_FILES_DEST'] = 'uploads'
#configure_uploads(app, files)
name=os.path.splitext(os.path.basename("/PEviewer-Packer-Protector-PEinfo-website/app/%s", f.filename))[0]

app.secret_key = 'dont tell anyone'
main='main.html'
pack='pack_protector'
howto='howtouse.html'
total='total.html'
peinfo='peinfo'
peview='peview'
dosheader='DOSHEADER.html'
fileheader='FILEHEADER.html'
#sectionheadrsrc='SECTIONHEADRSRC.html'
sectionheadupx0='SECTIONHEADUPX0.html'
#sectionheadupx1='SECTIONHEADUPX1.html'
#sectionrsrc='SECTIONRSRC.html'
sectionupx0='SECTIONUPX0.html'
#sectionupx1='SECTIONUPX1.html'
stubprogram='STUBPROGRAM.html'

jpg1='1.JPG'
jpg2='2.JPG'
jpg3='3.JPG'
jpg4='4.JPG'
jpg5='5.JPG'
# exe파일만 허용하는 함수
def allowed_file(filename): 
        return '.' in filename and \
                filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS
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

@app.route('/loading')
def loading():
    return render_template('loading.html')

@app.route('/peinfo')
def peinfo_e():
    return render_template('peinfo.html')

@app.route('/peview', methods = ['GET','POST'])
def peview_e():
   return render_template('peview.html')
#return Response(f.read(), mimetype='text/plain')
#data='peviewer'
#def peview_ee(Data):
#return render_template('peview.html',data=Data)

@app.route('/DOSHEADER')
def dosheader():
	return render_template('DOSHEADER.html')

@app.route('/FILEHEADER')
def fileheader():
	return render_template('FILEHEADER.html')

#@app.route('/OPTIONALHEADER', methods = ['GET', 'POST'])
#def optionalheader():
#	return render_template('OPTIONALHEADER.html')

#@app.route('/SECTIONHEADRSRC', methods = ['GET', 'POST'])
#def sectionheadrsrc():
#	return render_template('SECTIONHEADRSRC.html')

@app.route('/SECTIONHEADUPX0')
def sectionheadupx0():
	return render_template('SECTIONHEADUPX0.html')

#@app.route('/SECTIONHEADUPX1', methods = ['GET','POST'])
#def sectionheadupx1():
	#return render_template('SECTIONHEADUPX1.html')


@app.route('/SECTIONUPX0')
def sectionupx0():
	return render_template('SECTIONUPX0.html')

@app.route('/STUBPROGRAM')
def stubprogram():
	return render_template('STUBPROGRAM.html')

#@app.route('/SECTIONUPX1')
#def sectionupx1():
	#return render_template('SECTIONUPX1.html')

#@app.route('/SECTIONRSRC', methods = ['GET','POST'])
#def sectionrsrc():
	#return render_template('SECTIONRSRC.html')


@app.route('/pack_protector', methods = ['GET','POST'])
def render_file():
    return render_template('pack_protector.html',ff="Upload File..")

#파일 업로드 처리
@app.route('/upload', methods = ['GET', 'POST'])
def upload_file():
   #error = None
   if request.method == 'POST':
      f = request.files['file']
      
      #저장할 경로 + 파일명
#try:
   if f.filename == '':
      flash('No file selected for uploading')
      print(name)
      return render_template('pack_protector.html',ff="Upload File..")
   if f and allowed_file(f.filename):
      #flash('Upload Successfully!')
      f.save(secure_filename(f.filename))
      os.system('./viruscheck '+f.filename)

      os.system('pepack -f html '+f.filename+'> ./templates/'+f.filename+'peinfo1.html ')
      os.system('pesec -f html '+f.filename+'>> ./templates/'+f.filename+'peinfo1.html ')
      os.system('readpe -f html -h dos '+f.filename+'> ./templates/'+f.filename+'DOSHEADER.html ')
      os.system('readpe -f html -h coff '+f.filename+'> ./templates/'+f.filename+'FILEHEADER.html ')
      os.system('readpe -f html -h optional '+f.filename+'>> ./templates/'+f.filename+'FILEHEADER.html ')
     #os.system('pestr -o '+f.filename+'> ./stubprogram.txt ')
     #os.system('rst2html5 ./stubprogram.txt > ./templates/STUBPROGRAM.html ')
      os.system('readpe -f html -S UPX0 '+f.filename+'> ./templates/'+f.filename+'SECTIONHEADUPX0.html ')
      os.system('pehash -f html -s '+f.filename+'> ./templates/'+f.filename+'SECTIONUPX0.html ')

      flash("Upload and Virus check complete!")
      TXT = open("/root/TorF.txt",'r');
      line = TXT.readline()
      TXT.close()
      if line=='None':
      	return render_template('pack_protector.html',ff=f.filename)
      else:
        error = 'Please exe file upload!'
        flash(error)
        return render_template('pack_protector.html',ff="Upload File..")

@app.route('/pack_download', methods = ['GET', 'POST'])
def pack_download_file():
   if request.method == 'POST':
	f=request.form['fname']
	if f=="Upload":
                flash("Please Upload File first")
                return render_template('pack_protector.html',ff="Upload File..")
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
	if f=="Upload":
                flash("Please Upload File first")
                return render_template('pack_protector.html',ff="Upload File..")
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
                flash("Please Upload File first")
                return render_template('pack_protector.html',ff="Upload File..")
	elif f[0]=='/' or f[0]=='.' or f[0]==' ' or f[0]==';':
		return "Warning 112"
	else:
                f_list = f.split('.');
        	#path="/PEviewer-Packer-Protector-PEinfo-website/app/"+f+".7z"
        	os.system('./vmprotect_con '+f)
        	os.system('7z a '+ f_list[0] + '.vmp.7z '+ f_list[0] + ".vmp.exe")
  		path="/PEviewer-Packer-Protector-PEinfo-website/app/"+ f_list[0] + ".vmp.7z";
                return send_file(path,as_attachment=True)

if __name__ == '__main__':
    #서버 실행
   app.config['TEMPLATES_AUTO_RELOAD'] = True
   app.run(threaded=True, host='0.0.0.0', port=80)

