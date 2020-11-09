
class Node(object):
	def __init__(self, key):
		self.key    = key
		self.loc    = []
		self.left   = None
		self.right  = None
		self.height = 1

	def inputLoc(self, lokasi):
		if not lokasi in self.loc:
			self.loc.append(lokasi)


class AVL_Tree(object):
	def __init__(self):
		self.root = None

	# Query
	def search_helper(self, root, key):
		if root is None or root.key == key:
			return root

		if key < root.key:
			return self.search_helper(root.left, key)
		return self.search_helper(root.right, key)

	# Query
	def query(self, key):
		return self.search_helper(self.root, key)

	# Add / Insert
	def insert_helper(self, root, key, loc):
		# Kalau root gk ada, buat Node baru
		if root == None:
			new_node = Node(key)
			new_node.inputLoc(loc)
			return new_node
		elif root.key == key:
			root.inputLoc(loc)
			return root
		elif key < root.key:
			root.left = self.insert_helper(root.left, key, loc)
		else:
			root.right = self.insert_helper(root.right, key, loc)

		# Update height
		root.height = 1 + max(self.getHeight(root.left),
						self.getHeight(root.right))

		# Get balance
		balance = self.getBalance(root)

		# Kalau gak balance
		# Case 1 - Left Left
		if balance > 1 and key < root.left.key:
			return self.rightRotate(root)

		# Case 2 - Right Right
		if balance < -1 and key > root.right.key:
			return self.leftRotate(root)

		# Case 3 - Left Right
		if balance > 1 and key > root.left.key:
			root.left = self.leftRotate(root.left)
			return self.rightRotate(root)

		# Case 4 - Right Left
		if balance < -1 and key < root.right.key:
			root.right = self.rightRotate(root.right)
			return self.leftRotate(root)

		return root

	# Insert / Add
	def insert(self, key, loc):
		self.root = self.insert_helper(self.root, key, loc)
		if not self.root:
			return "Insert / Add False"

	def leftRotate(self, z):
		y  = z.right
		T2 = y.left

		# Perform rotation 
		y.left  = z
		z.right = T2

		# Update heights
		z.height = 1 + max(self.getHeight(z.left),
						self.getHeight(z.right))
		y.height = 1 + max(self.getHeight(y.left),
						self.getHeight(y.right))

		# Return the new root
		return y

	def rightRotate(self, z):
		y  = z.left
		T3 = y.right

		# Perform rotation
		y.right = z
		z.left  = T3

		# Update heights
		z.height = 1 + max(self.getHeight(z.left),
						self.getHeight(z.right))
		y.height = 1 + max(self.getHeight(y.left),
						self.getHeight(y.right))

		# Return the new root
		return y

	def getHeight(self, root):
		if not root:
			return 0

		return root.height

	def getBalance(self, root):
		if not root:
			return 0

		return self.getHeight(root.left) - self.getHeight(root.right)

	def preOrder(self, root, teks):
		if not root:
			return

		print(f"{teks} = {root.key},", end=" ")
		self.inOrder(root.left, "LEFT")
		self.inOrder(root.right, "RIGHT")

	def get_preOrder_helper(self, root, teks, keylist):
		if not root:
			return keylist

		keylist.append(f"{teks} = {root.key}, ")
		self.get_preOrder_helper(root.left, "LEFT", keylist)
		self.get_preOrder_helper(root.right, "RIGHT", keylist)
		return keylist

	def get_preOrder(self):
		keylist = []
		return self.get_preOrder_helper(self.root, "ROOT", keylist)




