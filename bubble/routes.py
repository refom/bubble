
import os
from flask import render_template, url_for, request, redirect, flash
from bubble import app
from bubble.forms import Search
from bubble.ekstrak import set_strukdat, get_data, get_file, cek_key

# Extension check
ALLOWED_EXTENSIONS = set(['html'])
def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# Route
@app.route("/", methods=['GET', 'POST'])
def index():
	form = Search()
	if request.method == 'POST':
		# Kalau searchnya di pakai, disini search algoritmanya
		keyword = form.keyword.data
		data = get_data(keyword)
		if data:
			return render_template('home.html', form=form, datas=data)
		
	return render_template('home.html', form=form)

@app.route("/add")
def add():
	return render_template('add.html')

@app.route("/add", methods=['POST'])
def upload_file():
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
				gagal += 1

		if gagal > 0:
			flash(f'Ada {gagal} File(s) failed uploaded.')
		else:
			flash('File(s) successfully uploaded.')

		return redirect(request.url)

@app.route("/key", methods=['GET'])
def cek_keyword():
	teks = cek_key()
	if teks:
		return render_template('cek_keyword.html', teks=teks)

@app.route("/delete", methods=['GET', 'POST'])
def delete():
	# Mengambil list file
	datas = get_file()
	if request.method == 'POST':
		# Jika file yang akan dihapus dipilih
		pass
	return render_template('delete.html', datas=data)


