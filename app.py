from flask import Flask, render_template, request, redirect, send_from_directory, url_for, flash
import os
from werkzeug.utils import secure_filename


APP_ROOT = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER', '/data')
ALLOWED_EXT = None # allow all
MAX_CONTENT_LENGTH = 1024 * 1024 * 1024 # 1 GiB per upload (adjust if needed)


os.makedirs(UPLOAD_FOLDER, exist_ok=True)


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH
app.secret_key = 'fdtx-fileshare-secret'




@app.route('/', methods=['GET', 'POST'])
def index():
if request.method == 'POST':
# handle upload
if 'file' not in request.files:
flash('No file part')
return redirect(request.url)
file = request.files['file']
if file.filename == '':
flash('No selected file')
return redirect(request.url)
filename = secure_filename(file.filename)
save_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
file.save(save_path)
flash(f'Uploaded {filename}')
return redirect(url_for('index'))


# list files
entries = []
for name in sorted(os.listdir(app.config['UPLOAD_FOLDER'])):
full = os.path.join(app.config['UPLOAD_FOLDER'], name)
if os.path.isfile(full):
size = os.path.getsize(full)
entries.append({'name': name, 'size': size})
return render_template('index.html', files=entries)




@app.route('/download/<path:filename>')
def download(filename):
filename = secure_filename(filename)
return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)




@app.route('/delete/<path:filename>', methods=['POST'])
def delete_file(filename):
filename = secure_filename(filename)
path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
if os.path.exists(path):
os.remove(path)
flash(f'Deleted {filename}')
else:
flash('File not found')
return redirect(url_for('index'))




if __name__ == '__main__':
# dev server
app.run(host='0.0.0.0', port=8080, debug=True)