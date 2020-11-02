import os
from flask import Flask


app = Flask(__name__)
app.config['SECRET_KEY'] = '45270fd9edf1d068cf42565bc04cbd01'
# Max 16 MB upload
app.config['MAX_CONTENT_LENGTH'] = 160 * 1024 * 1024

UPLOAD_FOLDER = os.path.join(app.root_path, 'static', 'data')
if not os.path.exists(UPLOAD_FOLDER):
	os.mkdir(UPLOAD_FOLDER)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

from bubble import routes
