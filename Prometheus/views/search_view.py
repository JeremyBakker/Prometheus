from django.shortcuts import render
from django.apps import apps
import datetime
import re
import nltk
from nltk import Text
from nltk import word_tokenize


def search (request):

    cEo_list = ['Steve Jobs']
    cFo_list = ['Peter Oppenheimer', 'Luca Maestri']
    try:
        transcript = request.GET['transcript']
        corporation = transcript.split('-')[0]
        transcript_date = transcript.split('-')[1]

        transcript_date = datetime.datetime.strptime((transcript_date), "%d %B %y")
        transcript_date_for_db = datetime.datetime.strftime((transcript_date), "%Y-%m-%d")
        transcript_date_for_display = datetime.datetime.strftime((transcript_date), "%B %d, %Y")

        model = apps.get_model('Prometheus', corporation)

        answers_query_set = model.objects.filter(date_of_call = transcript_date_for_db, question=0).order_by("name")
        for answer in answers_query_set:
            if any(answer.name in name for name in cEo_list):
                print(answer.name)
            if any(answer.name in name for name in cFo_list):
                print(answer.name)
                print(len(answer.question_answer_text))
                answer = word_tokenize(answer.question_answer_text)
                without_punctuation = re.compile('.*[A-Za-z0-9].*')
                filtered_answer = [word for word in answer if without_punctuation.match(word)]
                print("answer:", answer)
                print("length with punctuation: ", len(answer))
                print("length without punctuation: ", len(filtered_answer))

        
        

    except KeyError:
        corporation = ""
        pass


    template = 'index.html'
    context = {"search_view": True, "corporation": corporation, "date": transcript_date_for_display}
    return render(request, template, context)
