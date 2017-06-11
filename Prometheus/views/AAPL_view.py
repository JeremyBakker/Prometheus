from django.shortcuts import render
from django.urls import reverse
from Prometheus.models.models import *


def AAPL_transcript(request):
    
    template_name = 'corporations.html'
    context = {}

    transcripts = AAPL.objects.filter(question=0)

    questions = {transcript.name: transcript.question_answer_text for transcript in transcripts}

    dates = {transcript.date_of_call for transcript in transcripts}

    context = {"transcripts": transcripts, "dates": dates}

    return render(request, template_name, context)