from flask import Flask, request, jsonify, send_from_directory, abort, render_template
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os

UPLOAD_FOLDER = 'uploads'  # 替換成你想要上傳文件保存的地方
ALLOWED_EXTENSIONS = set(['pdf'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = os.path.abspath(UPLOAD_FOLDER)
CORS(app)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET'])
def upload_file():
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form action="/files" method=post enctype=multipart/form-data>
      <input type=file name=file multiple>
      <input type=text name=prefix multiple>
      <input type=submit value=Upload>
    </form>
    '''


@app.route('/files', methods=['GET', 'POST'])
def list_upload_files():
    if request.method == 'POST':
        files = request.files.getlist("file")
        prefix = request.form.get('prefix', default=None, type=str)
        results = []
        for file in files:
            if file and allowed_file(file.filename):
                filename = (prefix if prefix else "")+secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                results.append(filename)
        return jsonify({"message": "File uploaded successfully.", "filenames": results}), 200
    files = os.listdir(app.config['UPLOAD_FOLDER'])
    print(files)
    return render_template('files.html', files=files)
    # return jsonify(files)


@app.route('/files/<filename>', methods=['GET'])
def get_file(filename):
    if os.path.exists(os.path.join(app.config['UPLOAD_FOLDER'], filename)):
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)
    else:
        abort(404, description="File not found")


@app.route('/files/<filename>', methods=['DELETE'])
def delete_file(filename):
    file_path = os.path.abspath(os.path.join(
        app.config['UPLOAD_FOLDER'], filename))

    if not file_path.startswith(app.config['UPLOAD_FOLDER']):
        abort(403, description="Unauthorized request")

    if os.path.exists(file_path):
        os.remove(file_path)
        return jsonify({"message": f"'{filename}' has been deleted."}), 200
    else:
        abort(404, description=f"'{filename}' not found.")


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8002)
