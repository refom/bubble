from bs4 import BeautifulSoup
from time import process_time
import os, re

def parser_teks(teks, x=""):
	for i in teks:
		x += f"{i.text} "
	x = re.sub("[\W_]", " ", x.lower())
	return x.split()

def parser_html(dokumen_html):
	# Parser isinya
	with open(dokumen_html, "rb") as f:
		soup = BeautifulSoup(f.read(), "html.parser")
		x    = soup.find_all(["p", "title", "article"])

	# Pembuatan keyword
	teks = set(parser_teks(x))
	return teks

def parser_link(link):
	base = os.path.basename(link)
	name = os.path.splitext(base)
	name = name[0]
	return base, name


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
		self.add_value(other.value[0])


class RedBlackTree(object):
	""" 
		Rule Red Black Tree
	1. Node bisa RED / BLACK
	2. Root selalu BLACK
	3. Leaf selalu BLACK
	4. Jika Node RED, maka kedua anaknya BLACK
	5. Setiap jalan dari root ke leaf selalu memiliki jumlah BLACK node yang sama

		variable yang akan digunakan disini
	node     = Node sekarang
	p        = Parent
	y        = Paman
	p.parent = Nenek
	lf       = Leaf
	"""
	def __init__(self):
		self.len_data  = 0
		self.NIL       = Node(0)
		self.NIL.color = BLACK
		self.root      = self.NIL
		self.lane      = None

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
		p = node.parent
		while p != self.NIL and node == p.right:
			node = p
			p    = p.parent
		return p

	# Predecessor
	def predecessor(self, node):
		# Kondisi 1, Anak kiri tidak kosong
		if node.left != self.NIL:
			return self.max(node.left)

		# Kondisi 2, Anak kiri kosong
		p = node.parent
		while p != self.NIL and node == p.left:
			node = p
			p    = p.parent
		return p

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

	# Ambil panjang data
	def get_len_data(self):
		return self.len_data

	# Cek lanenya
	def check_lane(self):
		if not self.lane:
			self.lane = RBT_Lane()

	# Print Tree
	def print_tree(self):
		self.print_tree_helper(self.root)

	def print_tree_helper(self, node):
		if node != self.NIL:
			self.print_tree_helper(node.left)
			print(node, end=". ")
			self.print_tree_helper(node.right)

	""" Rotate (Left/Right)
	node = Node yang akan di rotasi
	a    = anak (kanan/kiri) node
	beta = anak (kiri/kanan) dari a
	p    = parent dari node
	"""
	def rotate_left(self, node):
		# print("[L] Rotate Left Called")
		a, p = node.right, node.parent

		"""
		anak kanan node adalah beta
		Jika beta ada, maka:
		1. parent dari beta adalah node
		"""
		node.right = a.left
		if a.left != self.NIL:
			a.left.parent = node

		"""
		Jika parent adalah None, maka a jadi root
		Jika node adalah anak kiri parent, maka anak kiri parent menjadi a.
		Berlaku sebaliknya """
		a.parent    = p
		if p is None:
			self.root = a
		elif node == p.left:
			p.left = a
		else:
			p.right = a

		node.parent = a
		a.left      = node
		# print("[L-] Rotate Left Done")

	def rotate_right(self, node):
		# print("[R] Rotate Right Called")
		a, p = node.left, node.parent

		node.left = a.right
		if a.right != self.NIL:
			a.right.parent = node

		if p is None:
			self.root = a
		elif node == p.left:
			p.left = a
		else:
			p.right = a

		a.parent    = p
		node.parent = a
		a.right     = node
		# print("[R] Rotate Right Done")


	# Add (keyword) / Bagian kesepakatan bersama
	def add(self, dokumen_html):
		now = process_time()
		# print("[A] Add Called")
		# Mendapatkan teks
		teks      = parser_html(dokumen_html)
		html_base, name = parser_link(dokumen_html)

		lane       = Node(html_base)
		lane.left  = self.NIL
		lane.right = self.NIL
		lane.name  = name

		for kata in teks:
			# Masukkan kata ke dalam node lane
			lane.add_value(kata)

			# Buat kata menjadi node
			new_node       = Node(kata)
			new_node.add_value(lane)
			new_node.left  = self.NIL
			new_node.right = self.NIL
			# print(new_node)
			# Masukkan node ke dalam struktur data
			self.add_helper(new_node)

		self.check_lane()
		self.lane.add_helper(lane)

		# print("[A-] Add Done")
		after = process_time()
		print(f"- Elapsed time : {after - now}")
		return

	# Add / Bagian BST
	def add_helper(self, new_node):
		# print("[AH] Add Helper Called")
		lf   = None
		node = self.root
		
		# Cari leaf (lf)
		while node != self.NIL:
			lf = node
			if new_node == node:
				node + new_node
				new_node = None
				# print("[i] kata yang sama ditemukan")
				return
			elif new_node < node:
				node = node.left
			else:
				node = node.right
		
		# Buat leaf sebagai parent dari new node
		new_node.parent = lf
		self.len_data += 1
		""" Jika leafnya gak ada, maka new node adalah root.
		Jika leafnya ada dan new node lebih kecil dari leaf maka anak kiri dari leaf adalah new node.
		Berlaku sebaliknya """
		if lf is None:
			self.root = new_node
		elif new_node < lf:
			lf.left = new_node
		else:
			lf.right = new_node

		""" Kondisi Root
		Jika parentnya gak ada, berarti dia root.
		Sesuai rule no.2 Root adalah BLACK """
		if new_node.parent is None:
			node.color = BLACK
			# print("[i] new_node adalah root")
			return
		
		""" Kondisi Nenek
		Jika neneknya tidak ada, maka bentuk treenya hanya berisi 2/3 data yaitu root dan root.left atau root.right.
		Pastinya root adalah BLACK, dan anaknya adalah RED.
		Bentuk ini tidaklah melanggar rule """
		if new_node.parent.parent is None:
			# print("[i] nenek new_node tidak ada ")
			return

		# Periksa jika ada yang melanggar rule
		self.fix_add(new_node)
		# print("[AH-] Add Helper Done")

	# Add / Bagian pemeriksa apakah ada yang melanggar rule
	def fix_add(self, node):
		# print("[FA] Fix Add Called")

		""" Jika parentnya BLACK, maka tidak melanggar rule.
		Selama parentnya RED, maka melanggar rule no.5 karena anaknya parent adalah RED """
		while node.parent.color == RED:
			p = node.parent
			""" Jika parent berada di kiri nenek, maka paman node berada di kanan nenek """
			# PARENT<-NENEK (LEFT)
			if p == p.parent.left:
				y = p.parent.right
				
				""" Kondisi 1
				1. Jika pamannya RED
				1.1 Nenek (p.parent) jadi RED
				1.2 Parent (p) dan Paman (y) jadi BLACK
				1.3 Update node sekarang menjadi nenek dan p adalah parent dari node yang baru
				"""
				if y.color == RED:
					p.parent.color = RED
					p.color = y.color = BLACK
					node = p.parent
				else:
					"""
					2. Jika pamannya BLACK
					2.1 Cek kondisi LEFT-RIGHT (2), jika iya maka Rotate Left lalu tukar nilai node dan p
					2.2 Jika tidak maka kondisinya LEFT-LEFT (3). Parent menjadi BLACK, nenek menjadi RED, lalu Rotate Right
					"""
					""" Kondisi 2 """
					# PARENT->NODE (RIGHT)
					if node == p.right:
						self.rotate_left(p)
						node, p = p, node

					""" Kondisi 3 """
					# NODE<-PARENT (LEFT)
					p.color        = BLACK
					p.parent.color = RED
					self.rotate_right(p.parent)
			
			# NENEK->PARENT (RIGHT)
			else:
				y = p.parent.left

				if y.color == RED:
					p.parent.color = RED
					p.color = y.color = BLACK
					node = p.parent
				else:
					# NODE<-PARENT (LEFT)
					if node == p.left:
						self.rotate_right(p)
						node, p = p, node

					# PARENT->NODE (RIGHT)
					p.color        = BLACK
					p.parent.color = RED
					self.rotate_left(p.parent)

			# Jika nodenya sudah sampai di root, maka selesai
			if node == self.root:
				break

		# Sesuai rule no.2
		self.root.color = BLACK
		# print("[FA-] Fix Add Done")


	# Query / Bagian kesepakatan bersama
	def query(self, kata):
		return self.query_helper(self.root, kata)

	# Query / Bagian pencariannya
	def query_helper(self, node, kata):

		# Jika kata sama dengan node key atau node adalah NIL, kembalikan node
		if node == self.NIL or kata == node.key:
			return node
		
		# Jika kata lebih kecil dari node key, cari lagi dengan nodenya adalah anak sebelah kiri dari node
		elif kata < node.key:
			return self.query_helper(node.left, kata)

		# Jika kata lebih besar dari node key, cari lagi dengan nodenya adalah anak sebelah kanan dari node
		return self.query_helper(node.right, kata)


class RBT_Lane(RedBlackTree):

	def __init__(self):
		super().__init__()

	def check_lane():
		return

