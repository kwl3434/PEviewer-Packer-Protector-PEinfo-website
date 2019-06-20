# -*- coding: utf-8 -*-
import subprocess
import os, walk
import sys
import commands
import string
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
#32Mb limit

app.secret_key = 'dont tell anyone'
main='main.html'
pack='pack_protector'
howto='howtouse.html'
total='total.html'
PEINFO='PEINFO'
peview='peview'
dosheader='DOSHEADER.html'
fileheader='FILEHEADER.html'
sectionheadupx0='SECTIONHEADUPX0.html'
sectionupx0='SECTIONUPX0.html'
stubprogram='STUBPROGRAM.html'

jpg1='main.JPG'
jpg2='loading.JPG'
jpg3='file.JPG'
jpg4='pack4.JPG'
jpg5='protect.JPG'
jpg6='peview1.JPG'
jpg7='peview2.JPG'
jpg8='peview3.JPG'
jpg9='peview4.JPG'
jpg10='peview5.JPG'
jpg11='virus1.JPG'
# exe파일만 허용하는 함수
def allowed_file(filename): 
        return '.' in filename and \
                filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

def character_black(f):
    if ';' in f:
        flash('dont use filename ! ~ ` # $ % ^ & * ( ) + = { } [ ] \" \' ; :')
        return False
    elif '=' in f:
        flash('dont use filename ! ~ ` # $ % ^ & * ( ) + = { } [ ] \" \' ; :')
        return False
    elif '+' in f:
        flash('dont use filename ! ~ ` # $ % ^ & * ( ) + = { } [ ] \" \' ; :')
        return False
    elif '!' in f:
        flash('dont use filename ! ~ ` # $ % ^ & * ( ) + = { } [ ] \" \' ; :')
        return False
    elif '@' in f:
        flash('dont use filename ! ~ ` # $ % ^ & * ( ) + = { } [ ] \" \' ; :')
        return False
    elif ']' in f:
        flash('dont use filename ! ~ ` # $ % ^ & * ( ) + = { } [ ] \" \' ; :')
        return False
    elif '[' in f:
        flash('dont use filename ! ~ ` # $ % ^ & * ( ) + = { } [ ] \" \' ; :')
        return False
    elif '#' in f:
        flash('dont use filename ! ~ ` # $ % ^ & * ( ) + = { } [ ] \" \' ; :')
        return False
    elif '$' in f:
        flash('dont use filename ! ~ ` # $ % ^ & * ( ) + = { } [ ] \" \' ; :')
        return False
    elif '%' in f:
        flash('dont use filename ! ~ ` # $ % ^ & * ( ) + = { } [ ] \" \' ; :')
        return False
    elif '^' in f:
        flash('dont use filename ! ~ ` # $ % ^ & * ( ) + = { } [ ] \" \' ; :')
        return False
    elif '&' in f:
        flash('dont use filename ! ~ ` # $ % ^ & * ( ) + = { } [ ] \" \' ; :')
        return False
    elif '*' in f:
        flash('dont use filename ! ~ ` # $ % ^ & * ( ) + = { } [ ] \" \' ; :')
        return False
    elif ')' in f:
        flash('dont use filename ! ~ ` # $ % ^ & * ( ) + = { } [ ] \" \' ; :')
        return False
    elif '(' in f:
        flash('dont use filename ! ~ ` # $ % ^ & * ( ) + = { } [ ] \" \' ; :')
        return False
    elif '{' in f:
        flash('dont use filename ! ~ ` # $ % ^ & * ( ) + = { } [ ] \" \' ; :')
        return False
    elif '}' in f:
        flash('dont use filename ! ~ ` # $ % ^ & * ( ) + = { } [ ] \" \' ; :')
        return False
    elif '|' in f:
        flash('dont use filename ! ~ ` # $ % ^ & * ( ) + = { } [ ] \" \' ; :')
        return False
    elif '\\' in f:
        flash('dont use filename ! ~ ` # $ % ^ & * ( ) + = { } [ ] \" \' ; :')
        return False
    elif '`' in f:
        flash('dont use filename ! ~ ` # $ % ^ & * ( ) + = { } [ ] \" \' ; :')
        return False
    elif '<' in f:
        flash('dont use filename ! ~ ` # $ % ^ & * ( ) + = { } [ ] \" \' ; :')
        return False
    elif '>' in f:
        flash('dont use filename ! ~ ` # $ % ^ & * ( ) + = { } [ ] \" \' ; :')
        return False
    elif ' ' in f:
        flash('dont use filename ! ~ ` # $ % ^ & * ( ) + = { } [ ] \" \' ; :')
        return False
    elif '\'' in f:
        flash('dont use filename ! ~ ` # $ % ^ & * ( ) + = { } [ ] \" \' ; :')
        return False
    elif '\"' in f:
        flash('dont use filename ! ~ ` # $ % ^ & * ( ) + = { } [ ] \" \' ; :')
        return False
    else:
        return True

#업로드 HTML 렌더링

@app.route('/')
def main():
    return render_template('main.html',src1=howto)

@app.route('/total')
def total():
    return render_template('total.html',src1=pack,src2=PEINFO, src3=peview)

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/howtouse')
def howtouse():
    return render_template('howtouse.html')

@app.route('/loading')
def loading():
    return render_template('loading.html')

@app.route('/PEINFO', methods = ['GET', 'POST'])
def PEINFO_e():
        return render_template('PEINFO.html') 

@app.route('/peinfo/<f>', methods = ['GET', 'POST'])
def peinfo_e(f):
    if f=="Upload":
        return render_template('empty.html')
    else:
        return render_template(f+'peinfo.html') 

@app.route('/peview', methods = ['GET','POST'])
def peview_e():
   return render_template('peview.html')

@app.route('/DOSHEADER/<f>')
def dosheader(f):
    if f=="Upload":
        return render_template('empty.html')
    else:
        return render_template(f+'DOSHEADER.html')
@app.route('/FILEHEADER/<f>')
def fileheader(f):
    if f=="Upload":
        return render_template('empty.html')
    else:
        return render_template(f+'FILEHEADER.html')

@app.route('/SECTIONHEAD/<f>')
def sectionhead(f):
    if f=="Upload":
        return render_template('empty.html')
    else:
        return render_template(f+'SECTIONHEAD.html')

@app.route('/SECTION/<f>')
def section(f):
    if f=="Upload":
        return render_template('empty.html')
    else:
        return render_template(f+'SECTION.html')

@app.route('/STUBPROGRAM/<f>', methods=['GET', 'POST'])
def stubprogram(f):
        if f=="Upload":
            return render_template('empty.html')
        else:
            ft = open('static/'+f+'stubprogram.txt','r')
            return "</br>".join(ft.readlines())

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
   printable = set(string.printable)
   for c in f.filename:
      if c not in printable:
          flash('File names are only ASCII code')
          return render_template('pack_protector.html',ff="Upload File..")

   CH=character_black(f.filename)
   if not CH:
      return render_template('pack_protector.html',ff="Upload File..")
   if f.filename == '':
      flash('No file selected for uploading')
      return render_template('pack_protector.html',ff="Upload File..")
   if f and allowed_file(f.filename):
      f.save(secure_filename(f.filename))
      size = os.stat(f.filename).st_size

      if size > 32*1024*1024:
          flash("File limit 32MB")
          os.system('rm '+f.filename)
          return render_template('pack_protector.html',ff="Upload File..")

      os.system('./viruscheck '+f.filename)
      TXT = open("/root/TorF.txt",'r');
      line = TXT.readline()
      TXT.close()

      if line=='None':
        flash("Upload and Virus check complete!")
        dir_path = "/PEviewer-Packer-Protector-PEinfo-website/app/templates"
        dir_name = f.filename
        os.system('pepack -f html '+f.filename+'> ./templates/'+f.filename+'peinfo.html ')
        os.system('pepack '+f.filename+'> ./templates/'+f.filename+'peinfo')
        os.system('pesec -f html '+f.filename+'>> ./templates/'+f.filename+'peinfo.html ')
        os.system('readpe -f html -h dos '+f.filename+'> ./templates/'+f.filename+'DOSHEADER.html ')
        os.system('readpe -f html -h coff '+f.filename+'> ./templates/'+f.filename+'FILEHEADER.html ')
        os.system('readpe -f html -h optional '+f.filename+'>> ./templates/'+f.filename+'FILEHEADER.html ')
        os.system('pestr -o '+f.filename+'> ./static/'+f.filename+'stubprogram.txt ')
        os.system('readpe -f html -S '+f.filename+'> ./templates/'+f.filename+'SECTIONHEAD.html ')
        os.system('pehash -f html -s '+f.filename+'> ./templates/'+f.filename+'SECTION.html ')
      	return render_template('pack_protector.html',ff=f.filename)
      else:
        error = 'Virus detected!'
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
            pein = open('./templates/'+f+'peinfo','r')
            line = pein.readline()
            pein.close()
            if "no" in line:
  	        path="/PEviewer-Packer-Protector-PEinfo-website/app/"+f+".7z"
                os.system('upx '+f)
	        os.system('7z a '+f+'.7z '+f)
                return send_file(path,as_attachment=True)
            elif "Microsoft Visual C++" in line:
  	        path="/PEviewer-Packer-Protector-PEinfo-website/app/"+f+".7z"
                os.system('upx '+f)
	        os.system('7z a '+f+'.7z '+f)
                return send_file(path,as_attachment=True)
            else:
                flash("Already packing")
                return render_template('pack_protector.html',ff=f)

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
            pein = open('./templates/'+f+'peinfo','r')
            line = pein.readline()
            pein.close()
            if "no" in line:
                flash("It is not already packed.")
                return render_template('pack_protector.html',ff=f)
            elif "Microsoft Visual C++" in line:
                flash("It is not already packed.")
                return render_template('pack_protector.html',ff=f)
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
            os.system('./vmprotect_con '+f)
            os.system('7z a '+ f_list[0] + '.vmp.7z '+ f_list[0] + ".vmp.exe")
  	    path="/PEviewer-Packer-Protector-PEinfo-website/app/"+ f_list[0] + ".vmp.7z";
            return send_file(path,as_attachment=True)

if __name__ == '__main__':
    #서버 실행
   app.config['TEMPLATES_AUTO_RELOAD'] = True
   app.run(threaded=True, host='0.0.0.0', port=80) #extra_files=extra_files

