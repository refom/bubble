import os, pickle, re
from bubble import app
from bubble.strukturdata import RedBlackTree

KEYWORD_FILE = os.path.join(app.root_path, "static", "keyword.dll")

class NoData(object):
	def __init__(self):
		self.key = "../.."
		self.name = "No Data Found"

no_data = NoData()

def load_file():
	with open(KEYWORD_FILE, "rb") as kf:
		kata = pickle.load(kf)

	return kata

def save_file(kata):
	with open(KEYWORD_FILE, "wb") as kf:
		pickle.dump(kata, kf)

def set_strukdat(dokumen_html):

	# Check keyword file
	if not os.path.exists(KEYWORD_FILE):
		kata = RedBlackTree()
	else:
		kata = load_file()

	kata.add(dokumen_html)

	if kata:
		save_file(kata)

def get_data(keyword):
	# Ambil keyword dari search
	keyword = re.sub("[\W_]", " ", keyword.lower())

	# Cek apakah ada file keyword.dll
	if not os.path.exists(KEYWORD_FILE):
		return [no_data]

	# Load file keyword.dll
	kata = load_file()

	data = kata.query(keyword.split())

	return data

def cek_key():
	# Cek jika ada file keyword
	if os.path.exists(KEYWORD_FILE):
		kata = load_file()
		# mengembalikan tree
		return kata.get_tree("inorder")
	
	return "Tidak ada file"

def get_file():
	if os.path.exists(KEYWORD_FILE):
		kata = load_file()
		return kata.lane.get_tree_all()
	
	return ["Tidak ada file"]

