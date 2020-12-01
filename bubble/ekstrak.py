import os, pickle, re
from bubble import app
from bubble.strukturdata import RedBlackTree

KEYWORD_FILE = os.path.join(app.root_path, "static", "keyword.dll")


def set_strukdat(dokumen_html):

	# Check keyword file
	if not os.path.exists(KEYWORD_FILE):
		keyword = RedBlackTree()
	else:
		with open(KEYWORD_FILE, "rb") as kf:
			keyword = pickle.load(kf)

	keyword.add(dokumen_html)

	if keyword:
		with open(KEYWORD_FILE, "wb") as kf:
			pickle.dump(keyword, kf)

def get_data(keyword):
	# Ambil keyword dari search
	keyword = re.sub("[\W_]", " ", keyword.lower())

	# Cek apakah ada file keyword.dll
	if not os.path.exists(KEYWORD_FILE):
		return [["No data Found", "../.."]]

	# Load file keyword.dll
	with open(KEYWORD_FILE, "rb") as kf:
		rbt = pickle.load(kf)

	data = []
	# cari tiap keyword
	for kata in keyword.split():
		node = rbt.query(kata)
		if node:
			for lokasi in node.value:
				if not lokasi in data:
					link  = os.path.basename(lokasi)
					judul = os.path.splitext(link)
					data.append([judul[0], link])

	return data

def cek_key():
	# Cek jika ada file keyword
	if os.path.exists(KEYWORD_FILE):
		# memuat keyword file
		with open(KEYWORD_FILE, "rb") as kf:
			rbt = pickle.load(kf)
		# mengembalikan tree
		return rbt.get_tree("inorder")
	
	return "Tidak ada file"


# def	get_file():
# 	pass
