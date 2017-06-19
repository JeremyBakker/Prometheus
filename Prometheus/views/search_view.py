from collections import Counter
from django.shortcuts import render
from django.apps import apps
from nltk import word_tokenize
from nltk.util import ngrams
from statistics import median
import datetime
import re

def search (request):
    '''
    This function renders the natural language data for the corporate 
    transcript selected by the user.

    ---Arguments---
    request: the full HTTP request object

    ---Return Value---
    request: the full HTTP request object
    template: index.html
    context: 
    '''

    # These regex patterns lists contain the possible renderings of the names
    # of CEOs and CFOs of the corporations whose transcripts we analyze. The
    # transcripts lack this data in any reliable pattern to pull when parsing. 
    # Thus, a hard-coded list is necessary for now. Each row correlates to a
    # company: Apple, Adobe, Amazon, HP, IBM, Microsoft, Oracle, and Samsung.
    # Within this data set, there are three instances of a single name 
    # appearing in two different roles over time. Tim Cook served as an EVP and
    # COO at Apple before becoming CEO in 2011. I include him in the CEO list
    # because Steve Jobs rarely, if ever, spoke on earnings calls. Tim Cook 
    # filled that role in practice even before he became CEO. Catherine Lesjak
    # briefly served as interim CEO of HP while maintaining her position as 
    # CFO. I leave her exclusively in the CFO category since she never
    # abandoned that role. Safra Catz has served as President and CFO, the 
    # the latter role multiple times. I leave her in the CFO category because
    # Larry Ellison has been CEO during Catz's entire tenure. Samsung is a bit
    # of an anomaly in this list. The corporation often had an executive vice
    # president and several senior vice presidents of product lines on the 
    # call. I categorized the EVP as CEO and the SVP as CFOs. Interpreters will
    # need to consider this when comparing Samsung to other companies.
    c_exec_o_list = [
    '^(Steve)? ?Jobs', '^(Tim)?(othy)? ?Cook', 
    '^(Bruce)? ?Chizen', '^(Shantanu)? ?Narayen',
    '^(Jeff)?(rey)? ?P?.? ?Bezos',
    '^(Mark)? ?(V\.)?Hurd', '^(L.o)? ?Apotheker',
    '^(Sam)(uel)? ?(J\.)? ?Palmisano',
    '^(Bill)? ?Gates',
    '^(Lawrence)?(Larry)? ?(J\.)? ?Ellison',
    '^(Dr.)? ?(Woo)? ?[Ss]+?(ik)? ?Chu'
    ]
    c_financ_o_list = [
    '^(Peter)? ?Oppenheimer', '^(Luca)? ?Maestri',
    '^(Murray)? ?Demo', '^(Mark)? ?Garrett',
    '^Th?(om)?(as)? (J\.)? ?Szkutak',
    '^(Bob)? ?Wayman', '^(Cath)?(erine)?(ie)? ?Lesjak',
    '^(Mark)? ?Loughridge',
    '^(Chris)?(topher)? ?(P\.)? ?Liddell', '^(Pete)(r)? ?Klein',
    '^(Greg)?(ory)? ?(B\.)? ?Maffei', '^(Safra)? ?(A\.)? ?Catz?', 
        '^(Jeff)?(rey)? ?Epstein', 
    '^(Dr.)? ?(Yeong) ?[Dd]+?(uk)? ?Cho', '^(Dr.)? ?(David)? ?Steel', 
        '(Il)? ?(Ung)? ?Kim', '^(Yeongho)? ?Kang', '^(Sangheung)? ?Shin',
        '^(Namseong)? ?Cho?', '^(Hyungdo)? ?Kim', '^(Hwan)? ?Kim', 
        '^(Yangkyu)? Kim?', '^(Myung)(kun)?(ho)? ?Kim', '^(Jungryul)? ?Lee', 
        '^(You?ng-?[Hh]ee)? ?Lee', '^(Bongku)? ?Kang', '(Wanhoon)? ?Hong',
        '^(Dr.)? (Youngcho)? ?Chi', '(Jaeyong)? ?Lee'
    ]
    c_exec_o_list_regex = re.compile(r'\b(?:%s)\b' % '|'.join(
        c_exec_o_list))
    c_financ_o_list_regex = re.compile(r'\b(?:%s)\b' % '|'.join(
        c_financ_o_list))
    
    # Here we pull the transcript name from the select box to get the 
    # relevant data we will use to render the page.
    transcript = request.GET['transcript']
    corporation = transcript.split('-')[0]
    transcript_date = transcript.split('-')[1]

    # Transform the date both for the SQL query and for display on the 
    # page.
    transcript_date = datetime.datetime.strptime(
        (transcript_date), "%d %B %y")
    transcript_date_for_db = datetime.datetime.strftime(
        (transcript_date), "%Y-%m-%d")
    transcript_date_for_display = datetime.datetime.strftime(
        (transcript_date), "%B %d, %Y")

    # Pull the appropriate corporation model according to the string passed 
    # from the transcript select box on index.html.
    model = apps.get_model('Prometheus', corporation)

    # Query the Database
    answers_query_set = model.objects.filter(
        date_of_call = transcript_date_for_db, question=0).order_by("name")
    
    c_exec_o_answer_list = list()
    c_financ_o_answer_list = list()
    c_exec_o_answer_length_list = list()
    c_financ_o_answer_length_list = list()
    number_of_shared_words = 0
    c_exec_o_negative_words = 0
    c_financ_o_negative_words = 0
    c_exec_o_positive_words = 0
    c_financ_o_positive_words = 0
    c_exec_o_bigram_refs_to_general_knowledge = 0
    c_exec_o_trigram_refs_to_general_knowledge = 0
    c_financ_o_bigram_refs_to_general_knowledge = 0
    c_financ_o_trigram_refs_to_general_knowledge = 0
    c_exec_o_bigram_refs_to_shareholders_value = 0
    c_exec_o_trigram_refs_to_shareholders_value = 0
    c_financ_o_bigram_refs_to_shareholders_value = 0
    c_financ_o_trigram_refs_to_shareholders_value = 0
    c_exec_o_bigram_refs_to_value_creation = 0
    c_financ_o_bigram_refs_to_value_creation = 0

    # For each answer, we determine whether it correlates to the CEO or 
    # CFO. Then, after tokenizing the text, removing punctuation, and 
    # capitalizing each word, we split the text into bigrams and trigrams 
    # for searching by phrase. From there, we compare n-grams (1, 2, or 3)
    # to relevant lectionaries stored as .txt files to determine text
    # characteristics (positive_words, general_knowledge, etc.). We then 
    # calculate the appropriate proportional number and pass the data to
    # the context for rendering.
    for answer in answers_query_set:
        if c_exec_o_list_regex.search(answer.name):
            
            # CEO Answers
            c_exec_o_filtered_answer = clean_text(
                answer.question_answer_text)
            c_exec_o_answer_list.append(
                c_exec_o_filtered_answer)
            c_exec_o_answer_length_list.append(len(
                c_exec_o_filtered_answer))    
            
            # CEO Bigrams
            c_exec_o_bigrams = list(ngrams(
                c_exec_o_filtered_answer, 2))
            c_exec_o_bigrams_strings = ["%s %s" % bigram for 
                bigram in c_exec_o_bigrams]
            
            # CEO Trigrams
            c_exec_o_trigrams = list(ngrams(
                c_exec_o_filtered_answer, 3))
            c_exec_o_trigrams_strings = ["%s %s %s" % trigram for 
                trigram in c_exec_o_trigrams]

            with open('Prometheus/static/lexicons/negative_words.txt', 
                'r') as file:
                lines = [line.strip() for line in file.readlines()]
                if set(c_exec_o_filtered_answer).intersection(lines):
                    negative_intersection_length = \
                        find_number_of_shared_words(
                        c_exec_o_filtered_answer, lines, 
                        number_of_shared_words)
                    c_exec_o_negative_words += \
                        negative_intersection_length

            with open('Prometheus/static/lexicons/positive_words.txt', 
                'r') as file:
                lines = [line.strip() for line in file.readlines()]
                if set(c_exec_o_filtered_answer).intersection(lines):
                    positive_intersection_length = \
                        find_number_of_shared_words(
                        c_exec_o_filtered_answer, lines, 
                        number_of_shared_words)
                    c_exec_o_positive_words += \
                        positive_intersection_length

            with open('Prometheus/static/lexicons/general_knowledge.txt', 
                'r') as file:
                lines = [line.strip().upper() for line in file.readlines()]
                if set(c_exec_o_bigrams_strings).intersection(lines):
                    c_exec_o_bigram_refs_to_general_knowledge += 1
                if set(c_exec_o_trigrams_strings).intersection(
                    lines):
                    c_exec_o_trigram_refs_to_general_knowledge += 1

            with open('Prometheus/static/lexicons/shareholders_value.txt', 
                'r') as file:
                lines = [line.strip().upper() for line in file.readlines()]
                if set(c_exec_o_bigrams_strings).intersection(
                    lines):
                    c_exec_o_bigram_refs_to_shareholders_value += 1
                if set(c_exec_o_trigrams_strings).intersection(
                    lines):
                    c_exec_o_trigram_refs_to_shareholders_value += 1

            with open('Prometheus/static/lexicons/value_creation.txt', 
                'r') as file:
                lines = [line.strip().upper() for line in 
                    file.readlines()]
                if set(c_exec_o_bigrams_strings).intersection(lines):
                    c_exec_o_bigram_refs_to_value_creation += 1

        if c_financ_o_list_regex.search(answer.name):

            # CFO Answers            
            c_financ_o_filtered_answer = clean_text(
                answer.question_answer_text)
            c_financ_o_answer_list.append(
                c_financ_o_filtered_answer)
            c_financ_o_answer_length_list.append(
                len(c_financ_o_filtered_answer))

            # CFO Bigrams
            c_financ_o_bigrams = list(ngrams(
                c_financ_o_filtered_answer, 2))
            c_financ_o_bigrams_strings = ["%s %s" % bigram for 
                bigram in c_financ_o_bigrams]
            
            # CFO Trigrams
            c_financ_o_trigrams = list(ngrams(
                c_financ_o_filtered_answer, 3))
            c_financ_o_trigrams_strings = ["%s %s %s" % trigram for 
                trigram in c_financ_o_trigrams]

            with open('Prometheus/static/lexicons/negative_words.txt', 
                'r') as file:
                lines = [line.strip() for line in file.readlines()]
                if set(c_financ_o_filtered_answer).intersection(lines):
                    negative_intersection_length = \
                        find_number_of_shared_words(
                        c_financ_o_filtered_answer, lines, 
                        number_of_shared_words)
                    c_financ_o_negative_words += \
                        negative_intersection_length

            with open('Prometheus/static/lexicons/positive_words.txt', 
                'r') as file:
                lines = [line.strip() for line in file.readlines()]
                if set(c_financ_o_filtered_answer).intersection(lines):
                    positive_intersection_length = \
                        find_number_of_shared_words(
                        c_financ_o_filtered_answer, lines, 
                        number_of_shared_words)
                    c_financ_o_positive_words += \
                        positive_intersection_length

            with open('Prometheus/static/lexicons/general_knowledge.txt', 
                'r') as file:
                lines = [line.strip().upper() for line in file.readlines()]
                if set(c_financ_o_bigrams_strings).intersection(lines):
                    c_financ_o_bigram_refs_to_general_knowledge += 1
                if set(c_financ_o_trigrams_strings).intersection(lines):
                    c_financ_o_trigram_refs_to_general_knowledge += 1

            with open('Prometheus/static/lexicons/shareholders_value.txt', 
                'r') as file:
                lines = [line.strip().upper() for line in file.readlines()]
                if set(c_financ_o_bigrams_strings).intersection(lines):
                    c_financ_o_bigram_refs_to_shareholders_value += 1
                if set(c_financ_o_trigrams_strings).intersection(lines):
                    c_financ_o_trigram_refs_to_shareholders_value += 1

            with open('Prometheus/static/lexicons/value_creation.txt', 
                'r') as file:
                lines = [line.strip().upper() for line in file.readlines()]
                if set(c_financ_o_bigrams_strings).intersection(lines): 
                    c_financ_o_bigram_refs_to_value_creation += 1

    c_exec_o_answer_length_sum = sum(c_exec_o_answer_length_list)
    c_financ_o_answer_length_sum = sum(c_financ_o_answer_length_list)

    # In the following try/except blocks, I only account for the absence of the 
    # CEO from the transcript. I want to be alerted to the absence of the CFO.
    # I know of transcripts that lack the CEO speaking. I have not found an 
    # instance in which a CFO does not speak on an earnings call. In fact, I 
    # cannot think of a logical reason for such an absence. The most 
    # reasonable explanation of an error raising due to the lack of data from 
    # a CFO here is that I have not properly formatted the opening regex above
    # to account for the different spellings of CFOs names (Tom vs. Thomas, for
    # instance). Thus, I would like the program to throw an error so I can 
    # adjust the preceding code as needed.
    
    # Median
    try:
        c_exec_o_answer_length_median = median(
            c_exec_o_answer_length_list)
    except ValueError:
        c_exec_o_answer_length_median = 0
    c_financ_o_answer_length_median = median(c_financ_o_answer_length_list) 
    
    # Negative Words
    try:
        c_exec_o_negative_proportion = c_exec_o_negative_words / \
            c_exec_o_answer_length_sum
    except ZeroDivisionError:
        c_exec_o_negative_proportion = 0
    c_financ_o_negative_proportion = c_financ_o_negative_words / \
        c_financ_o_answer_length_sum  

    # Positive Words
    try:    
        c_exec_o_positive_proportion = c_exec_o_positive_words / \
            c_exec_o_answer_length_sum
    except ZeroDivisionError:
        c_exec_o_positive_proportion = 0
    c_financ_o_positive_proportion = c_financ_o_positive_words / \
        c_financ_o_answer_length_sum
    
    # General Knowledge
    try:
        c_exec_o_proportion_refs_to_general_knowledge = \
            (c_exec_o_bigram_refs_to_general_knowledge + 
            c_exec_o_trigram_refs_to_general_knowledge) / \
            len(c_exec_o_answer_list)
    except ZeroDivisionError:
        c_exec_o_proportion_refs_to_general_knowledge = 0
    c_financ_o_proportion_refs_to_general_knowledge = \
        (c_financ_o_bigram_refs_to_general_knowledge + 
        c_financ_o_trigram_refs_to_general_knowledge) / \
        len(c_financ_o_answer_list)
    
    # Shareholders Value
    try:
        c_exec_o_proportion_refs_to_shareholders_value = \
            (c_exec_o_bigram_refs_to_shareholders_value + 
            c_exec_o_trigram_refs_to_shareholders_value) / \
            len(c_exec_o_answer_list)
    except ZeroDivisionError:
        c_exec_o_proportion_refs_to_shareholders_value = 0
    c_financ_o_proportion_refs_to_shareholders_value = \
        (c_financ_o_bigram_refs_to_shareholders_value + 
        c_financ_o_trigram_refs_to_shareholders_value) / \
        len(c_financ_o_answer_list)
    
    # Value Creation
    try:
        c_exec_o_proportion_refs_to_value_creation = \
            c_exec_o_bigram_refs_to_value_creation / \
            len(c_exec_o_answer_list)
    except ZeroDivisionError:
        c_exec_o_proportion_refs_to_value_creation = 0
    c_financ_o_proportion_refs_to_value_creation = \
        c_financ_o_bigram_refs_to_value_creation / \
        len(c_financ_o_answer_list)

    # First Person Singular Pronoun
    c_exec_o_number_of_i_instances = 0
    c_financ_o_number_of_i_instances = 0
    i = re.compile('I ')
    for answer in c_exec_o_answer_list:
        string_answer = (' ').join(answer)
        if i.search(string_answer):
            c_exec_o_number_of_i_instances += len([m.start() for m in 
                re.finditer(i, string_answer)])
    try:
        proportion_c_exec_o_number_of_i_instances = \
            round(c_exec_o_number_of_i_instances/c_exec_o_answer_length_sum, 4)
    except ZeroDivisionError:
        proportion_c_exec_o_number_of_i_instances = 0
    for answer in c_financ_o_answer_list:
        string_answer = (' ').join(answer)
        if i.search(string_answer):
            c_financ_o_number_of_i_instances += len([m.start() for m in 
                re.finditer(i, string_answer)])
        proportion_c_financ_o_number_of_i_instances = \
            round(c_financ_o_number_of_i_instances/
                c_financ_o_answer_length_sum, 4)


    template = 'index.html'
    context = {
        "search_view": True, 
        "corporation": corporation, 
        "date": transcript_date_for_display, 
        "cFo_median": c_financ_o_answer_length_median, 
        "cFo_sum": c_financ_o_answer_length_sum,
        "cEo_median": c_exec_o_answer_length_median,
        "cEo_sum": c_exec_o_answer_length_sum,
        "cEo_negative": round(c_exec_o_negative_proportion, 4),
        "cFo_negative": round(c_financ_o_negative_proportion, 4),
        "cEo_positive": round(c_exec_o_positive_proportion, 4),
        "cFo_positive": round(c_financ_o_positive_proportion, 4),
        "cEo_knowledge": round(
            c_exec_o_proportion_refs_to_general_knowledge, 4),
        "cFo_knowledge": round(
            c_financ_o_proportion_refs_to_general_knowledge, 4),
        "cEo_shareholders_value": round(
            c_exec_o_proportion_refs_to_shareholders_value, 4),
        "cFo_shareholders_value": round(
            c_financ_o_proportion_refs_to_shareholders_value, 4),
        "cEo_value_creation": round(
            c_exec_o_proportion_refs_to_value_creation, 4),
        "cFo_value_creation": round(
            c_financ_o_proportion_refs_to_value_creation, 4),
        "cEo_I": proportion_c_exec_o_number_of_i_instances,
        "cFo_I": proportion_c_financ_o_number_of_i_instances
        }

    return render(request, template, context)

def clean_text(question_answer_text):
    tokenized_answer = word_tokenize(question_answer_text)
    without_punctuation = re.compile('.*[A-Za-z0-9].*')
    filtered_answer = [word.upper() for word in tokenized_answer if 
        without_punctuation.match(word)]
    return filtered_answer

def find_number_of_shared_words(filtered_answer, lines, 
    number_of_shared_words):
    shared_words = list()
    for word in filtered_answer:
        if word in lines:
            shared_words.append(word)
            number_of_shared_words += len(shared_words)
    return number_of_shared_words