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

    # These lists of regex patterns contain the possible renderings of the 
    # names of CEOs and CFOs of the corporations whose transcripts we analyze.
    # The transcripts lack this data in any reliable pattern to pull when 
    # parsing. Thus, a hard-coded list is necessary for now.
    c_executive_o_list = ['^(Steve)? ?Jobs', '^(Tim)?(othy)? ?Cook']
    c_financial_o_list = ['^(Peter)? ?Oppenheimer', '^(Luca)? ?Maestri']
    c_executive_o_list_regex = re.compile(r'\b(?:%s)\b' % '|'.join(
        c_executive_o_list))
    c_financial_o_list_regex = re.compile(r'\b(?:%s)\b' % '|'.join(
        c_financial_o_list))
    
    try:
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

        answers_query_set = model.objects.filter(
            date_of_call = transcript_date_for_db, question=0).order_by("name")
        
        number_of_answers = len(answers_query_set)
        c_executive_o_answer_list = list()
        c_financial_o_answer_list = list()
        c_executive_o_answer_length_list = list()
        c_financial_o_answer_length_list = list()
        c_executive_o_negative_words = 0
        c_financial_o_negative_words = 0
        c_executive_o_positive_words = 0
        c_financial_o_positive_words = 0
        c_executive_o_bigram_references_to_general_knowledge = 0
        c_executive_o_trigram_references_to_general_knowledge = 0
        c_financial_o_bigram_references_to_general_knowledge = 0
        c_financial_o_trigram_references_to_general_knowledge = 0

        # For each answer, we determine whether it correlates to the CEO or 
        # CFO. Then, after tokenizing the text, removing punctuation, and 
        # capitalizing each word, we split the text into bigrams and trigrams 
        # for searching by phrase. From there, we compare n-grams (1, 2, or 3)
        # to relevant lectionaries stored as .txt files to determine text
        # characteristics (positive_words, general_knowledge, etc.). 
        for answer in answers_query_set:
            if c_executive_o_list_regex.search(answer.name):
                c_executive_o_filtered_answer = clean_text(
                    answer.question_answer_text)
                c_executive_o_answer_list.append(
                    c_executive_o_filtered_answer)
                c_executive_o_answer_length_list.append(len(
                    c_executive_o_filtered_answer))    
                
                c_executive_o_bigrams = list(ngrams(
                    c_executive_o_filtered_answer, 2))
                c_executive_o_bigrams_strings = ["%s %s" % bigram for 
                    bigram in c_executive_o_bigrams]
                c_executive_o_trigrams = list(ngrams(
                    c_executive_o_filtered_answer, 3))
                c_executive_o_trigrams_strings = ["%s %s %s" % trigram for 
                    trigram in c_executive_o_trigrams]

                with open('Prometheus/static/lexicons/negative_words.txt', 
                    'r') as file:
                    lines = [line.strip() for line in file.readlines()]
                    if set(c_executive_o_filtered_answer).intersection(lines):
                        negative_intersection_length = \
                            find_intersection_length(
                            c_executive_o_filtered_answer, lines)
                        c_executive_o_negative_words += \
                            negative_intersection_length

                with open('Prometheus/static/lexicons/positive_words.txt', 
                    'r') as file:
                    lines = [line.strip() for line in file.readlines()]
                    if set(c_executive_o_filtered_answer).intersection(lines):
                        positive_intersection_length = \
                            find_intersection_length(
                            c_executive_o_filtered_answer, lines)
                        c_executive_o_positive_words += \
                            positive_intersection_length

                with open('Prometheus/static/lexicons/general_knowledge.txt', 
                    'r') as file:
                    lines = [line.strip().upper() for line in file.readlines()]
                    if set(c_executive_o_bigrams_strings).intersection(lines):
                        c_executive_o_bigram_references_to_general_knowledge \
                        += 1
                    if set(c_executive_o_trigrams_strings).intersection(lines):
                        c_executive_o_trigram_references_to_general_knowledge \
                        += 1
 
            if c_financial_o_list_regex.search(answer.name):
                c_financial_o_filtered_answer = clean_text(
                    answer.question_answer_text)
                c_financial_o_answer_list.append(
                    c_financial_o_filtered_answer)
                c_financial_o_answer_length_list.append(
                    len(c_financial_o_filtered_answer))

                c_financial_o_bigrams = list(ngrams(
                    c_financial_o_filtered_answer, 2))
                c_financial_o_bigrams_strings = ["%s %s" % bigram for 
                    bigram in c_financial_o_bigrams]
                c_financial_o_trigrams = list(ngrams(
                    c_financial_o_filtered_answer, 3))
                c_financial_o_trigrams_strings = ["%s %s %s" % trigram for 
                    trigram in c_financial_o_trigrams]

                with open('Prometheus/static/lexicons/negative_words.txt', 
                    'r') as file:
                    lines = [line.strip() for line in file.readlines()]
                    if set(c_financial_o_filtered_answer).intersection(lines):
                        negative_intersection_length = \
                            find_intersection_length(
                            c_financial_o_filtered_answer, lines)
                        c_financial_o_negative_words += \
                            negative_intersection_length

                with open('Prometheus/static/lexicons/positive_words.txt', 
                    'r') as file:
                    lines = [line.strip() for line in file.readlines()]
                    if set(c_financial_o_filtered_answer).intersection(lines):
                        positive_intersection_length = \
                            find_intersection_length(
                            c_financial_o_filtered_answer, lines)
                        c_financial_o_positive_words += \
                            positive_intersection_length

                with open('Prometheus/static/lexicons/general_knowledge.txt', 
                    'r') as file:
                    lines = [line.strip().upper() for line in file.readlines()]
                    if set(c_financial_o_bigrams_strings).intersection(lines):
                        c_financial_o_bigram_references_to_general_knowledge \
                        += 1
                    if set(c_financial_o_trigrams_strings).intersection(lines):
                        c_financial_o_trigram_references_to_general_knowledge \
                        += 1

        c_executive_o_answer_length_sum = sum(c_executive_o_answer_length_list)
        c_financial_o_answer_length_sum = sum(c_financial_o_answer_length_list)

        try:
            c_executive_o_answer_length_median = median(
                c_executive_o_answer_length_list)
        except ValueError:
            c_executive_o_answer_length_median = "N/A"

        try:
            c_financial_o_answer_length_median = median(
                c_financial_o_answer_length_list)
        except ValueError:
            c_financial_o_answer_length_median = "N/A"  

    except KeyError:
        corporation = ""
        pass

    c_executive_o_negative_proportion = \
        c_executive_o_negative_words / \
        c_executive_o_answer_length_sum
    c_financial_o_negative_proportion = \
        c_financial_o_negative_words / \
        c_financial_o_answer_length_sum
    c_executive_o_positive_proportion = \
        c_executive_o_positive_words / \
        c_executive_o_answer_length_sum
    c_financial_o_positive_proportion = \
        c_financial_o_positive_words / \
        c_financial_o_answer_length_sum
    c_executive_o_percentage_references_to_general_knowledge = \
        (c_executive_o_bigram_references_to_general_knowledge + 
        c_executive_o_trigram_references_to_general_knowledge) / \
        len(c_executive_o_answer_list)
    c_financial_o_percentage_references_to_general_knowledge = \
        (c_financial_o_bigram_references_to_general_knowledge + 
        c_financial_o_trigram_references_to_general_knowledge) / \
        len(c_financial_o_answer_list)

    template = 'index.html'
    context = {
        "search_view": True, 
        "corporation": corporation, 
        "date": transcript_date_for_display, 
        "cFo_median": c_financial_o_answer_length_median, 
        "cFo_sum": c_financial_o_answer_length_sum,
        "cEo_median": c_executive_o_answer_length_median,
        "cEo_sum": c_executive_o_answer_length_sum,
        "cFo_negative": round(c_financial_o_negative_proportion, 4),
        "cEo_negative": round(c_executive_o_negative_proportion, 4),
        "cEo_positive": round(c_executive_o_positive_proportion, 4),
        "cFo_positive": round(c_financial_o_positive_proportion, 4),
        "cEo_knowledge": round(
            c_executive_o_percentage_references_to_general_knowledge, 4),
        "cFo_knowledge": round(
            c_financial_o_percentage_references_to_general_knowledge, 4)
        }

    return render(request, template, context)

def clean_text(question_answer_text):
    tokenized_answer = word_tokenize(question_answer_text)
    without_punctuation = re.compile('.*[A-Za-z0-9].*')
    filtered_answer = [word.upper() for word in tokenized_answer if 
        without_punctuation.match(word)]
    return filtered_answer

def find_intersection_length(filtered_answer, lines):
    intersection = set(filtered_answer).intersection(lines)
    intersection_length = len(intersection)
    return intersection_length