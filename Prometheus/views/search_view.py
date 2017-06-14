from django.shortcuts import render
from django.apps import apps
import datetime
import re
import nltk
from nltk import word_tokenize
from statistics import median


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

        for answer in answers_query_set:
            if c_executive_o_list_regex.search(answer.name):                
                tokenized_answer = word_tokenize(answer.question_answer_text)
                without_punctuation = re.compile('.*[A-Za-z0-9].*')
                filtered_answer = [word for word in tokenized_answer if without_punctuation.match(word)]
                c_executive_o_answer_list.append(filtered_answer)
                c_executive_o_answer_length_list.append(len(filtered_answer))
            if c_financial_o_list_regex.search(answer.name):
                answer = word_tokenize(answer.question_answer_text)
                without_punctuation = re.compile('.*[A-Za-z0-9].*')
                filtered_answer = [word for word in answer if without_punctuation.match(word)]
                c_financial_o_answer_list.append(filtered_answer)
                c_financial_o_answer_length_list.append(len(filtered_answer))

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


    template = 'index.html'
    context = {
        "search_view": True, 
        "corporation": corporation, 
        "date": transcript_date_for_display, 
        "cFo_median": c_financial_o_answer_length_median, 
        "cFo_sum": c_financial_o_answer_length_sum,
        "cEo_median": c_executive_o_answer_length_median,
        "cEo_sum": c_executive_o_answer_length_sum
        }
    return render(request, template, context)
