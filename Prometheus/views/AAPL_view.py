from django.shortcuts import render
from django.urls import reverse
from Prometheus.models.models import *
from django.http import HttpRequest
import datetime


def AAPL_transcript(request):
    print("AAPL request", request)
    print(request.path)
    if request.method == "GET":
        template = 'corporations.html'

        answers_query_set = AAPL.objects.filter(question=0)

        dates = {answer.date_of_call for answer in answers_query_set}
        dates = [datetime.datetime.strptime(str(date), "%Y-%m-%d") for date in dates]
        dates.sort()
        sorted_dates = [datetime.datetime.strftime(date, "%d %B %y") for date in dates]

        corporation = answers_query_set[0].corporation

        context = {"dates": sorted_dates, "corporation": corporation}

    if request.method == "POST":
        print("POST")
    #     apple_ceo_list = ['Jobs', 'Cook'] 
    #     apple_cfo_list = ['Oppenheimer', 'Maestri']


    #     answers_dict = {answer.name: answer.question_answer_text for answer in answers_query_set}
        
    #     cEo_questions_list = list()
    #     cFo_questions_list = list()

    #     for answer in answers_query_set:
    #         if "Jobs" in answer.name:
    #             cEo_questions_list.append({answer.question_answer_text:answer.date_of_call})
    #         if "Oppenheimer" in answer.name:
    #             cFo_questions_list.append({answer.question_answer_text:answer.date_of_call})
    #     print("cEo_questions_list", cEo_questions_list)
    #     print("cFo_questions_list", cFo_questions_list)




    # context = {"answers": answers_query_set, "dates": sorted_dates}

    return render(request, template, context)