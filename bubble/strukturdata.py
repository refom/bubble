from bs4 import BeautifulSoup
import os, re

def parser_teks(teks, x=""):
	for i in teks:
		x += f"{i.text} "
	x = re.sub("[\W_]", " ", x.lower())
	return x.split()

BLACK = 0
RED = 1

class Node(object):
	def __init__(self, key):
		self.right  = None
		self.left   = None
		self.parent = None
		self.color = RED
		self.key   = key
		self.value = []

	def add_value(self, value):
		if not value in self.value:
			self.value.append(value)

	# Bila object di print
	def __str__(self):
		return f"Object Node, Key = {self.key}"

	# Jika self equal other
	def __eq__(self, other):
		return self.key == other.key
	
	# Jika self less than other
	def __lt__(self, other):
		return self.key < other.key

	# Jika self greater than other
	def __gt__(self, other):
		return self.key > other.key

	# Menambah value
	def __add__(self, other):
		self.value = self.value + other.value


class BS_Tree(object):
	def __init__(self):
		self.len_data = 0
		self.root = None

	# Query / Bagian kesepakatan bersama
	def query(self, key):
		return self.query_helper(self.root, key)

	# Query / Bagian pencariannya
	def query_helper(self, node, key):

		# Jika key sama dengan node key atau node adalah None, kembalikan node
		if node is None or key == node.key:
			return node
		
		# Jika key lebih kecil dari node key, cari lagi dengan nodenya adalah anak sebelah kiri dari node
		elif key < node.key:
			return self.query_helper(node.left, key)

		# Jika key lebih besar dari node key, cari lagi dengan nodenya adalah anak sebelah kanan dari node
		return self.query_helper(node.right, key)

	# Rotate Left
	# def rotate_left(self, node):
	# 	x = node
	# 	y = x.right
	# 	beta = y.left


class RedBlackTree(object):
	def __init__(self):
		self.len_data  = 0
		self.NIL       = Node(0)
		self.NIL.color = BLACK
		self.root      = self.NIL
	
	# Minimum
	def min(self, node):
		while node.left != self.NIL:
			node = node.left
		return node
	
	# Maximum
	def max(self, node):
		while node.right != self.NIL:
			node = node.right
		return node

	# Successor
	def successor(self, node):
		# Kondisi 1, Anak kanan tidak kosong
		if node.right != self.NIL:
			return self.min(node.right)

		# Kondisi 2, Anak kanan kosong
		node_parent = node.parent
		while node_parent != self.NIL and node == node_parent.right:
			node        = node_parent
			node_parent = node_parent.parent
		return node_parent

	# Predecessor
	def predecessor(self, node):
		# Kondisi 1, Anak kiri tidak kosong
		if node.left != self.NIL:
			return self.max(node.left)

		# Kondisi 2, Anak kiri kosong
		node_parent = node.parent
		while node_parent != self.NIL and node == node_parent.left:
			node        = node_parent
			node_parent = node_parent.parent
		return node_parent

	# Mengambil isi tree
	def get_tree(self, param):
		teks = " "
		if param == "inorder":
			teks = self.get_tree_inorder(self.root, teks)
		elif param == "preorder":
			teks = self.get_tree_preorder(self.root, teks)
		elif param == "postorder":
			teks = self.get_tree_postorder(self.root, teks)
		return teks

	# Inorder | Mengambil isi tree dan Mengembalikan nilai key tree
	def get_tree_inorder(self, node, teks):
		if node != self.NIL:
			teks  = self.get_tree_inorder(node.left, teks)
			teks += f"{node.key}, "
			teks  = self.get_tree_inorder(node.right, teks)
		return teks

	# Preorder | Mengambil isi tree dan Mengembalikan nilai key tree
	def get_tree_preorder(self, node, teks):
		if node != self.NIL:
			teks += f"{node.key}, "
			teks  = self.get_tree_preorder(node.left, teks)
			teks  = self.get_tree_preorder(node.right, teks)
		return teks
	
	# Postorder | Mengambil isi tree dan Mengembalikan nilai key tree
	def get_tree_postorder(self, node, teks):
		if node != self.NIL:
			teks  = self.get_tree_postorder(node.left, teks)
			teks  = self.get_tree_postorder(node.right, teks)
			teks += f"{node.key}, "
		return teks


	# ADD
	def add(self, dokumen_html):
		# Parser isinya
		with open(dokumen_html, "rb") as f:
			soup = BeautifulSoup(f.read(), "html.parser")
			x    = soup.find_all(["p", "title", "article"])

		# Pembuatan keyword
		teks = set(parser_teks(x))

		for key in teks:
			new_node       = Node(key)
			new_node.add_value(dokumen_html)
			new_node.left  = self.NIL
			new_node.right = self.NIL

			# Memasukkan ke dalam struktur data
			self.add_helper(new_node)

		return

	def add_helper(self, new_node):
		lf    = None
		node = self.root
		
		# Cari leafnya (lf)
		while node != self.NIL:
			lf = node
			if new_node == node:
				node + new_node
				new_node = None
				return
			elif new_node < node:
				node = node.left
			else:
				node = node.right
		
		# Buat leaf sebagai parent dari new node
		new_node.parent = lf

		# Jika leafnya gak ada, maka new node adalah root
		# Jika leafnya ada dan new node lebih kecil dari leaf maka anak kiri dari leaf adalah new node. Berlaku sebaliknya
		if lf == None:
			self.root = new_node
		elif new_node < lf:
			lf.left = new_node
		else:
			lf.right = new_node

		# Jika parentnya gak ada, berarti dia root
		if new_node.parent == None:
			node.color = BLACK
			return
		
		# Bentuk tree yang berisi hanya 3 data yaitu root, root.left dan root.right.
		# Pastinya root adalah black, dan kedua anaknya adalah red.
		#  Bentuk ini tidaklah melanggar rule apapun
		if new_node.parent.parent == None:
			return

		# Periksa jika ada yang melanggar rule
		self.fix_insert(new_node)

	# Cek apakah ada yang melanggar rule
	def fix_insert(self, node):
		if node.parent.color == RED:
			pass





