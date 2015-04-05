
def count_letters(mystr):
	mystr = mystr.lower()
	return { letter : mystr.count(letter) for letter in set(mystr) }
