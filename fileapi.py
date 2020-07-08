from flask import Flask, jsonify, request, redirect, url_for, send_file
from flask_restful import Api, Resource, reqparse
import os

from hashlib import md5
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'store'

app = Flask(__name__)
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
api = Api(app)

client = app.test_client()

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route('/upload', methods=['POST', 'GET'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            hash = md5(filename.encode()).hexdigest()
            hash_dir = hash[0:2]
            upload_dir = UPLOAD_FOLDER + '\\'+ hash_dir
            try:

                os.mkdir(upload_dir)
                file.save(os.path.join(upload_dir, hash))
                return hash
            except FileExistsError:
                file.save(os.path.join(upload_dir, hash))
                return hash

    return '''
                <!doctype html>
                <title>Upload new File</title>
                <h1>Upload new File</h1>
                <form action="" method=post enctype=multipart/form-data>
                  <p><input type=file name=file>
                     <input type=submit value=Upload>
                </form>
                '''




@app.route('/download', methods=['GET', 'POST'])
def get_file():
    if request.method == 'POST':

        hash_data = request.get_json(force=True)['hash']
        hash_dir = hash_data[0:2]
        download_dir = UPLOAD_FOLDER + '\\' + hash_dir + '\\' + hash_data

        res = os.path.isfile(download_dir)
        if res == True:

            #uploads = os.path.join(app.root_path, download_dir)
            return send_file(download_dir,  as_attachment=True)

        else:
            return ('no such file')

    return ('need hash parameter')

@app.route('/delete', methods=['GET', 'POST'])
def del_file():
    if request.method == 'POST':

        hash_data = request.get_json(force=True)['hash']
        hash_dir = hash_data[0:2]
        download_dir = UPLOAD_FOLDER + '\\' + hash_dir + '\\' + hash_data

        res = os.path.isfile(download_dir)
        if res == True:

            os.remove(download_dir)
            return ('file successfully deleted')

        else:
            return ('no such file')

    return ('need hash parameter')


if __name__ == '__main__':
    app.run(debug=True)
