
import re, pickle
from bs4 import BeautifulSoup
from strukturdata import AVL_Tree

def naah():
	with open("Artificial Intelligence Mengubah Cara Kerja Dunia -.html", "r", encoding="utf8") as f:
		soup = BeautifulSoup(f.read(), "html.parser")
		x = soup.get_text()

	x = set(x.lower().split())

	r = None
	keyword = AVL_Tree()
	path = "./data.html"

	for key in x:
		r = keyword.insert(r, key, path)

	with open("key.dll", "wb") as kf:
		pickle.dump(r, kf)

def tampil():
	with open("key.dll", "rb") as kf:
		r = pickle.load(kf)
	keyword = AVL_Tree()
	keyword.inOrder(r, "ROOT")



naah()
tampil()

