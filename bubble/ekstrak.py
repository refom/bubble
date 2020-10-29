import os
from bs4 import BeautifulSoup
from bubble import app

class Node(object):
	def __init__(self, key, lokasi):
		self.data  = [lokasi]
		self.key   = key
		self.left  = None
		self.right = None

def search(root, key):
	pass

def insert(root, key, lokasi):
	if root is None:
		return Node(key, lokasi)
	else:
		if root.key == key:
			root.data.append(lokasi)
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

def setKeyword(path):
	# Parser isinya
	with open(path, "r") as f:
		soup      = BeautifulSoup(f.read(), 'html.parser')
		x = soup.find_all(["p", "title"])

	# Pembuatan keyword
	x = listToString(x)
	x = set(stringToList(x.lower()))
	r = None
	for key in x:
		insert(r, key, path)




	
	







