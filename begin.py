import nltk
from nltk import Text
from textract import process
import io
import re
import glob

files = glob.glob('Test/Amazon11.pdf')
file_count = 0
for file in files:
    text = process(file).decode()
    txt = io.StringIO(text)
    lines = txt.readlines()
    copyright_index = [index for index, item in enumerate(lines) if re.search('1 ? ? ?- ? 8 ?7 ?7 ?', item)]
    print("copyright_index", copyright_index)
    copyright_slice_list = list()
    for x in range(0, len(copyright_index)):
        copyright_index = copyright_index
        mininum_value = copyright_index[x] - 2
        maximum_value = copyright_index[x] + 14
        copyright_slice = lines[mininum_value: maximum_value]
        copyright_slice_list.append(copyright_slice)
        print("copyright_slice", copyright_slice)
    print("COPYRIGHT_SLICE_LIST", copyright_slice_list)
    for x in range(0, len(copyright_slice_list)):
        lines = [item for item in lines if item not in copyright_slice_list[x]]
    print("lines without copyright", lines)
    question_and_answer_index = [index for index, item in enumerate(lines) if re.search('Q(UESTION)? ?(AND)?&? ?A(NSWER SECTION\\n)?', item)]
    disclaimer_index = [index for index, item in enumerate(lines) if re.search('Disclaimer', item)]
    print("disclaimer", disclaimer_index)
    lines = lines[question_and_answer_index[0]:disclaimer_index[0]]
    question_indices = [index for index, question in enumerate(lines) if re.search('((<Q)|(^Q\\n))|(Question[:-])', question)]
    answer_indices = [index for index, answer in enumerate(lines) if re.search('((<A)|(A\\n))|(Answer[:-])', answer)]
    question_answer_indices = question_indices + answer_indices
    question_answer_indices.sort(key=int)
    for index, value in enumerate(question_answer_indices):
        print('\n\n')
        print('************************')
        try:
            output = lines[(question_answer_indices[index]):question_answer_indices[index+1]]
            # print(lines[(question_answer_indices[index]):question_answer_indices[index+1]])
        except IndexError:
            # print(lines[(question_answer_indices[index]):])
            output = (lines[question_answer_indices[index]:])
            file_count += 1
            print('#######################################################')
            print('NEXT FILE')
            print('#######################################################')
            pass
        with open("test.txt", 'a+') as write_file:
            write_file.write(' '.join(output))
print("file_count: ", file_count)
print("question_answer_indices length: ", len(question_answer_indices))

