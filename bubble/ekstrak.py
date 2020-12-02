import os, pickle, re
from bubble import app
from bubble.strukturdata import RedBlackTree

KEYWORD_FILE = os.path.join(app.root_path, "static", "keyword.dll")

class NoData(object):
	def __init__(self):
		self.key = "../.."
		self.name = "No Data Found"

no_data = NoData()

def set_strukdat(dokumen_html):

	# Check keyword file
	if not os.path.exists(KEYWORD_FILE):
		kata = RedBlackTree()
	else:
		with open(KEYWORD_FILE, "rb") as kf:
			kata = pickle.load(kf)

	kata.add(dokumen_html)

	if kata:
		with open(KEYWORD_FILE, "wb") as kf:
			pickle.dump(kata, kf)

def get_data(keyword):
	# Ambil keyword dari search
	keyword = re.sub("[\W_]", " ", keyword.lower())

	# Cek apakah ada file keyword.dll
	if not os.path.exists(KEYWORD_FILE):
		return [no_data]

	# Load file keyword.dll
	with open(KEYWORD_FILE, "rb") as kf:
		kata = pickle.load(kf)

	data = kata.query(keyword.split())

	return data

def cek_key():
	# Cek jika ada file keyword
	if os.path.exists(KEYWORD_FILE):
		# memuat keyword file
		with open(KEYWORD_FILE, "rb") as kf:
			kata = pickle.load(kf)
		# mengembalikan tree
		return kata.get_tree("inorder")
	
	return "Tidak ada file"


# def	get_file():
# 	pass
