
import os
from flask import render_template, url_for, request, redirect, flash
from bubble import app
from bubble.forms import Search
from bubble.ekstrak import *

# Extension check
ALLOWED_EXTENSIONS = set(['html'])
def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# Route
@app.route("/")
def index():
	form = Search()
	return render_template('home.html', form=form)

@app.route("/", methods=['POST'])
def search():
	form = Search()
	if request.method == 'POST':
		# Kalau searchnya di pakai, disini search algoritmanya
		keyword = form.keyword.data
		data = get_data(keyword)
	return render_template('home.html', form=form, datas=data)


@app.route("/insert")
def insert():
	return render_template('insert.html')

@app.route("/insert", methods=['POST'])
def upload_file():
	if request.method == 'POST':
		if 'files[]' not in request.files:
			flash('No file part')
			return redirect(request.url)

		files = request.files.getlist('files[]')

		for file in files:
			if file and allowed_file(file.filename):
				path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
				file.save(path)
				set_keyword(path)

		flash('File(s) successfully uploaded')
		return redirect(request.url)

@app.route("/key", methods=['GET'])
def cek_keyword():
	keylist = cek_key()
	return render_template('cek_keyword.html', keylist=keylist)


