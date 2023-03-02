import codecs

import pymysql.cursors
import base64
from codecs import encode
from _mysql_connector import MySQL
from flask import Flask, render_template, request,jsonify
from flaskext.mysql import MySQL
from app import app
from flask_wtf import FlaskForm
from wtforms import FileField,SubmitField
from werkzeug.utils import secure_filename
from flask_wtf.file import file_required
import os

mysql=MySQL()
app.config['MYSQL_DATABASE_USER']='root'
app.config['MYSQL_DATABASE_PASSWORD']='password'
app.config['MYSQL_DATABASE_DB']='employee_info'
app.config['MYSQL_DATABASE_HOST']='localhost'
mysql.init_app(app)

app=Flask(__name__)
app.config['SECRET_KEY']='superkey'
app.config['UPLOAD_FOLDER']='static/files'


def binarydata(filename):
    with open(filename, 'rb') as img_file:
        binaryData = img_file.read()
    return binaryData

# @app.route('/upload', methods=['GET','POST'])
# def upload():
#     form=UploadFileForm()
#     if form.validate_on_submit():
#         file=form.file.data
#         print(file)
#         file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)),app.config['UPLOAD_FOLDER'],secure_filename(file.filename)))
#         return "FILE HAS UPLOADED SUCCESSFULLY"
#     return render_template("index.html",form=form)


# class UploadFileForm(FlaskForm):
#     file=FileField("file",validators=[file_required()])
#     submit=SubmitField("Upload File")


@app.route('/uploadfile' , methods=['GET','POST'])
def uploadfile():
    files = request.files.getlist('files[]')
    for file in files:
        file.save("static/files/"+file.filename)
        print(file.filename)
    return "File uploaded successfully"


@app.route('/doc',methods=['GET','POST'])
def doc():
    _data = request.files['file']
    base=_data.read()
    store_file=base64.b64encode(base)
    # print(store_file)
    print(store_file)
    if request.method=='POST':
        conn=mysql.connect()
        cur=conn.cursor(pymysql.cursors.DictCursor)
        cur.execute("INSERT INTO documents(filename,data) values(%s,%s);",(_data.filename,store_file))
        conn.commit()
        resp=jsonify("DOCUMENT INSERTED SUCCESSFULLY")
        return resp


@app.route("/files/<int:id>",methods=['GET'])
def files(id):
    conn=mysql.connect()
    cur=conn.cursor(pymysql.cursors.DictCursor)
    cur.execute("SELECT filename,data FROM documents WHERE id=%s;",id)
    row=cur.fetchall()
    for i in row:
        file=i['data']
        filename=i['filename']
    f=open(filename, "wb")
    f.write(base64.decodebytes(file))
    f.close()
    return "p"

@app.route('/new_doc',methods=['GET','POST'])
def new_doc():
    _data = request.files['file']
    print(_data)
    if request.method=='POST':
        conn=mysql.connect()
        cur=conn.cursor(pymysql.cursors.DictCursor)
        cur.execute("INSERT INTO files(file_data) values(%s);",_data)
        conn.commit()
        resp=jsonify("DOCUMENT INSERTED SUCCESSFULLY")
        return resp


if __name__ == '__main__':
    app.run(debug=True)

