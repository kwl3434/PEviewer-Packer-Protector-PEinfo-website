from flask import Flask, render_template, request
from werkzeug import secure_filename
app = Flask(__name__)

#업로드 HTML 렌더링
@app.route('/upload')
def render_file():
   return render_template('upload.html')

#파일 업로드 처리
@app.route('/fileUpload', methods = ['GET', 'POST'])
def upload_file():
   if request.method == 'POST':
      f = request.files['file']
      #저장할 경로 + 파일명
      f.save(secure_filename(f.filename))
      return 'uploads 디렉토리 -> 파일 업로드 성공!'

if __name__ == '__main__':
    #서버 실행
   app.run(debug = True)
