import sys

BLACK = 0
RED = 1

class Node(object):
	def __init__(self, key):
		self.key    = key
		self.loc    = []
		self.parent = None
		self.left   = None
		self.right  = None
		self.color  = RED

	def inputLoc(self, lokasi):
		if not lokasi in self.loc:
			self.loc.append(lokasi)

	def get_color(self):
		if self.color:
			return "RED"
		else:
			return "BLACK"


class RedBlackTree(object):
	def __init__(self):
		self.TNULL = Node("")
		self.TNULL.color =  BLACK
		self.root = self.TNULL

	# Balance the tree after insertion
	def __fix_insert(self, k):
		while k.parent.color == RED:
			if k.parent == k.parent.parent.right:
				u = k.parent.parent.left
				if u.color == RED:
					u.color = BLACK
					k.parent.color = BLACK
					k = k.parent.parent
					k.color = RED
				else:
					if k == k.parent.left:
						k = k.parent
						self.right_rotate(k)
					k.parent.color = BLACK
					k.parent.parent.color = RED
					self.left_rotate(k.parent.parent)
			else:
				u = k.parent.parent.right

				if u.color == RED:
					u.color = BLACK
					k.parent.color = BLACK
					k.parent.parent.color = RED
					k = k.parent.parent
				else:
					if k == k.parent.right:
						k = k.parent
						self.left_rotate(k)
					k.parent.color = BLACK
					k.parent.parent.color = RED
					self.right_rotate(k.parent.parent)
			if k == self.root:
				break
		self.root.color = BLACK

	# Insert / Add
	def insert(self, key, loc):
		# BST
		parent = None
		root = self.root

		while root != self.TNULL:
			parent = root
			try:
				if key == root.key:
					root.inputLoc(loc)
					# Return True jika berhasil
					return "insert = TRUE"
				elif key < root.key:
					root = root.left
				else:
					root = root.right
			except:
				# Return False jika gagal
				return "insert = FALSE"

		node = Node(key)
		node.inputLoc(loc)
		node.left = self.TNULL
		node.right = self.TNULL
		node.parent = parent

		if parent == None:
			self.root = node
		elif node.key < parent.key:
			parent.left = node
		else:
			parent.right = node

		# if new node is a root node, simply return
		if node.parent == None:
			node.color = BLACK
			return

		# if the grandparent is None, simply return
		if node.parent.parent == None:
			return

		# Fix the tree
		self.__fix_insert(node)

		# Return True jika berhasil
		return "insert = TRUE"

	# Search the tree
	def __search_helper(self, node, key):
		if node == self.TNULL or key == node.key:
			# Mengembalikan node yg berisi lokasi dan nama key
			return node

		if key < node.key:
			return self.__search_helper(node.left, key)
		return self.__search_helper(node.right, key)

	# Query / Search
	def query(self, k):
		return self.__search_helper(self.root, k)

	# Delete
	def delete(self, key):
		self.delete_helper(self.root, key)

	def delete_helper(self, node, key):
		z = self.TNULL
		while node != self.TNULL:
			if node.key == key:
				z = node

			if node.key <= key:
				node = node.right
			else:
				node = node.left

		if z == self.TNULL:
			print("Cannot find key in the tree")
			return

		y = z
		y_original_color = y.color
		if z.left == self.TNULL:
			x = z.right
			self.__rb_transplant(z, z.right)
		elif (z.right == self.TNULL):
			x = z.left
			self.__rb_transplant(z, z.left)
		else:
			y = self.minimum(z.right)
			y_original_color = y.color
			x = y.right
			if y.parent == z:
				x.parent = y
			else:
				self.__rb_transplant(y, y.right)
				y.right = z.right
				y.right.parent = y

			self.__rb_transplant(z, y)
			y.left = z.left
			y.left.parent = y
			y.color = z.color
		if y_original_color == BLACK:
			self.delete_fix(x)

	def delete_fix(self, x):
		while x != self.root and x.color == BLACK:
			if x == x.parent.left:
				s = x.parent.right
				if s.color == RED:
					s.color = BLACK
					x.parent.color = RED
					self.left_rotate(x.parent)
					s = x.parent.right

				if s.left.color == BLACK and s.right.color == BLACK:
					s.color = RED
					x = x.parent
				else:
					if s.right.color == BLACK:
						s.left.color = BLACK
						s.color = RED
						self.right_rotate(s)
						s = x.parent.right

					s.color = x.parent.color
					x.parent.color = BLACK
					s.right.color = BLACK
					self.left_rotate(x.parent)
					x = self.root
			else:
				s = x.parent.left
				if s.color == RED:
					s.color = BLACK
					x.parent.color = RED
					self.right_rotate(x.parent)
					s = x.parent.left

				if s.right.color == BLACK and s.right.color == BLACK:
					s.color = RED
					x = x.parent
				else:
					if s.left.color == BLACK:
						s.right.color = BLACK
						s.color = RED
						self.left_rotate(s)
						s = x.parent.left

					s.color = x.parent.color
					x.parent.color = BLACK
					s.left.color = BLACK
					self.right_rotate(x.parent)
					x = self.root
		x.color = BLACK

	def __rb_transplant(self, u, v):
		if u.parent == None:
			self.root = v
		elif u == u.parent.left:
			u.parent.left = v
		else:
			u.parent.right = v
		v.parent = u.parent

	def left_rotate(self, x):
		y = x.right
		x.right = y.left
		if y.left != self.TNULL:
			y.left.parent = x

		y.parent = x.parent
		if x.parent == None:
			self.root = y
		elif x == x.parent.left:
			x.parent.left = y
		else:
			x.parent.right = y
		y.left = x
		x.parent = y

	def right_rotate(self, x):
		y = x.left
		x.left = y.right
		if y.right != None:
			y.right.parent = x

		y.parent = x.parent
		if x.parent == None:
			self.root = y
		elif x == x.parent.right:
			x.parent.right = y
		else:
			x.parent.left = y
		y.right = x
		x.parent = y

	def get_root(self):
		return self.root

	def minimum(self, node):
		while node.left != self.TNULL:
			node = node.left
		return node

	def maximum(self, node):
		while node.right != self.TNULL:
			node = node.right
		return node

	# Printing the tree
	def __print_helper(self, node, indent, last):
		if node != self.TNULL:
			sys.stdout.write(indent)
			if last:
				sys.stdout.write("R----")
				indent += "     "
			else:
				sys.stdout.write("L----")
				indent += "|    "

			print(str(node.key) + "(" + node.get_color() + ")")
			self.__print_helper(node.left, indent, False)
			self.__print_helper(node.right, indent, True)

	def print_tree(self):
		self.__print_helper(self.root, "", True)

	def get_preOrder_helper(self, node, teks, keylist):
		if node == self.TNULL:
			return keylist

		keylist.append(f"{teks} = {node.key}, ")
		self.get_preOrder_helper(node.left, "LEFT", keylist)
		self.get_preOrder_helper(node.right, "RIGHT", keylist)
		return keylist

	def get_preOrder(self, keylist):
		return self.get_preOrder_helper(self.root, "ROOT", keylist)







