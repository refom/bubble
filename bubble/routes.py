
import os
from flask import render_template, url_for, request, redirect, flash
from flask_paginate import Pagination, get_page_args
from bubble import app
from bubble.forms import Search
from bubble.ekstrak import set_strukdat, get_data, get_file, delete_file, checking

data_temp = []

# Extension check
ALLOWED_EXTENSIONS = set(['html', 'htm'])
def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_per_data(data, offset=0, per_page=10):
    return data[offset: offset + per_page]

def check_data_temp():
	if data_temp:
		data_temp.clear()

# Route
@app.route("/", methods=['GET', 'POST'])
def index():
	form = Search()
	if request.method == "POST":
		check_data_temp()
		data, time_required = get_data(form.keyword.data)
		if data:
			data_temp.append(data)
			data_temp.append(time_required)
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
								pagination=pagination,
								time=data_temp[1])
	return redirect(url_for('index'))

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

@app.route("/key/<param>", methods=['GET'])
def check(param):
	if param:
		teks = checking(param)
		return render_template('check.html', param=param, teks=teks)
	return render_template('check.html')

@app.route("/delete", methods=['GET', 'POST'])
def delete():
	if request.method == 'POST':
		for key, value in request.form.items():
			if key == "button":
				if value == "get":
					check_data_temp()
					data = get_file()
					if data:
						data_temp.append(data)
					return redirect(request.url)
				else:
					delete_file(value)
					if value in data_temp[0]:
						data_temp[0].remove(value)
						os.remove(os.path.join(app.config['UPLOAD_FOLDER'], value))
					return redirect(request.url)

	if data_temp:
		data = data_temp[0]
		page, per_page, offset = get_page_args(page_parameter='page', per_page_parameter='per_page', )
		pagination_data = get_per_data(data, offset=offset, per_page=per_page)
		pagination = Pagination(page=page, per_page=per_page, total=len(data), css_framework='bootstrap4')
		return render_template('delete.html',
								data=pagination_data,
								pagination=pagination)
	return render_template('delete.html')



