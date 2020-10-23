

class Node: 
	def __init__(self,key): 
		self.left = None
		self.right = None
		self.val = key 


def insert(root,key): 
	if root is None: 
		return Node(key) 
	else: 
		if root.val == key: 
			return root 
		elif root.val < key: 
			root.right = insert(root.right, key) 
		else: 
			root.left = insert(root.left, key) 
	return root 


def inorder(root): 
	if root: 
		inorder(root.left) 
		print(root.val) 
		inorder(root.right) 


# Driver program to test the above functions 
# Let us create the following BST 
# 50 
# /	 \ 
# 30	 70 
# / \ / \ 
# 20 40 60 80 

r = Node("aa") 
r = insert(r, "bb") 
r = insert(r, "cc") 
r = insert(r, "dd") 
r = insert(r, "70") 
r = insert(r, "ab") 
r = insert(r, "bc") 

# Print inoder traversal of the BST 
inorder(r) 
