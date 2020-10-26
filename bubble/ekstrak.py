import os
from bs4 import BeautifulSoup
from bubble import app


# Buat file path.dll => tambahkan filename ke 
def insertFile(filename):
	path = os.path.join(app.config['KEYPATH_FOLDER'], "path.dll")
	with open(path, "a") as f:
		f.write(filename)
	with open(path, "r") as f:
		index = f.readlines()
		index = len(index)-1
	return index

class Node(object):
	def __init__(self, key, loc):
		self.lokasi = loc
		self.key    = key
		self.left   = None
		self.right  = None

def insert(root, key, loc):
	if root is None:
		return Node(key, loc)
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

def listToString(x):
	str = " "
	return (str.join(x))

def stringToList(x):
	return list(x.split(" "))


	def setKeyword(filename, loc):
		# Filenya
		path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

		# Parser isinya
		with open(path, "r") as f:
			soup      = BeautifulSoup(f.read(), 'html.parser')
			list_teks = soup.find_all(["p", "title"])

		# Pembuatan keyword
		str_key   = listToString(list_teks)
		str_key   = str_key.lower()
		list_key  = stringToList(str_key)
		r         = None
		for key in list_key:
			insert(r, key, loc)




# Filename => String Keyword => lowercase => string to list => ubah ke set => masukkan ke BST
# => save BST

	
	







