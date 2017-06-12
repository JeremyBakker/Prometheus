from django.shortcuts import render
from django.urls import reverse
from Prometheus.models.models import *
from django.apps import apps
import datetime


def transcript(request):
    corporation = (request.path).replace("/","")
    model = apps.get_model('Prometheus', corporation)
    if request.method == "GET":
        template = 'index.html'

        answers_query_set = model.objects.filter(question=0)

        dates = {answer.date_of_call for answer in answers_query_set}
        dates = [datetime.datetime.strptime(str(date), "%Y-%m-%d") for date in dates]
        dates.sort()
        sorted_dates = [datetime.datetime.strftime(date, "%d %B %y") for date in dates]

        corporation = answers_query_set[0].corporation

        context = {"dates": sorted_dates, "corporation": corporation}

        return render(request, template, context)