from django.shortcuts import render
from django.urls import reverse
from Prometheus.models.models import *
from django.apps import apps
import datetime


def transcript(request):
    '''
    This function renders the corporation view, which shows the selected 
    corporation's earnings data on the D3 line graph and populates the select
    box with transcripts for the user to choose.

    ---Arguments---
    request: the full HTTP request object

    ---Return Value---
    request: the full HTTP request object
    template: index.html
    context:    "dates": sorted_dates -- dates of available transcripts
                "corporation": corporation -- the company selected
    '''

    # Here we grab the corporation name from the URL in order to query the 
    # database
    corporation = (request.path).replace("/","")
    
    # Grab the appropriate model with the string pulled from the URL
    model = apps.get_model('Prometheus', corporation)

    # The database contains questions and answers from the earnings call 
    # transcripts. A question field with a zero indicates an answer.
    answers_query_set = model.objects.filter(question=0)

    # Sort the dates of available transcripts.
    dates = {answer.date_of_call for answer in answers_query_set}
    dates = [datetime.datetime.strptime(
        str(date), "%Y-%m-%d") for date in dates]
    dates.sort()
    sorted_dates = [datetime.datetime.strftime(
        date, "%d %B %y") for date in dates]

    corporation = answers_query_set[0].corporation

    template = 'index.html'
    context = {"dates": sorted_dates, "corporation": corporation}

    return render(request, template, context)