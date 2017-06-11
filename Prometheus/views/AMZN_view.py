from django.shortcuts import render
from django.urls import reverse
from Prometheus.models.models import *


def AMZN_transcript(request):
    
    template_name = 'corporations.html'
    context = {}

    transcripts = AMZN.objects.get(pk=28)
    # Transcripts.objects.filter(position=1, question=0)

    context = {"transcripts": transcripts}

    return render(request, template_name, context)