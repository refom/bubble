
class Node(object):
	def __init__(self, key, lokasi):
		self.data = lokasi
		self.key = key
		self.left = None
		self.right = None

def insert(root, key):
	if root is None:
		return Node(key)
	else:
		if root.key == key:
			return root
		elif root.key < key:
			root.right = insert(root.right, key)
		else:
			root.left = insert(root.left, key)
	return root

def inorder(root):
	if root:
		inorder(root.left)
		print(root.key)
		inorder(root.right)

r = Node("a")
yee = ["2", "!", "z", "e", "f", "g"]

for i in yee:
	r = insert(r, i)

inorder(r)



