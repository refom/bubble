
import os
from flask import render_template, url_for, request, redirect, flash
from flask_paginate import Pagination, get_page_args
from bubble import app
from bubble.forms import Search
from bubble.ekstrak import set_strukdat, get_data, cek_key

data_temp = []

# Extension check
ALLOWED_EXTENSIONS = set(['html', 'htm'])
def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_per_data(data, offset=0, per_page=10):
    return data[offset: offset + per_page]

# Route
@app.route("/", methods=['GET', 'POST'])
def index():
	form = Search()
	if request.method == "POST":
		if data_temp:
			data_temp.clear()
		data = get_data(form.keyword.data)
		if data:
			data_temp.append(data)
		return redirect(url_for('search'))
	return render_template('home.html', form=form)

@app.route("/search", methods=['GET', 'POST'])
def search():
	if data_temp:
		data = data_temp[0]
		page, per_page, offset = get_page_args(page_parameter='page', per_page_parameter='per_page', )
		pagination_data = get_per_data(data, offset=offset, per_page=per_page)
		pagination = Pagination(page=page, per_page=per_page, total=len(data), css_framework='bootstrap4')
		return render_template('search.html',
								data=pagination_data,
								pagination=pagination)
	return render_template('search.html', data=["No data Found"])

@app.route("/add", methods=['GET', 'POST'])
def add():
	if request.method == 'POST':
		if 'files[]' not in request.files:
			flash('No file part')
			return redirect(request.url)

		# mengambil apa yang user upload. Filenya dalam bentuk list
		files = request.files.getlist('files[]')

		gagal = 0

		# perulangan untuk mengambil file file yg diupload tadi
		for file in files:

			# Pengecekan apakah filenya ada dan extensinya html atau tidak
			if file and allowed_file(file.filename):
				path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
				file.save(path)

				# ADD file ke struktur data
				set_strukdat(path)

			# Jika file gagal di upload, akan mengembalikan nilai False
			else:
				print(" Add = False")
				gagal += 1

		if gagal > 0:
			flash(f'Ada {gagal} File(s) failed uploaded.')
		else:
			flash('File(s) successfully uploaded.')

		return redirect(request.url)
	return render_template('add.html')

@app.route("/key", methods=['GET'])
def cek_keyword():
	teks = cek_key()
	return render_template('cek_keyword.html', teks=teks)

@app.route("/delete", methods=['GET', 'POST'])
def delete():
	# Mengambil list file
	datas = get_file()
	if request.method == 'POST':
		# Jika file yang akan dihapus dipilih
		pass
	return render_template('delete.html', datas=data)


