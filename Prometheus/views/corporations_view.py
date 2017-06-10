from django.shortcuts import render
from django.urls import reverse
from Prometheus.models.models import *


def corporations(request):
    
    template_name = 'corporations.html'
    context = {}

    transcripts = AMZN.objects.get(pk=1)
    # Transcripts.objects.filter(position=1, question=0)

    print("reverse", reverse('corporations'))

    context = {"transcripts": transcripts}

    return render(request, template_name, context)