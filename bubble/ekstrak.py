import os, pickle, re
from bubble.strukturdata import BS_Tree
from bubble import app

KEYWORD_FILE = os.path.join(app.root_path, "static", "keyword.dll")
# LOKASI_FILE = os.path.join(app.root_path, "static", "lokasi.dll")


def parser_teks(teks):
	x = ""
	for i in teks:
		x += f"{i.text} "
	x = re.sub("[\W_]", " ", x.lower())
	return x.split()


def set_strukdat(teks, dokumen_html):

	# Check keyword file
	if not os.path.exists(KEYWORD_FILE):
		bst = BS_Tree()
	else:
		with open(KEYWORD_FILE, "rb") as kf:
			bst = pickle.load(kf)

	bst = bst.add(dokumen_html)

	if bst:
		with open(KEYWORD_FILE, "wb") as kf:
			pickle.dump(bst, kf)


def get_data(keyword):
	# Ambil keyword dari search
	keyword = re.sub("[\W_]", " ", keyword.lower())

	# Cek apakah ada file keyword.dll
	if not os.path.exists(KEYWORD_FILE):
		return [["Tidak ada data, harap untuk mengupload data", ""]]

	# Load file keyword.dll
	with open(KEYWORD_FILE, "rb") as kf:
		bst = pickle.load(kf)

	data = []
	# cari tiap keyword
	for key in keyword.split():
		node = bst.query(key)
		if node:
			for lokasi in node.lokasi:
				if not lokasi in data:
					lokasi = os.path.basename(lokasi)
					judul  = os.path.splitext(lokasi)
					data.append([judul[0], lokasi])

	return data


def cek_key():
	# Cek jika ada file keyword
	if os.path.exists(KEYWORD_FILE):
		# memuat keyword file
		with open(KEYWORD_FILE, "rb") as kf:
			bst = pickle.load(kf)
		# mengembalikan tree
		return bst.get_tree()
	
	return "Tidak ada file"


# def	get_file():
# 	pass
