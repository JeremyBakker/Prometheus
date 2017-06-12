import datetime
from django.shortcuts import render
from django.urls import reverse
from Prometheus.models.models import *


def AMZN_transcript(request):
    
    template = 'corporations.html'

    transcripts = AAPL.objects.filter(question=0)

    questions = {transcript.name: transcript.question_answer_text for transcript in transcripts}

    dates = {transcript.date_of_call for transcript in transcripts}
    dates = [datetime.datetime.strptime(str(date), "%Y-%m-%d") for date in dates]
    dates.sort()
    sorted_dates = [datetime.datetime.strftime(date, "%d %B %y") for date in dates]


    context = {"transcripts": transcripts, "dates": sorted_dates}

    return render(request, template, context)