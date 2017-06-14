from django.shortcuts import render
from django.apps import apps
from nltk import word_tokenize
from statistics import median
import datetime
import nltk
import re

def search (request):

    c_executive_o_list = ['^(Steve)? ?Jobs', '^(Tim)?(othy)? ?Cook']
    c_financial_o_list = ['^(Peter)? ?Oppenheimer', '^(Luca)? ?Maestri']
    c_executive_o_list_regex = re.compile(r'\b(?:%s)\b' % '|'.join(c_executive_o_list))
    c_financial_o_list_regex = re.compile(r'\b(?:%s)\b' % '|'.join(c_financial_o_list))
    try:
        transcript = request.GET['transcript']
        corporation = transcript.split('-')[0]
        transcript_date = transcript.split('-')[1]

        transcript_date = datetime.datetime.strptime((transcript_date), "%d %B %y")
        transcript_date_for_db = datetime.datetime.strftime((transcript_date), "%Y-%m-%d")
        transcript_date_for_display = datetime.datetime.strftime((transcript_date), "%B %d, %Y")

        model = apps.get_model('Prometheus', corporation)

        answers_query_set = model.objects.filter(date_of_call = transcript_date_for_db, question=0).order_by("name")
        
        number_of_answers = len(answers_query_set)
        c_executive_o_answer_list = list()
        c_financial_o_answer_list = list()
        c_executive_o_answer_length_list = list()
        c_financial_o_answer_length_list = list()
        number_of_c_executive_o_negative_words = 0
        number_of_c_financial_o_negative_words = 0
        number_of_c_executive_o_positive_words = 0
        number_of_c_financial_o_positive_words = 0

        for answer in answers_query_set:
            if c_executive_o_list_regex.search(answer.name):                
                filtered_answer = clean_text(answer.question_answer_text)
                c_executive_o_answer_list.append(filtered_answer)
                c_executive_o_answer_length_list.append(len(filtered_answer))    
                
                with open('Prometheus/static/lexicons/negative_words.txt', 'r') as file:
                    lines = [line.strip() for line in file.readlines()]
                    if set(filtered_answer).intersection(lines):
                        negative_intersection_length = find_intersection_length(filtered_answer, lines)
                        number_of_c_executive_o_negative_words += negative_intersection_length
            
                with open('Prometheus/static/lexicons/positive_words.txt', 'r') as file:
                    lines = [line.strip() for line in file.readlines()]
                    if set(filtered_answer).intersection(lines):
                        positive_intersection_length = find_intersection_length(filtered_answer, lines)
                        number_of_c_executive_o_positive_words += positive_intersection_length

            if c_financial_o_list_regex.search(answer.name):
                filtered_answer = clean_text(answer.question_answer_text)

                c_financial_o_answer_list.append(filtered_answer)
                c_financial_o_answer_length_list.append(len(filtered_answer))
                
                with open('Prometheus/static/lexicons/negative_words.txt', 'r') as file:
                    lines = [line.strip() for line in file.readlines()]
                    if set(filtered_answer).intersection(lines):
                        negative_intersection_length = find_intersection_length(filtered_answer, lines)
                        number_of_c_financial_o_negative_words += negative_intersection_length

                with open('Prometheus/static/lexicons/positive_words.txt', 'r') as file:
                    lines = [line.strip() for line in file.readlines()]
                    if set(filtered_answer).intersection(lines):
                        positive_intersection_length = find_intersection_length(filtered_answer, lines)
                        number_of_c_financial_o_positive_words += positive_intersection_length

        c_executive_o_answer_length_sum = sum(c_executive_o_answer_length_list)
        c_financial_o_answer_length_sum = sum(c_financial_o_answer_length_list)

        try:
            c_executive_o_answer_length_median = median(c_executive_o_answer_length_list)
        except ValueError:
            c_executive_o_answer_length_median = "N/A"
        try:
            c_financial_o_answer_length_median = int(median(c_financial_o_answer_length_list))
        except ValueError:
            c_financial_o_answer_length_median = "N/A"  
    except KeyError:
        corporation = ""
        pass

    c_executive_o_negative_proportion = number_of_c_executive_o_negative_words / c_executive_o_answer_length_sum
    c_financial_o_negative_proportion = number_of_c_financial_o_negative_words / c_financial_o_answer_length_sum
    c_executive_o_positive_proportion = number_of_c_executive_o_positive_words / c_executive_o_answer_length_sum
    c_financial_o_positive_proportion = number_of_c_financial_o_positive_words / c_financial_o_answer_length_sum
    

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
        "cFo_positive": round(c_financial_o_positive_proportion, 4)
        }
    return render(request, template, context)

def clean_text(question_answer_text):                
    tokenized_answer = word_tokenize(question_answer_text)
    without_punctuation = re.compile('.*[A-Za-z0-9].*')
    filtered_answer = [word.upper() for word in tokenized_answer if without_punctuation.match(word)]
    return filtered_answer

def find_intersection_length(filtered_answer, lines):
    intersection = set(filtered_answer).intersection(lines)
    intersection_length = len(intersection)
    return intersection_length