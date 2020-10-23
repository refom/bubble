from bs4 import BeautifulSoup

nah = "data html/4 Library Python Terbaik untuk Machine Learning - Teknologi.id.html"

with open(nah, "r") as f:
	soup = BeautifulSoup(f.read(), 'html.parser')
	teks = soup.find_all(["p", "title"])
	



	with open("keyword.txt", "w") as k:
		kw = []
		for isi in teks:
			if isi.string != None:
				kw = kw + isi.text.split()
		print(*kw)
		# k.write(print(*kw))





