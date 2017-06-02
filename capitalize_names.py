import nltk

with open('names.txt', 'r') as read_file:
    txt = read_file.read()

name_list = []

tokens = nltk.word_tokenize(txt)
print("tokens: ", tokens)

for token in tokens:
    name = token.lower().title()
    print(name)
    name_list.append(name)

with open('names_capitalized.txt', 'w') as write_file:
    for name in name_list:
        write_file.write("%s\n" % name)