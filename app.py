from flask import Flask, render_template, request, redirect, send_from_directory, url_for, flash
import os
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = '/data'   # This will exist once the PVC is mounted

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = 'fdtx-fileshare-secret'


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files.get('file')
        if not file or file.filename == '':
            flash('No file selected')
            return redirect('/')

        filename = secure_filename(file.filename)
        save_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(save_path)
        flash(f'Uploaded {filename}')
        return redirect('/')

    files = []
    if os.path.exists(UPLOAD_FOLDER):
        for f in sorted(os.listdir(UPLOAD_FOLDER)):
            full = os.path.join(UPLOAD_FOLDER, f)
            if os.path.isfile(full):
                files.append({'name': f, "size": round(os.path.getsize(filepath) / (1024 * 1024), 2)})

    return render_template('index.html', files=files)


@app.route('/download/<path:filename>')
def download(filename):
    filename = secure_filename(filename)
    return send_from_directory(UPLOAD_FOLDER, filename, as_attachment=True)


@app.route('/delete/<path:filename>', methods=['POST'])
def delete_file(filename):
    filename = secure_filename(filename)
    path = os.path.join(UPLOAD_FOLDER, filename)

    if os.path.exists(path):
        os.remove(path)
        flash(f'Deleted {filename}')
    else:
        flash('File not found')

    return redirect('/')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)

