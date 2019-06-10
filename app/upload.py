#-*- coding: utf-8 -*-
import subprocess
import os, walk
import sys
import commands

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import threading
from flask import Flask, render_template, request, make_response, redirect, url_for, flash, Response
#from flaskext.uploads import UploadSet,configure_uploads,ALL
from flask import send_file
from werkzeug import secure_filename

from functools import wraps, update_wrapper
from datetime import datetime

ALLOWED_EXTENSIONS = set(['exe'])
app = Flask(__name__)

#extra_dirs = ['/PEviewer-Packer-Protector-PEinfo-website/app/static','/PEviewer-Packer-Protector-PEinfo-website/app/templates']
#extra_files = extra_dirs[:]
#for extra_dir in extra_dirs:
    #for dirname, dirs, files in os.walk(extra_dir):
        #for filename in files:
            #filename = os.path.join(dirname, filename)
            #if os.path.isfile(filename):
		#extra_files.append(filename)
#my_loader = jinja2.ChoiceLoader([
#	app.jinja_loader,
#	jinja2.FileSystemLoader(['/PEviewer-Packer-Protector-PEinfo-website/app/templates' ]), ])
#app.jinja_loader = my_loader
#username = f.filename
#render_template('templask/%s/DOSHEADER.html' %username)

#UPLOAD_FOLDER = '/PEviewer-Packer-Protector-PEinfo-website/app'
#app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
#app.config['UPLOADED_FILES_DEST'] = 'uploads'
#configure_uploads(app, files)

app.secret_key = 'dont tell anyone'
main='main.html'
pack='pack_protector'
howto='howtouse.html'
total='total.html'
peinfo='peinfo'
peview='peview'
dosheader='DOSHEADER.html'
fileheader='FILEHEADER.html'
sectionheadupx0='SECTIONHEADUPX0.html'
sectionupx0='SECTIONUPX0.html'
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

@app.route('/peinfo', methods = ['GET', 'POST'])
def peinfo_e():
   # with open('/PEviewer-Packer-Protector-PEinfo-website/app/static/peinfo.txt', 'r') as d:
   #      data = d.read()
    return render_template('peinfo.html') #data=data

@app.route('/peview', methods = ['GET','POST'])
def peview_e():
   return render_template('peview.html')

@app.route('/DOSHEADER/<f>')
def dosheader(f):
	#with open('/PEviewer-Packer-Protector-PEinfo-website/app/static/dosheader.txt', 'r') as f:
	#data = f.read()
	return render_template(f+'DOSHEADER.html')
@app.route('/FILEHEADER')
def fileheader():
	f=request.form['fname']
	return render_template(f+'FILEHEADER.html')

@app.route('/SECTIONHEADUPX0')
def sectionheadupx0():
	f=request.form['fname']
	return render_template(f+'SECTIONHEADUPX0.html')

@app.route('/SECTIONUPX0')
def sectionupx0(filename):
	#f=request.form['fname']
	return render_template('%s/SECTIONUPX0.html' %filename)

@app.route('/STUBPROGRAM', methods = ['GET', 'POST'])
def stubprogram():
	f=request.form['fname']
	with open('/PEviewer-Packer-Protector-PEinfo-website/app/static/stubprogram.txt', 'r') as f:
	     content = f.read()
	return render_template(f+'STUBPROGRAM.html', content=content)

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
   if f.filename == '':
      flash('No file selected for uploading')
      return render_template('pack_protector.html',ff="Upload File..")
   if f and allowed_file(f.filename):
      f.save(secure_filename(f.filename))
      os.system('./viruscheck '+f.filename)
      dir_path = "/PEviewer-Packer-Protector-PEinfo-website/app/templates"
      dir_name = f.filename
      #os.mkdir(dir_path+"/"+dir_name+"/")
      os.system('pepack -f html '+f.filename+'> ./templates/peinfo1.html ')
      os.system('pesec -f html '+f.filename+'>> ./templates/peinfo1.html ')
      os.system('readpe -f html -h dos '+f.filename+'> ./templates/'+f.filename+'DOSHEADER.html ')
      os.system('readpe -f html -h coff '+f.filename+'> ./templates/'+f.filename+'FILEHEADER.html ')
      os.system('readpe -f html -h optional '+f.filename+'>> ./templates/'+f.filename+'FILEHEADER.html ')
      os.system('pestr -o '+f.filename+'> ./static/'+f.filename+'stubprogram.txt ')
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
   else:
        flash('Please upload .exe file')
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
   app.run(threaded=True, host='0.0.0.0', port=80) #extra_files=extra_files

