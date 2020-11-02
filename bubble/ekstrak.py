import os, pickle, re
from bubble.strukturdata import AVL_Tree
from bubble import app
from bs4 import BeautifulSoup

KEYWORD_FILE = os.path.join(app.root_path, "static", "keyword.dll")

def set_strukdat(teks, path):
	# Root = None
	r = None
	keyword = AVL_Tree()

	# Check keyword file
	if not os.path.exists(KEYWORD_FILE):
		with open(KEYWORD_FILE, "wb") as kf:
			pickle.dump(r, kf)
	else:
		with open(KEYWORD_FILE, "rb") as kf:
			r = pickle.load(kf)

	for key in teks:
		r = keyword.insert(r, key, path)

	with open(KEYWORD_FILE, "wb") as kf:
		pickle.dump(r, kf)


def get_data():
	with open(KEYWORD_FILE, "rb") as kf:
		r = pickle.load(kf)
	keyword = AVL_Tree()
	keyword.search(r, "ROOT")

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
		r = pickle.load(kf)
	keyword = AVL_Tree()
	keylist = []
	return keyword.get_preOrder(r, "ROOT", keylist)

