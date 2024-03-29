from flask import Flask, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
import os

UPLOAD_FOLDER = '/path/to/the/uploads'
ALLOWED_EXTENSIONS = {'pdf'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = 'supersecretkey'  # Needed to use 'flash'

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'document' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['document']
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        try:
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            flash('File successfully uploaded')
            return redirect(url_for('upload_file'))  # Redirect to the upload page or to a 'success' page
        except Exception as e:
            flash('An error occurred: ' + str(e))
            return redirect(url_for('upload_file'))
    else:
        flash('Allowed file types are: pdf')
        return redirect(request.url)

if __name__ == "__main__":
    app.run(debug=True)
