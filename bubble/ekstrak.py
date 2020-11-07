import os, pickle, re
from bubble.strukturdata import RedBlackTree
from bubble import app
from bs4 import BeautifulSoup

KEYWORD_FILE = os.path.join(app.root_path, "static", "keyword.dll")
LOKASI_FILE = os.path.join(app.root_path, "static", "lokasi.dll")

def set_strukdat(teks, path):

	# Check keyword file
	if not os.path.exists(KEYWORD_FILE):
		rbt = RedBlackTree()
	else:
		with open(KEYWORD_FILE, "rb") as kf:
			rbt = pickle.load(kf)

	for key in teks:
		rbt.insert(key, path)

	with open(KEYWORD_FILE, "wb") as kf:
		pickle.dump(rbt, kf)

def get_data(keyword):
	# Ambil keyword dari search
	keyword = re.sub("[\W_]", " ", keyword.lower())

	# Load keyword file
	with open(KEYWORD_FILE, "rb") as kf:
		rbt = pickle.load(kf)

	lokasi = []
	# cari tiap keyword
	for key in keyword.split():
		print(key)
		dataNode = rbt.query(key)
		if dataNode:
			for lok in dataNode.loc:
				print(lok)
				if not lok in lokasi:
					lok = os.path.basename(lok)
					name = os.path.splitext(lok)
					lokasi.append([name[0], lok])

	return lokasi

def parser_teks(teks):
	x = ""
	for i in teks:
		x += f"{i.text} "
	x = re.sub("[\W_]", " ", x.lower())
	return x.split()

def set_keyword(path):
	# Parser isinya
	with open(path, "r", encoding="utf8") as f:
		soup = BeautifulSoup(f.read(), "html.parser")
		x    = soup.find_all(["p", "title", "article"])

	# Pembuatan keyword
	teks = set(parser_teks(x))

	# Memasukkan ke dalam struktur data
	set_strukdat(teks, path)

def cek_key():
	with open(KEYWORD_FILE, "rb") as kf:
		rbt = pickle.load(kf)
	keylist = []
	return rbt.get_preOrder(keylist)

def	get_file():
	pass
