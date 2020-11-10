from bs4 import BeautifulSoup
from bubble import app
from ekstrak import parser_teks
import os

KEYWORD_FILE = os.path.join(app.root_path, "static", "keyword.dll")

class Node(object):
	def __init__(self, key):
		self.key    = key
		self.lokasi = []
		self.left   = None
		self.right  = None

	def input_lokasi(self, dokumen_html):
		if not dokumen_html in self.lokasi:
			self.lokasi.append(dokumen_html)


class BS_Tree(object):
	def __init__(self):
		self.root = None

	# Add / Bagian Parser
	def add(self, dokumen_html):
		# Parser isinya
		with open(dokumen_html, "r", encoding="utf8") as f:
			soup = BeautifulSoup(f.read(), "html.parser")
			x    = soup.find_all(["p", "title", "article"])

		# Pembuatan keyword
		teks = set(parser_teks(x))

		for key in teks:
			# Memasukkan ke dalam struktur data
			self.root = self.add_helper(self.root, key, dokumen_html)

		if self.root:
			print(" Add = True ")
			return self.root

		print(" Add = False ")
		return None
	
	# Add / Bagian memasukkan kedalam BST
	def add_helper(self, node, key, dokumen_html):

		# Kalau node gk ada, buat Node baru
		if not node:
			node_baru = Node(key)
			node_baru.input_lokasi(dokumen_html)
			return node_baru

		# Kalau key sudah ada, masukkan dokumen html ke node
		elif node.key == key:
			node.input_lokasi(dokumen_html)
			return node

		# Kalau key lebih kecil dari keynya node
		elif key < node.key:
			node.left = self.add_helper(node.left, key, dokumen_html)

		# Kalau key lebih besar dari keynya node
		node.right = self.add_helper(node.right, key, dokumen_html)

		# kembalikan node
		return node

	# Query / Bagian kesepakatan bersama
	def query(self, key):
		return self.query_helper(self.root, key)

	# Query / Bagian pencariannya
	def query_helper(self, node, key):

		# Jika key sama dengan node key, kembalikan node
		if key == node.key:
			return node
		
		# Jika key lebih kecil dari node key, cari lagi dengan nodenya adalah anak sebelah kiri dari node
		elif key < node.key:
			return self.query_helper(node.left, key)

		# Jika key lebih besar dari node key, cari lagi dengan nodenya adalah anak sebelah kanan dari node
		return self.query_helper(node.right, key)

	# Menampilkan tree
	def print_tree(self):
		teks = ""
		teks = self.print_tree_helper(self.root, teks)
		print(teks)

	# Tampilkan tree dengan berurutan dari yang paling kiri
	def print_tree_helper(self, root, teks):
		if root:
			teks = self.print_tree_helper(root.left, teks)
			teks += f"{root.key}, "
			teks = self.print_tree_helper(root.right, teks)
			return teks

	# Mengambil isi tree
	def get_tree(self):
		teks = ""
		return self.get_tree_helper(self.root, teks)

	# Mengembalikan nilai key tree
	def get_tree_helper(self, root, teks):
		if root:
			teks = self.get_tree_helper(root.left, teks)
			teks += f"{root.key}, "
			teks = self.get_tree_helper(root.right, teks)
			return teks





