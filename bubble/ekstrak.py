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

def get_file():
	if os.path.exists(KEYWORD_FILE):
		kata = load_file()
		return kata.lane.get_tree_all()
	
	return ["Tidak ada file"]

def delete_file(filename):
	if os.path.exists(KEYWORD_FILE):
		kata = load_file()
		kata.delete(filename)
	
	save_file(kata)

def checking(param):
	if os.path.exists(KEYWORD_FILE):
		kata = load_file()

		if param == "root":
			root = kata.get_root()
			return f"Key = {root.key}, color = {root.color}, Left Child = {root.left.key}, Right Child = {root.right.key}, Parent = {root.parent}"

		if param == "successor":
			node = kata.successor(kata.root)
			return f"Successor from root = {node.key}"

		if param == "predecessor":
			node = kata.predecessor(kata.root)
			return f"Predecessor from root = {node.key}"

		if param == "inorder":
			return kata.get_tree("inorder")

		if param == "preorder":
			return kata.get_tree("preorder")

		if param == "postorder":
			return kata.get_tree("postorder")

		if param == "len":
			banyak = kata.get_len_data()
			return f"Banyak Data = {banyak}"

		if param == "min":
			node = kata.min(kata.root)
			return f"Minimum from root = {node.key}"

		if param == "max":
			node = kata.max(kata.root)
			return f"Maximum from root = {node.key}"
		

	return "Nothing in here"
