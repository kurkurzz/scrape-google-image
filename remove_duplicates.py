text_file = open('malay-words-with-duplicates.txt', 'r')
lines = text_file.readlines()

lines = list(dict.fromkeys(lines))

with open('malay-words.txt', 'a') as file:
	for item in lines:
		file.write(str(item))