
import os
from flask import render_template, url_for, request, redirect, flash
from bubble import app
from bubble.forms import Search

# Extension check
ALLOWED_EXTENSIONS = set(['html'])
def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# Route
@app.route("/", methods=['GET', 'POST'])
def index():
	form = Search()
	if form.validate_on_submit():
		# Kalau searchnya di pakai, disini search algoritmanya
		return redirect(request.url)
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
			if file and allowed_file(file.filename):
				file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
				# index_file = insertFile(file.filename)
				# Keyword(filename, index_file)

		flash('File(s) successfully uploaded')
		return redirect(request.url)

