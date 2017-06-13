import re

# c_financial_o_list = ['Oppenheimer', 'Luca Maestri']
# cfo = re.compile(r'\b(?:%s)\b' % '|'.join(c_financial_o_list))

# print(re.match('Oppenheimer', cfo))

fruit_list = ['^(Peter)? ?Oppenheimer', 'banana', 'peach', 'plum', 'pineapple', 'kiwi']
fruit = re.compile(r'\b(?:%s)\b' % '|'.join(fruit_list))
print(fruit.search('apple'))
print(fruit.search('Peter Oppenheimer - ceo'))
print(fruit.search('Oppenheimer'))
