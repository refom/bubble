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
		return f"Node = {self.key}"
	
	# Jika self less than other
	def __lt__(self, other):
		return self.key < other.key

	# Jika self greater than other
	def __gt__(self, other):
		return self.key > other.key

	# Menambah value
	def __add__(self, other):
		self.value = self.value + other.value


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
	lane     = File HTML
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
		while p != None and node == p.right:
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
		while p != None and node == p.left:
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

	# Ambil root
	def get_root(self):
		return self.root

	# Ambil semua data
	def get_tree_all(self):
		data = []
		return self.get_tree_all_helper(self.root, data)

	def get_tree_all_helper(self, node, data):
		if node != self.NIL:
			data = self.get_tree_all_helper(node.left, data)
			data.append(node.key)
			data = self.get_tree_all_helper(node.right, data)
		return data

	# Cek lanenya
	def check_lane(self):
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
		a.parent = p
		if p == None:
			self.root = a
		elif node == p.left:
			p.left = a
		else:
			p.right = a

		node.parent = a
		a.left      = node

	def rotate_right(self, node):
		a, p = node.left, node.parent

		node.left = a.right
		if a.right != self.NIL:
			a.right.parent = node

		a.parent = p
		if p == None:
			self.root = a
		elif node == p.left:
			p.left = a
		else:
			p.right = a

		node.parent = a
		a.right     = node


	# Add (keyword) / Bagian kesepakatan bersama
	def add(self, dokumen_html):
		now = process_time()
		# Mendapatkan teks
		teks      = parser_html(dokumen_html)
		html_base = os.path.basename(dokumen_html)

		if self.lane == None:
			self.check_lane()

		lane       = Node(html_base)
		lane.left  = self.lane.NIL
		lane.right = self.lane.NIL

		for kata in teks:
			# Buat kata menjadi node
			new_node       = Node(kata)
			new_node.add_value(html_base)
			new_node.left  = self.NIL
			new_node.right = self.NIL

			# Masukkan node ke dalam struktur data
			self.add_helper(new_node, lane)

		self.lane.add_helper(lane)

		after = process_time()
		print(f"- Elapsed time : {after - now}")

	# Add / Bagian BST
	def add_helper(self, new_node, lane):
		lf   = None
		node = self.root
		
		# Cari leaf (lf)
		while node != self.NIL:
			lf = node
			if new_node.key == node.key:
				node + new_node
				new_node = None
				# Masukkan node ke dalam lane
				lane.add_value(node)
				return
			elif new_node < node:
				node = node.left
			else:
				node = node.right
		
		# Buat leaf sebagai parent dari new node
		new_node.parent = lf
		# Masukkan new node ke dalam lane
		lane.add_value(new_node)
		self.len_data += 1
		""" Jika leafnya kosong, maka new node adalah root.
		Jika leafnya ada dan new node lebih kecil dari leaf maka anak kiri dari leaf adalah new node.
		Berlaku sebaliknya """
		if lf == None:
			self.root = new_node
		elif new_node < lf:
			lf.left = new_node
		else:
			lf.right = new_node

		""" Kondisi Root
		Jika parentnya kosong, berarti parent adalah root.
		Sesuai rule no.2 Root adalah BLACK """
		if new_node.parent == None:
			new_node.color = BLACK
			return
		
		""" Kondisi Nenek
		Jika nenek kosong, maka bentuk treenya hanya berisi 2/3 data yaitu root dan root.left atau root.right.
		Pastinya root adalah BLACK, dan anaknya adalah RED.
		Bentuk ini tidaklah melanggar rule """
		if new_node.parent.parent == None:
			return

		# Periksa jika ada yang melanggar rule
		self.fix_add(new_node)

	# Add / Bagian pemeriksa apakah ada yang melanggar rule
	def fix_add(self, node):

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


	# Query / Bagian kesepakatan bersama
	def query(self, kata):
		data = []
		if type(kata) == list:
			for i in kata:
				data = self.query_get_file(i, data)
		elif type(kata) == str:
			data = self.query_get_file(kata, data)

		return data

	# Query / Bagian pengatur datanya
	def query_get_file(self, kata, data):
		temp = self.query_helper(self.root, kata)
		if temp != self.NIL:
			data = list(set(data + temp.value))
		return data

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


	""" Transplant / Mengganti node
	x = node yang akan digantikan
	y = node yang menggantikan x """
	def transplant(self, x, y):
		if x.parent == None:
			self.root = y
		elif x == x.parent.left:
			x.parent.left = y
		else:
			x.parent.right = y
		y.parent = x.parent

	""" 
		Kondisi Delete BST
	1. Jika node adalah leaf, langsung delete
	2. Jika punya 1 anak, anaknya menggantikan node
	3. Jika punya 2 anak, cari successor, lalu successor menggantikan node

	node = node yang mau dihapus
	x    = anak
	suc  = successor
	w    = saudara si x
	"""
	# Delete / Bagian kesepakatan bersama
	def delete(self, dokumen_html):
		lane = self.lane.query_helper(self.lane.root, dokumen_html)
		for keyword in lane.value:
			if dokumen_html in keyword.value:
				keyword.value.remove(dokumen_html)
			
			if not keyword.value:
				self.delete_helper(keyword)

		self.lane.delete_helper(lane)
		print("delete complete")

	def delete_helper(self, node):
		# Simpan color node untuk di periksa apakah akan terjadi DOUBLE BLACK atau tidak
		node_color_awal = node.color

		"""
		Kondisi 1
			Jika node adalah leaf, langsung diganti dengan NIL.
		Kondisi 2
			Jika punya 1 anak, anaknya menggantikan node.
		Kondisi 1 bisa diabaikan karena bisa di gantikan oleh Kondisi 2
		Jika node adalah leaf, maka salah satu anaknya (yang merupakan NIL) menggantikan node
		"""
		if node.left == self.NIL:
			x = node.right
			self.transplant(node, x)
		elif node.right == self.NIL:
			x = node.left
			self.transplant(node, x)

		# Kondisi 3
		else:
			"""
			Alasan tidak menggunakan fungsi successor secara langsung,
			karena pada kondisi 3, sudah diketahui bahwa node memiliki 2 anak
			sehingga tidak perlu lagi di periksa pada fungsi successor
			"""
			suc = self.min(node.right)
			# Karena node digantikan oleh successor, jadi color successor disimpan
			node_color_awal = suc.color
			x = suc.right

			"""
			Jika successor bukan anak kanan dari node atau parent successor bukanlah node
			Maka transplant successor dengan x, sehingga successor bebas
			Lalu 
			"""
			if suc.parent == node:
				x.parent = suc
			else:
				self.transplant(suc, x)
				suc.right = node.right
				suc.right.parent = suc
			
			self.transplant(node, suc)
			suc.left = node.left
			suc.left.parent = suc
			suc.color = node.color
		
		if node_color_awal == BLACK:
			self.fix_delete(x)
		
		self.len_data -= 1

	def fix_delete(self, x):
		# Jika terjadi double dan x bukanlah root
		while x != self.root and x.color == BLACK:
			# Saudaranya di sebelah kanan
			if x == x.parent.left:
				w = x.parent.right

				# Kondisi 2
				# Jika warna w adalah RED
				if w.color == RED:
					# Switch Color w dengan parent
					w.color = w.parent.color
					w.parent.color = RED
					# Rotate parent dengan w
					self.rotate_left(w.parent)
					# ganti reference w menjadi saudara x yang baru
					w = x.parent.right

				# disini color w pasti BLACK
				# Kondisi 1
				if w.left.color == BLACK and w.right.color == BLACK:
					# Extra black ke parent, karena parentnya sudah pasti BLACK, jadi tidak perlu di tulis lagi
					w.color = RED
					x = x.parent
				else:
					# Kondisi 3
					if w.right.color == BLACK:
						# Switch color w dengan anak w terdekat dengan x
						w.color = w.left.color
						w.left.color = BLACK
						# Rotasi w ke anak w terjauh dari x
						self.rotate_right(w)
						w = x.parent.right

					# Kondisi 4
					# Switch color w dengan p
					w.color = x.parent.color
					x.parent.color = BLACK
					# Rotasi p ke x
					self.rotate_left(x.parent)
					# Extra black ke j
					w.right.color = BLACK
					""" Biasanya setelah kondisi 4, sudah tidak ada double black, jadi kita hentikan perulangan dengan cara x adalah root.
					Ini juga disebut sebagai Kondisi 0 """
					x = self.root
			# Saudaranya disebelah kiri
			else:
				w = x.parent.left

				if w.color == RED:
					w.color = w.parent.color
					w.parent.color = RED
					self.rotate_right(w.parent)
					w = x.parent.left

				if w.left.color == BLACK and w.right.color == BLACK:
					w.color = RED
					x = x.parent
				else:
					if w.left.color == BLACK:
						w.color = w.right.color
						w.right.color = BLACK
						self.rotate_left(w)
						w = x.parent.left

					w.color = x.parent.color
					x.parent.color = BLACK
					self.rotate_right(x.parent)
					w.left.color = BLACK
					x = self.root
		x.color = BLACK

class RBT_Lane(RedBlackTree):
	def __init__(self):
		super().__init__()

	def add_helper(self, new_node):
		lf   = None
		node = self.root
		
		while node != self.NIL:
			lf = node
			if new_node.key == node.key:
				node + new_node
				new_node = None
				return
			elif new_node < node:
				node = node.left
			else:
				node = node.right
		
		new_node.parent = lf
		self.len_data += 1

		if lf == None:
			self.root = new_node
		elif new_node < lf:
			lf.left = new_node
		else:
			lf.right = new_node

		if new_node.parent == None:
			node.color = BLACK
			return
		
		if new_node.parent.parent == None:
			return

		self.fix_add(new_node)

	def check_lane(self):
		self.lane = 1

