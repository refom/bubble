
import os
from flask import render_template, url_for, request, redirect, flash
from bubble import app
from bubble.forms import Search
from bubble.ekstrak import set_keyword, get_data, get_file, cek_key

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
		return render_template('home.html', form=form, datas=data)
	return render_template('home.html', form=form)

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
			# Jika file sukses di upload, akan mengembalikan nilai True
			if file and allowed_file(file.filename):
				path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
				file.save(path)
				# INSERT / ADD filename
				set_keyword(path)
				flash('File(s) successfully uploaded. ')
			# Jika file gagal di upload, akan mengembalikan nilai False
			else:
				flash('File(s) failed to uploaded. ')

		return redirect(request.url)

@app.route("/key", methods=['GET'])
def cek_keyword():
	keylist = cek_key()
	return render_template('cek_keyword.html', keylist=keylist)

@app.route("/delete", methods=['GET', 'POST'])
def delete():
	# Mengambil list file
	datas = get_file()
	if request.method == 'POST':
		# Jika file yang akan dihapus dipilih
		pass
	return render_template('delete.html', datas=data)


